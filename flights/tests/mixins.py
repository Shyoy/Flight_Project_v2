from django.test import TestCase
from flights.models import Country,Flight
from accounts.models import Airline, CustomUser, Customer
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import make_password


class TestDataMixin(TestCase):

    @classmethod
    def setUpTestData(self):
        self.now = timezone.now()
        self.later = self.now + timedelta(hours=12)

        self.country = Country.objects.create(name='United States', pic='https://dummyimage.com/600x400/000/fff')
        self.country1 = Country.objects.create(name='Spain', pic='https://dummyimage.com/600x400/000/fff')
        self.country2 = Country.objects.create(name='Brazil', pic='https://dummyimage.com/600x400/000/fff')

        self.user_customer = CustomUser.objects.create(username='testuser1', password='testpassword1',email='testemail1')
        self.customer = Customer.objects.create(user=self.user_customer)

        self.user_airline = CustomUser.objects.create(username='testuser', password='testpassword',email='testemail')
        self.airline = Airline.objects.create(user=self.user_airline,name='airline',country=self.country)
        self.flight = Flight.objects.create(airline=self.airline, departure_time=self.now, landing_time=self.later,tickets=200,origin_country=self.country, destination_country=self.country1)