from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CustomUser)
admin.site.register(models.Customer)
admin.site.register(models.Airline)
admin.site.register(models.Administrator)