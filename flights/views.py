from django.shortcuts import render, redirect
from django.views.generic import TemplateView ,FormView
from accounts.forms import CustomerProfileForm
from django.urls import reverse_lazy
from accounts import models as acc_models

# 

def error_404_view(request, exception=None):
    # make a redirect to homepage
    return redirect('homepage') # or redirect('name-of-index-url')

def home(request):
    return redirect('homepage')

def homepage(request):
    return render(request, 'flights/homepage.html')


# TODO: Customer views

class CustomerProfile(FormView):
    template_name = 'customer/profile.html'
    form_class = CustomerProfileForm
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        """Adds customer details to the context"""
        context = super(CustomerProfile, self).get_context_data(**kwargs)
        context['customer'] = self.request.user.customer.__dict__
        return context

    def get_form(self):
        """Returns form_class with user customer as instance"""
        return self.form_class(instance=self.request.user.customer, **self.get_form_kwargs())
    
    def form_valid(self, form):
        """This saves the form that creates new customer and returns success_url"""
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super(CustomerProfile, self).form_valid(form)





# TODO: AirLine views
# TODO: Administrator views
