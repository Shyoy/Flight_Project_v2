
# from django.contrib.auth.models import Group
import accounts.models as acc_models
# Signals:
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.db.models import F, Q


# Workaround for using reverse with success_url in class based generic views
# because direct usage of it throws an exception.
# reverse_lazy = lambda name=None, *args : lazy(reverse, str)(name, args=args)

# def reverse_lazy(name=None, *args):
#     """
#     regular reverse function dont work inside a generic view
#     so this one will work.
#     """
#     return lazy(reverse, str)(name, args=args)


@receiver(m2m_changed, sender='accounts.CustomUser_groups')
def _m2m_user_groups_receiver(action , instance,**kwargs):
    """
    Intercepts user groups change when creating a new user
    and creates a new type of user.
    """

    if action == 'post_add' and instance.groups.count()==1:
        if instance.groups.first().name == 'customers':
            print('creates a user customer')
            # creates a user customer
            acc_models.Customer.objects.create(user=instance)
            print(instance.customer)

        elif instance.groups.first().name == 'airlines':
            # creates a user airline
            acc_models.Airline.objects.create(user=instance , name=instance.username)
            print(instance.airline)

        elif instance.groups.first().name == 'administrators':
            # creates a user administrator
            acc_models.Administrator.objects.create(user=instance)
            print(instance.administrator)
    
