from django.contrib import admin

# Register your models here.
from user.models import AdminProfile, NumberCar

admin.site.register(AdminProfile)
admin.site.register(NumberCar)