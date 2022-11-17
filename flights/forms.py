from django import forms
from . import models
from accounts import models as acc_models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from django.utils import timezone
from django.core.exceptions import ValidationError


# TODO: Customer Forms
class SearchFlightsForm(forms.Form):

    origin_country = forms.CharField(label='From:', widget=forms.TextInput(attrs={'placeholder': 'Country name','size':13}),required = False)
    destination_country = forms.CharField(label='To:', widget=forms.TextInput(attrs={'placeholder': 'Country name' ,'size':13}),required = False)
    departure_time = forms.DateField(label='Date:', widget=forms.DateInput(attrs={'type':'date'}),required = False)
    # landing_time = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}),required = False)

    def clean(self):
        if self.departure_time < timezone.now().date() and self.departure_time:
            raise ValidationError(f'you can only look for future flights dates')


# TODO: Administrator Forms
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
     
    def clean(self):
        data = list(self.data.keys())
        if not all([field in data for field in self.fields.keys()]):
            raise ValidationError("This form needs to contain all is fields")

# TODO: Airline Forms
class AirlineSearchFlightsForm(forms.ModelForm):
        class Meta:
            model = models.Flight
            fields  = ('departure_time','origin_country','destination_country',)
        departure_time = forms.DateField(label='Departure Time', widget=forms.DateInput(format='%d-%m-%Y',attrs={'type':'date'}),required = False)
        def __init__(self, *args, **kwargs):
            super(AirlineSearchFlightsForm, self).__init__(*args, **kwargs)
            # self.fields['departure_time'].widget =forms.DateInput(attrs={'type':'date'})
            for fieldname in self.fields.keys(): 
                self.fields[fieldname].widget.attrs.update({'class':'form-control','style':'position: absolute; z-index: 2; max-width:180px;'})
                self.fields[fieldname].required = False
                
                self.fields[fieldname].label += ":"
             
        def clean(self):
            data = list(self.data.keys())
            if not all([field in data for field in self.fields.keys()]):
                raise ValidationError("This form needs to contain all is fields")


class AddFlightForm(forms.ModelForm):
    class Meta:
        model = models.Flight
        exclude  = ('airline','passengers',)
    # departure_time = forms.DateField(label='Departure Time', widget=forms.DateInput(attrs={'type':'datetime-local'}))
    # landing_time = forms.DateField(label='landing_time', widget=forms.DateInput(attrs={'type':'datetime-local'}))
    def __init__(self, *args, **kwargs):
        super(AddFlightForm, self).__init__(*args, **kwargs)
        self.fields['departure_time'].widget = forms.DateInput(attrs={'type':'datetime-local'})
        self.fields['landing_time'].widget = forms.DateInput(attrs={'type':'datetime-local'})
        for fieldname in self.fields.keys(): 
            self.fields[fieldname].widget.attrs.update({'class':'form-control','style':'z-index: 2;'})
            # self.fields[fieldname].widget.attrs["size"] = 12
    def clean(self):
        print('cleanings_time')
    #     self.fields['last_name'].widget.attrs["placeholder"] = 'Obama'
    #     self.fields['phone_number'].widget.attrs["placeholder"] = '0549998888'



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
