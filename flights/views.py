from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView , FormView, ListView
from accounts.forms import CustomerProfileForm
from flights.forms import SearchFlightsForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import urllib.parse
from accounts import models as acc_models
from accounts.mixins import AllowedGroupsTestMixin
from flights.models import Flight

# 

def error_404_view(request, exception=None):
    # make a redirect to homepage
    return redirect('homepage') # or redirect('name-of-index-url')

def home(request):
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
        return context

    def get_form(self):
        """Returns form_class with user customer as instance"""
        return self.form_class(instance=self.request.user.customer, **self.get_form_kwargs())
    
    def form_valid(self, form):
        """This saves the form that creates new customer and returns success_url"""
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        return super(CustomerProfile, self).form_valid(form)


class SearchView(AllowedGroupsTestMixin, FormView):##TODO: implement
    allowed_groups = '__all__'
    model = Flight
    template_name = "customer/search_flights.html"
    form_class = SearchFlightsForm
    paginate_by = 2

    def get(self, request, *args, **kwargs):## TODO add get false request check
        
        # origin_country = request.GET.get('origin_country')
        # destination_country = request.GET.get('destination_country')
        # departure_time = request.GET.get('departure_time')
        q = request.GET
        print('THis is get')
        if q:
            self.results = Flight.objects.filter(origin_country__name__icontains=q['origin_country'],
                                                destination_country__name__icontains=q['destination_country'],
                                            departure_time__contains=q['departure_time']).order_by('-landing_time')
        return super().get(request, *args, **kwargs)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     q = self.request.GET
    #     kwargs['initial'] = q
    #     return kwargs



    def get_context_data(self, **kwargs):
        """Add context to the template"""
        print('THis is get_context_data')
        context = super(SearchView, self).get_context_data(**kwargs)
        q = dict(self.request.GET)
        
        get = '?' + urllib.parse.urlencode(q, doseq=True)
        context['get'] = get
        
        if not get=='?':
            self.paginator = Paginator(self.results,self.paginate_by)
            page_number = q.pop('page', [1])[0]
            page_obj = self.paginator.get_page(page_number)
            # print(f'results: {self.results}')
            context['page_obj']= page_obj
        return context

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        print('get_initial')
        return self.request.GET

# TODO: AirLine views
# TODO: Administrator views
