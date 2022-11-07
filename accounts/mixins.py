from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.contrib.auth.models import Group


class AllowedGroupsTestMixin(LoginRequiredMixin,UserPassesTestMixin):
    allowed_groups = []
    def test_func(self):
        if '*' in self.allowed_groups or self.allowed_groups == '__all__':
            return True
        user = self.request.user
        # in_groups = self.request.user.groups.first().name in self.allowed_groups
        # print(self.allowed_groups)
        # print(self.request.user.groups.all())
        return  user.is_superuser or user.groups.first().name in self.allowed_groups
