from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
# Create your models here.

# # New FIELD
# class NameField(models.CharField):
#     def __init__(self, *args, **kwargs):
#         super(NameField, self).__init__(*args, **kwargs)

#     def get_prep_value(self, value):
#         return str(value).lower()


class Country(models.Model):
    name = models.CharField(max_length=200 , unique=True)
    pic = models.URLField(default="https://www.supercoloring.com/sites/default/files/styles/coloring_medium/public/cif/2022/03/question-mark-flag-emoji-coloring-page.png")
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
        return f'On: {self.departure_time.ctime()}--From: {self.origin_country}--To: {self.destination_country}'
        # return f'Flight number: {self.id} - Date: {self.departure_time.date()} - Remaining Tickets: {self.remaining_tickets}'

    class Meta:
        ordering = ['departure_time']

    def clean(self):
        if (self.airline.country != self.destination_country) and (self.airline.country != self.origin_country):
            raise ValidationError(f'This Flight Must depart from, or land at {self.airline.country} !')
            
        if self.origin_country == self.destination_country:
            raise ValidationError(f'Origin Country and Destination Country can\'t be the same !')
        if self.tickets < 50:
            raise ValidationError(f'Flight size must be greater than 50 !')
        if self.departure_time > self.landing_time:
            raise ValidationError(f'Landing time must be after departure time !')
        if self.flight_duration < timedelta(hours=1):
            raise ValidationError(f'Flight duration can\'t be less then 1 hour !')
            
        # if self.departure_time < timezone.now():
        #     raise ValidationError(f'You can only add future flights dates !')
