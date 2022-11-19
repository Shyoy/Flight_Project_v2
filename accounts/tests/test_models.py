from unittest import result
from django.forms import ValidationError
from django.test import TestCase ,RequestFactory
from django.urls import reverse
from flights.models import Country,Flight
from accounts.models import Airline, CustomUser, Customer
from datetime import timedelta
from django.utils import timezone
from .mixins import TestDataMixin

# Create your tests here.


# class CountryTest(TestCase):

#     def test_model_str(self):
#         URL ='https://dummyimage.com/600x400/000/fff'
#         country = Country.objects.create(name='United States', pic=URL)
#         self.assertEqual(str(country), 'United States')


class CustomerTest(TestDataMixin,TestCase):

    def test_valid_customer(self):
        bad_customer =self.customer.valid_customer
        self.customer.first_name = 'Joe'
        self.customer.last_name = 'Bush'
        self.customer.phone_number = '0509876485'
        good_customer = self.customer.valid_customer
        
        self.assertTrue(good_customer)
        self.assertFalse(bad_customer)

    
    def test_model_str(self):
        bad_customer =self.customer
        self.assertEqual(bad_customer.user.email ,'testemail1' )
        bad_customer.first_name = 'Joe'
        bad_customer.last_name = 'Bush'
        bad_customer.phone_number = '0509876485'
        good_customer = bad_customer
        self.assertEqual(good_customer.first_name + " " + good_customer.last_name ,'Joe Bush')


    def test_if_phone_digits_only(self):##TODO: implement Here TEster
        # airline country not in bad_flight
        bad_flight = self.flight
        bad_flight.origin_country = self.country2
        bad_flight.destination_country = self.country1
        
        with self.assertRaisesMessage(
                expected_exception=ValidationError,
                expected_message='Phone Number must countian only digits !'):
            bad_flight.clean()

    # def test_same_countries_flight(self):
    #     bad_flight = self.flight
    #     bad_flight.origin_country = self.country
    #     bad_flight.destination_country = self.country
    #     with self.assertRaisesMessage(
    #             expected_exception=ValidationError,
    #             expected_message=f'Origin Country and Destination Country can\'t be the same !'):
    #         bad_flight.clean()
       
    # def test_flight_size(self):
    #     bad_flight = self.flight
    #     bad_flight.tickets = 45
    #     with self.assertRaisesMessage(
    #                 expected_exception=ValidationError,
    #                 expected_message=f'Flight size must be greater than 50 !'):
    #         bad_flight.clean()

    # def test_landing_after_depart(self):
    #     bad_flight = self.flight
    #     bad_flight.landing_time = self.now
    #     bad_flight.departure_time = self.later
    #     with self.assertRaisesMessage(
    #                 expected_exception=ValidationError,
    #                 expected_message=f'Landing time must be after departure time !'):
    #         bad_flight.clean()