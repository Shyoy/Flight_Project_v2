from django.db import models
from django.core.exceptions import ValidationError

#Res
from django.contrib.auth.models import AbstractUser
# from flights.models import Flight

# Tools
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator ,MaxLengthValidator
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, related_name='customer', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    phone_number = models.CharField(_("phone number"), max_length=12, validators=[MinLengthValidator(6)],blank=True, null=True)

    @property
    def valid_customer(self):
        return all([self.first_name,self.last_name,self.phone_number])


    def __str__(self):
        if not self.valid_customer:
            return self.user.email
        return self.first_name + " " + self.last_name

    def clean(self):
        if self.phone_number and not self.phone_number.isdigit():
            raise ValidationError('Phone Number must countian only digits !')
        if self.first_name and not self.first_name.isalpha():
            raise ValidationError('First Name must countian only Letters !')
        if self.last_name and not self.last_name.isalpha():
            raise ValidationError('Last Name must countian only Letters !')
        

class Airline(models.Model):
    user = models.OneToOneField(CustomUser, related_name='airline', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey('flights.Country', related_name='airlines',on_delete=models.DO_NOTHING)
    
    class Meta:
        ordering = ['-id']

    # @property
    # def valid_airline(self):
    #     return self.country
     

    def __str__(self):
        return self.name


class Administrator(models.Model):##TODO: way to add Administrator potfile
    user = models.OneToOneField(CustomUser, related_name='administrator', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)

    # @property
    # def valid_admin(self):
    #     return all([self.first_name,self.last_name])
        

    def __str__(self):
        return self.user.username
        

