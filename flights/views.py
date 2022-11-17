# Python related
import urllib.parse
# Time
from datetime import timedelta

from django.contrib import messages
from django.core.paginator import Paginator
# django Tools
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, FormView, ListView, TemplateView

from accounts import models as acc_models
# Forms and Models
from accounts.forms import AddAirline, CustomerProfileForm, UserRegisterForm
# Custom Mixins and functions
from accounts.mixins import AllowedGroupsTestMixin
from flights.forms import (AddFlightForm, AirlineSearchFlightsForm,
                           SearchAirlineForm, SearchFlightsForm)
from flights.models import Flight


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

class CustomerProfile(AllowedGroupsTestMixin, FormView):  # TODO Page not Fully done yet
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
                                                 departure_time__gt=timezone.now()).order_by('departure_time')
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

        print('self.object.departure_time: ', self.object.departure_time)
        print('timezone.now: ', timezone.now())
        print(hours_till_flight)
        print(SAFETY_HOURS)
        context['needs_confirm'] = hours_till_flight < SAFETY_HOURS

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


# TODO: AirLine views

class AirlineHome(AllowedGroupsTestMixin, TemplateView):  # TODO implement Home
    allowed_groups = ['airlines']
    template_name = 'airline/airline_homepage.html'


class AirlineFlightsManage(AllowedGroupsTestMixin, ListView):  # TODO Update in or out ?

    allowed_groups = ['airlines']
    model = Flight
    template_name = 'airline/flights_manager.html'
    form_class = AirlineSearchFlightsForm
    paginate_by = 10

    def get_context_data(self, **kwargs):
        self.object_list = self.object_list.filter(
            airline=self.request.user.airline)
        form = self.form_class(
            self.request.session.get('flights_manager_POST'))
        if form.data:
            # Get fields from form data
            departure_time = form.data.get('departure_time')
            origin_country = form.data.get('origin_country')
            destination_country = form.data.get('destination_country')
            # Filters
            q = self.object_list
            q = q.filter(
                departure_time__icontains=departure_time) if departure_time else q
            q = q.filter(
                origin_country__id=origin_country) if origin_country else q
            q = q.filter(
                destination_country__id=destination_country) if destination_country else q
            self.object_list = q

        # print(self.queryset)
        context = super().get_context_data(object_list=self.object_list, **kwargs)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        # for Delete form
        delete_id = request.POST.get('delete', None)
        if delete_id:
            flight = self.model.objects.get(id=delete_id)
            if flight.passengers.all():
                messages.add_message(
                    request, messages.WARNING, f'You can\'t delete Flight that already has passengers')
            else:
                flight_id = flight.id
                flight.delete()
                messages.add_message(
                    request, messages.WARNING, f'Flight {flight_id} deleted successfully')
            return redirect('flights_manager')

        # For AirlineSearchFlightsForm
        form = self.form_class(request.POST)
        if form.is_valid():
            request.session['flights_manager_POST'] = form.data

        return redirect('flights_manager')


class AddFlight(AllowedGroupsTestMixin, FormView):

    allowed_groups = ['airlines']
    template_name = 'airline/add_flight.html'
    form_class = AddFlightForm
    success_url = reverse_lazy('flights_manager')



    def form_valid(self, form):
        """This saves the form that creates new customer and returns success_url"""
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        flight = form.save(commit=False)
        flight.airline = self.request.user.airline
        new_flight = flight.save()
        print('valid form')
        print(form.cleaned_data)
        print(new_flight)
        print()
       
        return super(AddFlight, self).form_valid(form)

    def form_invalid(self, form):

        print('invalid form !!!!')
        return self.render_to_response(self.get_context_data(form=form))
    # def form_valid(self, request, form,*args, **kwargs):
    #     print(form.cleaned_data)
    #     return redirect('add_flight')

    # def post(self, request, *args, **kwargs):
        
    #     print(request.POST)
    #     return redirect('add_flight')


class AirlineFlightDetail(AllowedGroupsTestMixin, DetailView, ListView):  # TODO: Email Booking Confirmed
    allowed_groups = ['airlines']
    template_name = 'airline/airline_flight_detail.html'
    model = Flight
    form_class = CustomerProfileForm
    # success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        self.object_list = self.object.passengers.all().order_by('first_name', 'last_name')
        print(self.object)
        print(self.object_list)
        # print(self.object_list)
        # form = self.form_class(
        #     self.request.session.get('airlines_manager_POST'))
        # if form.data:
        #     name = form.data.get('name')
        #     country_id = form.data.get('country')

        #     q = self.object_list
        #     q = self.object_list.filter(name__icontains=name) if name else q
        #     q = q.filter(country__id=country_id) if country_id else q
        #     self.object_list = q

        context = super(AirlineFlightDetail,self).get_context_data( **kwargs)
        # context['form'] = form
        return context

    def post(self, request, *args, **kwargs):

        flight = self.get_object()
        remove_id = request.POST.get('remove', None)
        if remove_id:
            customer = flight.passengers.get(id=remove_id)
            # flight.passengers.remove(customer)
            print(flight.passengers.all())
            messages.add_message(
                    request, messages.WARNING, f'{customer.first_name} {customer.last_name} removed from flight {flight.id} successfully')
            # return redirect('airlines_manager')
        return super(AirlineFlightDetail, self).get(request, *args, **kwargs)


# TODO: Administrator views

class AdminHome(AllowedGroupsTestMixin, TemplateView):  # TODO implement Home
    allowed_groups = ['administrators']
    template_name = 'administrator/administrator_homepage.html'
    

class AdminAirlinesManage(AllowedGroupsTestMixin, ListView):  # TODO Update in or out ?
    allowed_groups = ['administrators']
    model = acc_models.Airline
    template_name = "administrator/airlines_manager.html"
    form_class = SearchAirlineForm
    paginate_by = 2

    def get_context_data(self, **kwargs):
        form = self.form_class(
            self.request.session.get('airlines_manager_POST'))
        if form.data:
            name = form.data.get('name')
            country_id = form.data.get('country')

            q = self.object_list
            q = self.object_list.filter(name__icontains=name) if name else q
            q = q.filter(country__id=country_id) if country_id else q
            self.object_list = q

        context = super().get_context_data(object_list=self.object_list, **kwargs)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        # for Delete form
        delete_id = request.POST.get('delete', None)
        if delete_id:
            airline = self.model.objects.get(id=delete_id)
            if airline.flights.all():
                messages.add_message(
                    request, messages.WARNING, f'You can\'t delete airline with working flights')
            else:
                airline_name = airline.name
                airline.user.delete()
                messages.add_message(
                    request, messages.WARNING, f'{airline_name} Airline deleted successfully')
            return redirect('airlines_manager')
        # For SearchAirlineForm
        form = self.form_class(request.POST)
        if form.is_valid():
            request.session['airlines_manager_POST'] = form.data

        return redirect('airlines_manager')
