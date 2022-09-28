from django.shortcuts import render, redirect
from django.views.generic import TemplateView



# 

def error_404_view(request, exception=None):
    # make a redirect to homepage
    return redirect('homepage') # or redirect('name-of-index-url')

def home(request):
    return redirect('homepage')

def homepage(request):
    return render(request, 'flights/homepage.html')


# TODO: Customer views
class CustomerProfile(TemplateView):
    template_name="customer/profile.html"
    def get(self, request, *args, **kwargs):
        context = self.request.user.customer.__dict__
        return self.render_to_response(context)

    pass




# TODO: AirLine views
# TODO: Administrator views
