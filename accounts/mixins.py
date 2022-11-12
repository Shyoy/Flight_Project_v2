from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages

class AllowedGroupsTestMixin(LoginRequiredMixin,UserPassesTestMixin):
    allowed_groups = ['*']
    def test_func(self):
        user = self.request.user
        if 'superuser' in self.allowed_groups:
            if not user.is_superuser:
                messages.add_message(self.request, messages.ERROR,
                                 'ERROR 403:\tOnly superusers are allowed to use this page.')
                return False
            return user.is_superuser

        if '*' in self.allowed_groups or self.allowed_groups == '__all__':
            return True

        if not user.is_superuser and user.groups.first().name in self.allowed_groups:
            return True
        elif user.is_superuser or not user.groups.first().name in self.allowed_groups:
            messages.add_message(self.request, messages.ERROR,
                                 f'ERROR 403:\tYou should be in {self.allowed_groups[0]} to view this page !')
            return False
        # return  user.is_superuser or user.groups.first().name in self.allowed_groups
