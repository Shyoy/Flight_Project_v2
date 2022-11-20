
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
# Generic
from django.views.generic import ListView ,DetailView, CreateView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from . import models
# from . import services
from accounts.mixins import AllowedGroupsTestMixin
from django.contrib import messages
# Create your views here.


class RegisterForm(FormView):
    template_name = 'accounts/register.html'
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('home')
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            username = request.user.username
            messages.add_message(self.request, messages.WARNING,
                                 f'{username} You are already logged in')
            return redirect(self.success_url)
        return super(RegisterForm, self).get(request, *args, **kwargs)


    def form_valid(self, form): 
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # ? FIXME: should connect to receivers?
        user= form.save()
        group = Group.objects.get(name='customers')
        user.groups.add(group)
        login(self.request, user)
        messages.add_message(self.request, messages.SUCCESS,
                                 'User Created Successfully')
        return super(RegisterForm, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.add_message(self.request, messages.WARNING,
                                 'User Registration failed Make sure the data you entered is valid !')
        return self.render_to_response(self.get_context_data(form=form))



class AdminRegister(AllowedGroupsTestMixin, FormView):
    allowed_groups =['superuser']
    template_name = 'administrator/admin_register.html'
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('admin_profile')

    def get(self, request, *args, **kwargs):
        self.new_admin_user = self.request.session.get('new_admin_user')
        if self.new_admin_user:
            new_user = models.CustomUser.objects.get(id = self.new_admin_user)
            messages.add_message(self.request, messages.WARNING,
                                 f'Create a profile for User "{new_user}" !')
            return redirect(self.success_url)
        return super(AdminRegister, self).get(request, *args, **kwargs)
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user= form.save()
        group = Group.objects.get(name='administrators')
        user.groups.add(group)
        self.request.session['new_admin_user'] = user.id
        messages.add_message(self.request, messages.SUCCESS,
                                 f'Good now create a profile for User "{user}"')
        return super(AdminRegister, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        messages.add_message(self.request, messages.WARNING,
                                 'Administrator account creation failed !')
        return self.render_to_response(self.get_context_data(form=form))


class AdminProfile(AllowedGroupsTestMixin, FormView):
    allowed_groups =['superuser']
    template_name = 'administrator/admin_register.html'
    form_class = forms.AdminProfileForm
    success_url = reverse_lazy('homepage')

    def get(self, request, *args, **kwargs):
        self.new_admin_user = self.request.session.get('new_admin_user')
        if not self.new_admin_user:
            return redirect('admin_register')
        new_user = models.CustomUser.objects.get(id = self.new_admin_user)
        messages.add_message(self.request, messages.WARNING,
                                 f'Create a profile for User "{new_user}" !')
        return super(AdminProfile, self).get(request, *args, **kwargs)
    
    def get_initial(self):
        self.new_admin_user = self.request.session.get('new_admin_user')
        new_user = models.CustomUser.objects.get(id = self.new_admin_user)
        return {'user': new_user}

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        new_admin_user = self.request.session.get('new_admin_user')
        new_user = models.CustomUser.objects.get(id = new_admin_user)
        administrator= form.save(commit=False)
        administrator.user = new_user
        administrator.save()
        print(administrator)
        messages.add_message(self.request, messages.SUCCESS,
                                 f'Administrator "{administrator}" Created Successfully you can login now.')
        del self.request.session['new_admin_user']
        return super(AdminProfile, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        print(form.data)
        messages.add_message(self.request, messages.WARNING,
                                 'Administrator account creation failed !')
        return self.render_to_response(self.get_context_data(form=form))


class AirlineRegister(AllowedGroupsTestMixin, TemplateView):
    allowed_groups =['administrators']
    template_name = 'airline/airline_register.html'
    # form_class = forms.AddAirline
    success_url = reverse_lazy('airlines_manager')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_form = forms.UserRegisterForm()
        airline_form = forms.AddAirline()
        context['title'] = 'Airline Signup'
        context['user_form'] = user_form
        context['airline_form'] = airline_form
        return context

    def post(self,request, *args, **kwargs):
        user_form = forms.UserRegisterForm(request.POST)
        airline_form = forms.AddAirline(request.POST)
        if all([user_form.is_valid() ,airline_form.is_valid()]):
            user= user_form.save()
            group = Group.objects.get(name='airlines')
            user.groups.add(group)
            country = airline_form.cleaned_data['country']
            models.Airline.objects.create(user=user , name=user.username, country = country )
            messages.add_message(self.request, messages.SUCCESS,
                                 f'{user.username} Airline Created Successfully you can login now.')
            return redirect(self.success_url)
        
        else:
            messages.add_message(self.request, messages.WARNING,
                                 'Airline account creation failed !')
            context={'user_form':user_form,'airline_form':airline_form}
            context['title'] = 'Airline SignUp'
            return self.render_to_response(context=context)


class AirlineDetailUpdate(AllowedGroupsTestMixin, DetailView):##TODO implement Update for Airline account by airline
    allowed_groups =['administrators']
    template_name = 'airline/airline_register.html'
    model = models.Airline
    success_url = reverse_lazy('airlines_manager')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = forms.UserRegisterForm(instance=self.get_object().user)
        airline_form = forms.AddAirline(instance=self.get_object())


        context['title'] = 'Airline Update'
        context['user_form'] = user_form
        context['airline_form'] = airline_form
        return context

    def post(self,request, *args, **kwargs):
        user_form = forms.UserRegisterForm(request.POST)
        airline_form = forms.AddAirline(request.POST)
        if all([user_form.is_valid() ,airline_form.is_valid()]):
            username = user_form.cleaned_data['username']
            country = airline_form.cleaned_data['country']
            
            messages.add_message(self.request, messages.SUCCESS,
                                 f'{username} Airline Created Successfully you can login now.')
            return redirect(self.success_url)
        
        else:
            messages.add_message(self.request, messages.WARNING,
                                 'Airline account creation failed !')
            context={'user_form':user_form,'airline_form':airline_form}
            context['title'] = 'Airline Update'
            return self.render_to_response(context=context)