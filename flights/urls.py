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

    #Airline urlpatterns
    path('airline/homepage/', views.AirlineHome.as_view(), name='airline_homepage'),
    path('airline/flights_manager/', views.AirlineFlightsManage.as_view(), name='flights_manager'),
    path('airline/add_flight/', views.AddFlight.as_view(), name='add_flight'),
    path('airline/airline_flight_detail/<pk>', views.AirlineFlightDetail.as_view(), name='airline_flight_detail'),


    # Admin urlpatterns
    path('administrator/homepage/', views.AdminHome.as_view(), name='admin_homepage'),
    path('administrator/airlines_manager/', views.AdminAirlinesManage.as_view(), name='airlines_manager'),
]

