from django.utils import timezone
from django.contrib.auth.mixins import PermissionRequiredMixin, AccessMixin
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView, FormView, ListView, DetailView
from accounts import forms
from accounts.forms import AddAirline, CustomerProfileForm
from flights.forms import SearchFlightsForm
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
            return redirect('airline-homepage')
    
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
        print('this is context')
        context = super(CustomerProfile, self).get_context_data(**kwargs)
        context['customer'] = self.request.user.customer.__dict__

        context['flight_history'] = self.request.user.customer.flights.filter(
            departure_time__lte=timezone.now()).order_by('-departure_time')
        context['current_flights'] = self.request.user.customer.flights.filter(
            departure_time__gt=timezone.now()).order_by('-departure_time')
        return context

    def get_form(self):
        """Returns form_class with user customer as instance"""
        return self.form_class(instance=self.request.user.customer, **self.get_form_kwargs())

    def form_valid(self, form):
        """This saves the form that creates new customer and returns success_url"""
        print('this is form_valid')
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # context = self.get_context_data(object=self.object)

        go_to_url = reverse_lazy('profile')
        previews = '?next='+request.get_full_path()
        print('this is post')

        if request.user.customer.valid_customer:
            request.user.customer.flights.add(self.object)
            print('Booking Confirmed')
            messages.add_message(request, messages.SUCCESS,
                                 'Booking saved successfully.')
            return redirect(self.success_url)
        else:
            messages.add_message(
                request, messages.INFO, 'You need to fill out your profile before booking.')
            return redirect(go_to_url+previews)

        # return self.render_to_response(context)


# TODO: AirLine views



# TODO: Administrator views

class AdminHome(AllowedGroupsTestMixin, TemplateView):
    allowed_groups = ['administrators']
    template_name = 'administrator/administrator_homepage.html'




class AdminAirlinesManage(AllowedGroupsTestMixin,ListView):
    allowed_groups = ['administrators']
    model = acc_models.Airline
    template_name = "administrator/airlines_manage.html"
    
    paginate_by = 1

    # def get(self, request, *args, **kwargs):  
    #     q = request.GET
    #     origin_country = q.get('origin_country')
    #     destination_country = q.get('destination_country')
    #     departure_time = q.get('departure_time')

    #     # Check if valid GET request
    #     is_q = all([isinstance(x, str)
    #                for x in [origin_country, destination_country, departure_time]])
    #     if not (len(q) == 0 or (is_q and len(q) == 3) or (is_q and q['page'] and len(q) == 4)):
    #         return redirect('search_flights')
    #     if is_q:
    #         self.results = Flight.objects.filter(origin_country__name__icontains=origin_country,
    #                                              destination_country__name__icontains=destination_country,
    #                                              departure_time__contains=departure_time,
    #                                              departure_time__gt= timezone.now()).order_by('departure_time')
    #     return super().get(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        print('this is POST')
        print(request.POST)
        return super().post(request, *args, **kwargs)

        # inlineformset_factory
    
    def get_context_data(self, **kwargs):
        """Add context to the template"""
        print('THis is get_context_data')
        context = super(AdminAirlinesManage, self).get_context_data(**kwargs)
        # q = dict(self.request.GET)
        print(context['object_list'])
        # if q:
        #     self.paginator = Paginator(self.results, self.paginate_by)
        #     page_number = q.pop('page', [1])[0]
        #     page_obj = self.paginator.get_page(page_number)
        #     # print(f'results: {self.results}')
        #     get = '?' + urllib.parse.urlencode(q, doseq=True)
        #     context['page_obj'] = page_obj
        #     context['get'] = get
        return context

    # def get_initial(self):
    #     """Return the initial data to use for forms on this view."""
    #     print('get_initial')
    #     return self.request.GET