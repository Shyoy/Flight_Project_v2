
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin, AccessMixin
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django import forms as dj_forms

from accounts.forms import AddAirline, CustomerProfileForm, UserRegisterForm
from flights.forms import SearchFlightsForm, SearchAirlineForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib import messages

import urllib.parse
from accounts import models as acc_models
from accounts.mixins import AllowedGroupsTestMixin
from flights.models import Flight
from django.forms import inlineformset_factory

#
def error_403_view(request, exception=None):
    # make a redirect to homepage
    # messages.add_message(request, messages.ERROR,
    #                              'This is a 403 Forbidden')

    return redirect('home')  # or redirect('name-of-index-url')

def error_404_view(request, exception=None):
    # make a redirect to homepage
    return redirect('home')  # or redirect('name-of-index-url')


def home(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.user.groups.first().name == 'administrators':
            return redirect('admin_homepage')

        elif request.user.groups.first().name == 'airlines':
            return redirect('airline_homepage')
    
    return redirect('homepage')


def homepage(request):
    return render(request, 'flights/homepage.html')



# TODO: Customer views

class CustomerProfile(AllowedGroupsTestMixin, FormView):
    allowed_groups = ['customers']
    template_name = 'customer/profile.html'
    form_class = CustomerProfileForm
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        """Adds customer details to the context"""
        context = super(CustomerProfile, self).get_context_data(**kwargs)
        context['customer'] = self.request.user.customer.__dict__

        context['flight_history'] = self.request.user.customer.flights.filter(
            departure_time__lte=timezone.now()).order_by('departure_time')
        context['current_flights'] = self.request.user.customer.flights.filter(
            departure_time__gt=timezone.now()).order_by('departure_time')
        return context

    def get_form(self):
        """Returns form_class with user customer as instance"""
        return self.form_class(instance=self.request.user.customer, **self.get_form_kwargs())

    def form_valid(self, form):
        """This saves the form that creates new customer and returns success_url"""
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        next = self.request.GET.get('next')
        if next:
            url, page_id = next.split('/')[1:]
            if self.request.user.customer.valid_customer:
                return redirect(url, pk=page_id)
            path_next = self.request.path+'?next='+next
            return redirect(path_next)
        return super(CustomerProfile, self).form_valid(form)


class SearchView(AllowedGroupsTestMixin, FormView):
    allowed_groups = '__all__'
    model = Flight
    template_name = "customer/search_flights.html"
    form_class = SearchFlightsForm
    paginate_by = 20

    def get(self, request, *args, **kwargs):  
        q = request.GET
        origin_country = q.get('origin_country')
        destination_country = q.get('destination_country')
        departure_time = q.get('departure_time')

        # Check if valid GET request
        is_q = all([isinstance(x, str)
                   for x in [origin_country, destination_country, departure_time]])
        if not (len(q) == 0 or (is_q and len(q) == 3) or (is_q and q['page'] and len(q) == 4)):
            return redirect('search_flights')
        if is_q:
            self.results = Flight.objects.filter(origin_country__name__icontains=origin_country,
                                                 destination_country__name__icontains=destination_country,
                                                 departure_time__contains=departure_time,
                                                 departure_time__gt= timezone.now()).order_by('departure_time')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add context to the template"""
        print('THis is get_context_data')
        context = super(SearchView, self).get_context_data(**kwargs)
        q = dict(self.request.GET)

        if q:
            self.paginator = Paginator(self.results, self.paginate_by)
            page_number = q.pop('page', [1])[0]
            page_obj = self.paginator.get_page(page_number)
            # print(f'results: {self.results}')
            get = '?' + urllib.parse.urlencode(q, doseq=True)
            context['page_obj'] = page_obj
            context['get'] = get
        return context

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        print('get_initial')
        return self.request.GET


class FlightView(AllowedGroupsTestMixin, DetailView):  # TODO: Email Booking Confirmed
    allowed_groups = ['customers']
    template_name = 'customer/flight_detail.html'
    model = Flight
    success_url = reverse_lazy('profile')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        SAFETY_HOURS = timedelta(hours=12)
        # only check the hour not by the date    .seconds/60/60                                                
        hours_till_flight = (self.object.departure_time - timezone.now())
        
        print('self.object.departure_time: ' ,self.object.departure_time)
        print('timezone.now: ',timezone.now())
        print(hours_till_flight)
        print(SAFETY_HOURS)
        context['needs_confirm'] =  hours_till_flight < SAFETY_HOURS

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

       
        print('this is post')
        book = self.request.POST.get('book', False)
        if book:
            if request.user.customer.valid_customer:
                if self.object in request.user.customer.flights.all():
                    messages.add_message(request, messages.INFO,
                                    'You Already Booked This Flight')
                    return redirect(self.success_url)
                request.user.customer.flights.add(self.object)
                print('Booking Confirmed')
                messages.add_message(request, messages.SUCCESS,
                                    'Booking saved successfully.')
                return redirect(self.success_url)
            else:
                messages.add_message(
                    request, messages.INFO, 'You need to fill out your profile before booking.')
                go_to_url = reverse_lazy('profile')
                previews = '?next='+request.get_full_path()
                return redirect(go_to_url+previews)

        # return self.render_to_response(context)


# TODO: AirLine views

class AirlineHome(AllowedGroupsTestMixin, TemplateView):##TODO implement Home
    allowed_groups = ['airlines']
    template_name = 'airline/airline_homepage.html'
    

class AirlineFlightsManage(AllowedGroupsTestMixin,ListView):##TODO Update in or out ?
    class Form(dj_forms.ModelForm):
        class Meta:
            model = Flight
            fields  = ('departure_time','origin_country','destination_country',)
        departure_time = dj_forms.DateField(label='Departure Time', widget=dj_forms.DateInput(attrs={'type':'date'}),required = False)
        def __init__(self, *args, **kwargs):
            super(AirlineFlightsManage.Form, self).__init__(*args, **kwargs)
            # self.fields['departure_time'].widget =dj_forms.DateInput(attrs={'type':'date'})
            for fieldname in self.fields.keys(): 
                self.fields[fieldname].widget.attrs.update({'class':'form-control','style':'position: absolute; z-index: 2; max-width:180px;'})
                self.fields[fieldname].required = False
                self.fields[fieldname].label += ":"
            # self.fields['departure_time'].widget = dj_forms.DateInput(format='%d-%m-%Y')

    allowed_groups = ['airlines']
    model = Flight
    template_name = 'airline/flights_manager.html'
    form_class = Form
    paginate_by = 10

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset() 
        self.object_list = self.object_list.filter(airline=self.request.user.airline)
        context = super().get_context_data(object_list= self.object_list,**kwargs)
        # print(self.request.user.airline )
        # print(Flight.objects.filter(airline=self.request.user.airline))
        print('This is get_context_data')
        print(context)
        form = self.form_class()
        context['form'] = form
        return context

    def post(self,request, *args, **kwargs):
        print('this is POST')
        # self.object_list = self.get_queryset()
        # context = self.get_context_data(object_list=self.object_list)
        # # for Delete form
        # delete_id = request.POST.get('delete', None)
        # if delete_id:
        #     airline = acc_models.Airline.objects.get(id=delete_id)
        #     if airline.flights.all():
        #         messages.add_message(
        #         request, messages.WARNING, f'{airline.name} You can\'t delete airline with working flights')
        #         return redirect('airlines_manager')

            
        #     print(airline , "Deleted")
        #     messages.add_message(
        #         request, messages.WARNING, f'{airline.name} Airline deleted successfully')
        #     return redirect('airlines_manager')

            
        # for SearchFlight form
        form= self.form_class(self.request.POST)
        
        departure_time = form.data['departure_time']
        origin_country = form.data['origin_country']
        destination_country = form.data['destination_country']

        print(departure_time, origin_country, destination_country)
        q = self.model.objects.filter(departure_time__icontains=departure_time)

        q = q.filter(departure_time__icontains=departure_time) if departure_time else q
        q = q.filter(origin_country__id=origin_country) if origin_country else q
        q = q.filter(destination_country__id=destination_country) if destination_country else q
        # print(context)
        # self.object_list
        # self.object_list = self.get_context_data()
        
        
        self.queryset  = q
        
        return super().get(request, *args, **kwargs)






class AddFlight(AllowedGroupsTestMixin, FormView):
                
    allowed_groups =['airlines']
    template_name = 'airline/add_flight.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('admin_register')

    





# TODO: Administrator views

class AdminHome(AllowedGroupsTestMixin, TemplateView):##TODO implement Home
    allowed_groups = ['administrators']
    template_name = 'administrator/administrator_homepage.html'



class AdminAirlinesManage(AllowedGroupsTestMixin,ListView):##TODO Update in or out ?
    allowed_groups = ['administrators']
    model = acc_models.Airline
    template_name = "administrator/airlines_manager.html"
    form_class = SearchAirlineForm
    paginate_by = 2


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('This is get_context_data')
        form = self.form_class()
        context['form'] = form
        return context

    def post(self,request, *args, **kwargs):
        print('this is POST')
        # for Delete form
        delete_id = request.POST.get('delete', None)
        if delete_id:
            airline = acc_models.Airline.objects.get(id=delete_id)
            if airline.flights.all():
                messages.add_message(
                request, messages.WARNING, f'{airline.name} You can\'t delete airline with working flights')
                return redirect('airlines_manager')
            airline.user.delete()
            print(airline , "Deleted")
            messages.add_message(
                request, messages.WARNING, f'{airline.name} Airline deleted successfully')
            return redirect('airlines_manager')

        # for SearchAirline form
        form= self.form_class(self.request.POST)
        
        name = form.data['name']
        country_id = form.data['country']
        print('name:' ,name)
        print('country:', country_id)
        q = acc_models.Airline.objects.filter(name__icontains=name)
        self.queryset = q.filter(country__id=country_id) if country_id else q
        
        return super().get(request, *args, **kwargs)


