
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

# urlpatterns = [
#     url(r'^login/$', auth_views.login, name='login'),
#     url(r'^register/$', auth_views.register, name='register'),
#     url(r'^admin/', admin.site.urls),
# ]

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterForm.as_view(), name='register'),
]
