from unittest import result
from django.forms import ValidationError
from django.test import TestCase ,RequestFactory
from django.urls import reverse
from flights.models import Country,Flight
from accounts.models import Airline, CustomUser, Customer
from datetime import timedelta
from django.utils import timezone
from flights.tests.mixins import TestDataMixin

# Create your tests here.


class CountryTest(TestCase):

    def test_model_str(self):
        URL ='https://dummyimage.com/600x400/000/fff'
        country = Country.objects.create(name='United States', pic=URL)
        self.assertEqual(str(country), 'United States')


class FlightTest(TestDataMixin,TestCase):

    def test_remaining_tickets(self):
        self.flight.passengers.add(self.customer)
        self.assertEqual(self.flight.remaining_tickets, 199)

    def test_model_str(self):
        result = f'On: {self.now.ctime()}--From: {self.country}--To: {self.country1}'
        self.assertEqual(str(self.flight), result)

    def test_flight_duration(self):
        fly_12_hours = self.later - self.now
        self.assertEqual(self.flight.flight_duration, fly_12_hours)

    def test_airline_country_in_flight(self):
        # airline country not in bad_flight
        bad_flight = self.flight
        bad_flight.origin_country = self.country2
        bad_flight.destination_country = self.country1
        
        with self.assertRaisesMessage(
                expected_exception=ValidationError,
                expected_message=f'This Flight Must depart from, or land at {self.airline.country} !'):
            bad_flight.clean()

    def test_same_countries_flight(self):
        bad_flight = self.flight
        bad_flight.origin_country = self.country
        bad_flight.destination_country = self.country
        with self.assertRaisesMessage(
                expected_exception=ValidationError,
                expected_message=f'Origin Country and Destination Country can\'t be the same !'):
            bad_flight.clean()
       
    def test_flight_size(self):
        bad_flight = self.flight
        bad_flight.tickets = 45
        with self.assertRaisesMessage(
                    expected_exception=ValidationError,
                    expected_message=f'Flight size must be greater than 50 !'):
            bad_flight.clean()

    def test_landing_after_depart(self):
        bad_flight = self.flight
        bad_flight.landing_time = self.now
        bad_flight.departure_time = self.later
        with self.assertRaisesMessage(
                    expected_exception=ValidationError,
                    expected_message=f'Landing time must be after departure time !'):
            bad_flight.clean()

    def test_flight_duration(self):
        bad_flight = self.flight
        bad_flight.departure_time = self.now 
        bad_flight.landing_time = self.now + timedelta(minutes=59)
        with self.assertRaisesMessage(
                    expected_exception=ValidationError,
                    expected_message=f'Flight duration can\'t be less then 1 hour !'):
            bad_flight.clean()