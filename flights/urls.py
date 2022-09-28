from re import template
from django.contrib import admin
from django.urls import path
from . import views
# from django.views.generic import TemplateView

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('', views.home, name='home'),
    path('profile/',views.CustomerProfile.as_view(), name='profile'),
    # path('login/', views.login, name='login'),
]
