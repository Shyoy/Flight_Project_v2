from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.

# # New FIELD
# class NameField(models.CharField):
#     def __init__(self, *args, **kwargs):
#         super(NameField, self).__init__(*args, **kwargs)

#     def get_prep_value(self, value):
#         return str(value).lower()


class Country(models.Model):
    name = models.CharField(max_length=200 , unique=True)
    pic = models.URLField(blank=True,null=True)
    # departing_flights =models.ForeignKey(Flight,related_name='origin_country', on_delete=models.DO_NOTHING)
    # landing_flights =models.ForeignKey(Flight,related_name='destination_country', on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name


class Flight(models.Model):
    airline = models.ForeignKey('accounts.Airline', related_name='flights', on_delete=models.PROTECT)
    departure_time = models.DateTimeField(default=timezone.now)
    landing_time = models.DateTimeField(default=timezone.now)
    tickets = models.IntegerField(default=150)
    origin_country =models.ForeignKey(Country,related_name='departing_flights', on_delete=models.CASCADE)
    destination_country =models.ForeignKey(Country,related_name='landing_flights', on_delete=models.CASCADE)
    passengers = models.ManyToManyField('accounts.Customer', blank=True, related_name='flights')


    @property
    def remaining_tickets(self):
        return self.tickets - self.passengers.count()
    
    @property
    def flight_duration(self):
        return self.landing_time - self.departure_time

        
    def __str__(self):
        return f'Flight number: {self.id} - Date: {self.departure_time.date()} - Remaining Tickets: {self.remaining_tickets}'



# class User_role(models.Model):
    
#     Role_name = models.CharField(max_length=100)
