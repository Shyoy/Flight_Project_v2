from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('homepage/', views.home, name='homepage'),
    path('login/', views.login, name='login'),
]
