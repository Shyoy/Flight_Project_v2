from django.test import TestCase
from flights.models import Country,Flight
from accounts.models import Administrator, Airline, CustomUser, Customer
from django.contrib.auth.models import Group
from datetime import timedelta
from django.utils import timezone


class TestDataMixin(TestCase):

    @classmethod
    def setUpTestData(self):
        self.now = timezone.now()
        self.later = self.now + timedelta(hours=12)
        # superuser
        self.super_user = CustomUser.objects.create_superuser(username='super',email='super@email.com')
        self.super_user.set_password('testsuperuser2')
        self.super_user.save()

        self.country = Country.objects.create(name='United States', pic='https://dummyimage.com/600x400/000/fff')
        self.country1 = Country.objects.create(name='Spain', pic='https://dummyimage.com/600x400/000/fff')
        self.country2 = Country.objects.create(name='Brazil', pic='https://dummyimage.com/600x400/000/fff')
        #  create customer account
        self.customers_group = Group.objects.create(name='customers')
        self.user_customer = CustomUser.objects.create(username='testuser1',email='testemail1')
        self.user_customer.set_password('testpassword1')
        self.user_customer.save()
        new_customer_user = CustomUser.objects.get(username='testuser1')
        new_customer_user.groups.add(self.customers_group)

        self.customer = Customer.objects.get(user=new_customer_user)

        #  create admin account
        self.admin_group = Group.objects.create(name='administrators')
        self.user_admin = CustomUser.objects.create(username='testadmin',email='testadmin@email.com')
        self.user_admin.set_password('adminpassword1')
        self.user_admin.save()
        new_admin_user = CustomUser.objects.get(username='testadmin')
        new_admin_user.groups.add(self.admin_group)
       

        # self.admin = Administrator.objects.get(user=new_admin_user)
        # print(self.admin)
        self.user_airline = CustomUser.objects.create(username='testuser', password='testpassword',email='testemail')
        self.airline = Airline.objects.create(user=self.user_airline,name='airline',country=self.country)
        self.flight = Flight.objects.create(airline=self.airline, departure_time=self.now, landing_time=self.later,tickets=200,origin_country=self.country, destination_country=self.country1)