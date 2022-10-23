from unittest import result
from django.test import TestCase ,RequestFactory
from django.urls import reverse
from flights.models import Country,Flight
from accounts.models import Airline, CustomUser, Customer
from datetime import timedelta
from django.utils import timezone

# Create your tests here.


class CountryTest(TestCase):

    def test_model_str(self):
        URL ='https://dummyimage.com/600x400/000/fff'
        country = Country.objects.create(name='United States', pic=URL)

        self.assertEqual(str(country), 'United States')


class FlightTest(TestCase):

    @classmethod
    def setUpTestData(self):
        now = timezone.now()
        later = now + timedelta(hours=12)

        self.country = Country.objects.create(name='United States', pic='https://dummyimage.com/600x400/000/fff')
        self.country1 = Country.objects.create(name='Spain', pic='https://dummyimage.com/600x400/000/fff')

        self.user_customer = CustomUser.objects.create(username='testuser1', password='testpassword1',email='testemail1')
        self.customer = Customer.objects.create(user=self.user_customer)

        self.user_airline = CustomUser.objects.create(username='testuser', password='testpassword',email='testemail')
        self.airline = Airline.objects.create(user=self.user_airline,name='airline',country=self.country)
        self.flight = Flight.objects.create(airline=self.airline, departure_time=now, landing_time=later,tickets=200,origin_country=self.country, destination_country=self.country1)

    def test_remaining_tickets(self):
        self.flight.passengers.add(self.customer)
        self.assertEqual(self.flight.remaining_tickets, 199)

    def test_model_str(self):
        result = f'Flight number: 1 - Date: {timezone.now().date()} - Remaining Tickets: {200}'
        self.assertEqual(str(self.flight), result)
