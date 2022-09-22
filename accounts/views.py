from django.shortcuts import render, HttpResponse

from .services import reverse_lazy
# Generic
from django.views.generic import ListView ,DetailView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from . import models

# Create your views here.


def home(request):
    return render(request, 'home.html')


class RegisterForm(FormView):
    template_name = 'accounts/register.html'
    form_class = forms.UserRegisterForm
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # book = form.save(commit=False)
        # book.visitor = self.request.user.visitor
        # book.save()
        print('form is valid')
        return super(RegisterForm, self).form_valid(form)