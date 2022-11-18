
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
        print('form is valid') 
        user= form.save()
        print('user saved successfully') 
        group = Group.objects.get(name='customers')
        user.groups.add(group)
        login(self.request, user)
        print('user logged in successfully') 
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
    success_url = reverse_lazy('admin_register')
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print('form is valid') 
        user= form.save()
        print('user saved successfully') 
        group = Group.objects.get(name='administrators')
        user.groups.add(group)
        messages.add_message(self.request, messages.SUCCESS,
                                 'Administrator account Created Successfully you can login now.')
        return super(AdminRegister, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
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
        context['title'] = 'Airline SingUp'
        context['user_form'] = user_form
        context['airline_form'] = airline_form
        return context

    def post(self,request, *args, **kwargs):
        print('this is POST')
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
            print('not valid')
            messages.add_message(self.request, messages.WARNING,
                                 'Airline account creation failed !')
            context={'user_form':user_form,'airline_form':airline_form}
            context['title'] = 'Airline SingUp'
            return self.render_to_response(context=context)


class AirlineDetailUpdate(AllowedGroupsTestMixin, DetailView):##TODO implement Update for Airline account by airline
    allowed_groups =['administrators']
    template_name = 'airline/airline_register.html'
    model = models.Airline
    success_url = reverse_lazy('airlines_manager')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.request)
        # print(self.context_object_name)
        # print(self.queryset)
        # print(self.get_object().id)
        # print(self.queryset)

        user_form = forms.UserRegisterForm(instance=self.get_object().user)
        airline_form = forms.AddAirline(instance=self.get_object())


        context['title'] = 'Airline Update'
        context['user_form'] = user_form
        context['airline_form'] = airline_form
        return context

    def post(self,request, *args, **kwargs):
        print('this is POST')
        user_form = forms.UserRegisterForm(request.POST)
        airline_form = forms.AddAirline(request.POST)
        if all([user_form.is_valid() ,airline_form.is_valid()]):
            print(user_form.cleaned_data)
            username = user_form.cleaned_data['username']
            country = airline_form.cleaned_data['country']
            
            messages.add_message(self.request, messages.SUCCESS,
                                 f'{username} Airline Created Successfully you can login now.')
            return redirect(self.success_url)
        
        else:
            print('not valid')
            messages.add_message(self.request, messages.WARNING,
                                 'Airline account creation failed !')
            context={'user_form':user_form,'airline_form':airline_form}
            context['title'] = 'Airline Update'
            return self.render_to_response(context=context)