from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.contrib.auth.models import Group


class GroupTestMixin(LoginRequiredMixin,UserPassesTestMixin):

     def test_func(self):
        # raise NotImplementedError(
        #     "{} is missing the implementation of the test_func() method.".format(
        #         self.__class__.__name__
        #     )
        # )
        return self.request.user.username == 'shay'
