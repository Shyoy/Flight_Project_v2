from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
# Generic
from django.views.generic import ListView ,DetailView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from . import models
# from . import services

# Create your views here.


class RegisterForm(FormView):
    template_name = 'accounts/register.html'
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('homepage')
    
    def form_valid(self, form): ##TODO: finish user save
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # ? FIXME: should connect to receivers
        print('form is valid') 
        user= form.save()
        print('user saved successfully') 
        group = Group.objects.get(name='customers')
        user.groups.add(group)
        login(self.request, user)
        print('user logged in successfully') 
       
        return super(RegisterForm, self).form_valid(form)