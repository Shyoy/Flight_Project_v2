
from django.shortcuts import render, redirect
from django.views.generic import TemplateView , FormView, ListView
from accounts.forms import CustomerProfileForm
from flights.forms import SearchFlightsForm
from django.urls import reverse_lazy
from accounts import models as acc_models
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

class CustomerProfile(FormView):
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


class SearchView(FormView):##TODO: implement
    model = Flight
    template_name = "customer/search_flights.html"
    form_class = SearchFlightsForm
    # success_url = reverse_lazy('search_flights')
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        q = request.GET
        if q:
            self.results = Flight.objects.filter(origin_country__name__icontains=q['origin_country'],
                                                destination_country__name__icontains=q['destination_country'],
                                            departure_time__contains=q['departure_time']).order_by('-landing_time')
        return super().get(request, *args, **kwargs)

    # def get_form(self):
    #     """Returns form_class with user customer as instance"""
    #     q = self.request.GET
    #     print(q)
    #     return self.form_class( **self.get_form_kwargs())
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        q = self.request.GET
        kwargs['initial'] = q
        return kwargs

    # def form_valid(self, form):
    #     """This saves the form that creates new customer and returns success_url"""
    #     q = self.request.GET
    #     print(q)
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     super(CustomerProfile, self).form_valid(form)
    

    def get_context_data(self, **kwargs):
        """Add context to the template"""
        context = super(SearchView, self).get_context_data(**kwargs)
        # context['customer'] = self.request.user.customer.__dict__
        # return context
        q = self.request.GET
        if not q:
            context['q']= True
            return context
        # print(f'results: {self.results}')
        context['results']= self.results
        return context


# TODO: AirLine views
# TODO: Administrator views
