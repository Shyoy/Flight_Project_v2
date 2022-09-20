from django.db import models

#Res
from django.contrib.auth.models import AbstractUser, User
from flights.models import Flight

# Tools
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator ,MaxLengthValidator
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    # class Meta(AbstractUser.Meta):
    #     swappable = "AUTH_USER_MODEL"
    
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, related_name='customer', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField(_("phone number"),validators=[MinLengthValidator(6), MaxLengthValidator(12)])
    flights = models.ManyToManyField(Flight, related_name='passengers')

    def __str__(self):
        return self.first_name + " " + self.last_name


class Airline(models.Model):
    user = models.OneToOneField(CustomUser, related_name='airline', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    flights = models.ForeignKey(Flight, related_name='airline', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Administrator(models.Model):
    user = models.OneToOneField(CustomUser, related_name='administrator', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name

