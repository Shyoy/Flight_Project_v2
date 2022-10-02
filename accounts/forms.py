from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs["placeholder"] = f'  {self.fields[fieldname].label}'
            self.fields[fieldname].label = ''
    
    email = forms.EmailField(label='',
    widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Address'}),
        help_text="Must be a valid email address"
        )
    # email.widget.attrs["placeholder"] = f'Enter email Here'
    class Meta:
        model = models.CustomUser
        fields = ['username', 'email','password1', 'password2']


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        exclude  = ('user',)
    # def __init__(self, *args, **kwargs):
    #     super(CustomerProfileForm, self).__init__(*args, **kwargs)
    #     for key in self.fields.keys(): 
    #         self.fields[key].required = True
    #         print(f'{key}')