from unittest import result
from django.forms import ValidationError
from django.test import TestCase, RequestFactory
from django.urls import reverse
from flights.models import Country, Flight
from accounts.models import Airline, CustomUser, Customer, Administrator
from datetime import timedelta
from django.utils import timezone
from accounts.tests.mixins import TestDataMixin

# Create your tests here.


# class CountryTest(TestCase):

#     def test_model_str(self):
#         URL ='https://dummyimage.com/600x400/000/fff'
#         country = Country.objects.create(name='United States', pic=URL)
#         self.assertEqual(str(country), 'United States')


class CustomerTest(TestDataMixin, TestCase):

    def test_valid_customer(self):
        bad_customer = self.customer
        good_customer = Customer(user_id=1,
                                 first_name='Joe',
                                 last_name='Bush',
                                 phone_number='0509876485')

        self.assertTrue(good_customer.valid_customer)
        self.assertFalse(bad_customer.valid_customer)

    def test_model_str(self):
        bad_customer = self.customer
        self.assertEqual(str(bad_customer), 'testemail1')
        
        good_customer = Customer(user_id=1,
                                 first_name='Joe',
                                 last_name='Bush',
                                 phone_number='0509876485')

        self.assertEqual(str(good_customer), 'Joe Bush')

    def test_if_phone_digits_only(self):
        bad_customer = Customer(user_id=1,
                                first_name='Joe',
                                last_name='Bush',
                                phone_number='+56521')

        with self.assertRaisesMessage(
                expected_exception=ValidationError, 
                expected_message='Phone Number must countian only digits !'):
            bad_customer.clean()

    def test_if_first_name_alpha_only(self):
        bad_customer = Customer(user_id=1,
                                first_name='Joe23',
                                last_name='Bush',
                                phone_number='0509876485')

        with self.assertRaisesMessage(
                expected_exception=ValidationError, 
                expected_message='First Name must countian only Letters !'):
            bad_customer.clean()
   
    def test_if_last_name_alpha_only(self):
        bad_customer = Customer(user_id=1,
                                first_name='Joe',
                                last_name='Bush61',
                                phone_number='0509876485')

        with self.assertRaisesMessage(
                expected_exception=ValidationError, 
                expected_message='Last Name must countian only Letters !'):
            bad_customer.clean()


class AirlineTest(TestDataMixin, TestCase):

    def test_model_str(self):
        airline = Airline(user_id=1,
                        name='wizz',
                        country_id=1,)
        self.assertEqual(str(airline) , 'wizz')


class AdministratorTest(TestDataMixin, TestCase):

    def test_model_str(self):
        admin = Administrator(user_id=1,
                        first_name='Joe',
                        last_name='Bush',)
        self.assertEqual(str(admin) , admin.user.username)