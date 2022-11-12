from re import template
from django.contrib import admin
from django.urls import path
from . import views

# from django.views.generic import TemplateView


urlpatterns = [
    # Flights urlpattern
    path('homepage/', views.homepage, name='homepage'),
    path('', views.home, name='home'),
    # Customer urlpatterns
    path('profile/',views.CustomerProfile.as_view(), name='profile'),
    path('search/',views.SearchView.as_view(), name='search_flights'),
    path('flight_detail/<pk>',views.FlightView.as_view(), name='flight_detail'),


    # Admin urlpatterns
    path('administrator/homepage/', views.AdminHome.as_view(), name='admin_homepage'),
    path('administrator/airlines_manage/', views.AdminAirlinesManage.as_view(), name='airlines_manage'),
]

