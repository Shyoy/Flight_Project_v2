from django.shortcuts import render, redirect


# Create your views here.

def error_404_view(request, exception=None):
    # make a redirect to homepage
    return redirect('homepage') # or redirect('name-of-index-url')

def home(request):
    return render(request, 'flights/home.html')

def login(request):
    return render(request, 'flights/login.html')
    