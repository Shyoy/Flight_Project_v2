
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

    #Superuser
    path('administrator/register/', views.AdminRegister.as_view(), name='admin_register'),
    path('administrator/admin_profile/', views.AdminProfile.as_view(), name='admin_profile'),

    # Admin urlpatterns
    path('administrator/airline_register', views.AirlineRegister.as_view(), name='airline_register'),
    path('administrator/airline_update/<pk>', views.AirlineDetailUpdate.as_view(), name='airline_update'),
]
