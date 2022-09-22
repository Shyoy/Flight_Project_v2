from django.utils.functional import lazy
from django.urls import reverse

# Workaround for using reverse with success_url in class based generic views
# because direct usage of it throws an exception.
# reverse_lazy = lambda name=None, *args : lazy(reverse, str)(name, args=args)

def reverse_lazy(name=None, *args):
    return lazy(reverse, str)(name, args=args)