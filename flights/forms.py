from django import forms
from . import models
from accounts import models as acc_models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from django.utils import timezone
from django.core.exceptions import ValidationError


# class UserRegisterForm(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super(UserRegisterForm, self).__init__(*args, **kwargs)
#         for fieldname in ['username', 'password1', 'password2']:
#             self.fields[fieldname].widget.attrs["placeholder"] = f'  {self.fields[fieldname].label}'
#             self.fields[fieldname].label = ''
    
#     email = forms.EmailField(label='',
#     widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Address'}),
#         help_text="Must be a valid email address"
#         )
#     # email.widget.attrs["placeholder"] = f'Enter email Here'
#     class Meta:
#         model = models.CustomUser
#         fields = ['username', 'email','password1', 'password2']


class SearchFlightsForm(forms.Form):

    origin_country = forms.CharField(label='From:', widget=forms.TextInput(attrs={'placeholder': 'Country name','size':13}),required = False)
    destination_country = forms.CharField(label='To:', widget=forms.TextInput(attrs={'placeholder': 'Country name' ,'size':13}),required = False)
    departure_time = forms.DateField(label='Date:', widget=forms.DateInput(attrs={'type':'date'}),required = False)
    # landing_time = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}),required = False)

    def clean(self):
        super().clean()
        if self.departure_time < timezone.now().date() and self.departure_time:
            raise ValidationError(f'you can only look for future flights dates')



class SearchAirlineForm(forms.ModelForm):
    class Meta:
        model = acc_models.Airline
        fields  = ('name','country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control','placeholder': 'Airline Name','size':13})
        self.fields['name'].required = False
        self.fields['country'].widget.attrs.update({'class':'form-control','style':'position: absolute; z-index: 2; max-width:400px;'})
        self.fields['country'].required = False






# class AddAirline(forms.ModelForm):
#     class Meta:
#         model = models.Customer
#         exclude  = ('user',)
#     origin_country = forms.CharField(label='From:', widget=forms.TextInput(attrs={'placeholder': 'Country name','size':13}),required = False)
#     destination_country = forms.CharField(label='To:', widget=forms.TextInput(attrs={'placeholder': 'Country name' ,'size':13}),required = False)
#     departure_time = forms.DateField(label='Date:', widget=forms.DateInput(attrs={'type':'date'}),required = False)
#     # landing_time = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}),required = False)

#     def clean(self):
#         super().clean()
#         if self.departure_time < timezone.now().date() and self.departure_time:
#             raise ValidationError(f'you can only look for future flights dates')
