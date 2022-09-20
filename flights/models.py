from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class Flight(models.Model):
    departure_time = models.DateTimeField(default=timezone.now)
    landing_time = models.DateTimeField(default=timezone.now)
    tickets = models.IntegerField()

    @property
    def remaining_tickets(self):
        if hasattr(self.passengers, 'first') and self.passengers.first() != None:
            return self.tickets - len(list(self.passengers))
        return self.tickets

        
    def __str__(self):
        return f'Flight number: {self.id} - Date: {self.departure_time.date()} - Remaining Tickets: {self.remaining_tickets}'

class Country(models.Model):
    name = models.CharField(max_length=200)
    departing_flights =models.ForeignKey(Flight,related_name='origin_country', on_delete=models.DO_NOTHING)
    landing_flights =models.ForeignKey(Flight,related_name='destination_country', on_delete=models.DO_NOTHING)




# class User_role(models.Model):
    
#     Role_name = models.CharField(max_length=100)
