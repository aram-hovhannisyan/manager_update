from django.contrib import admin
from .models import User
from storage.models import Non_Working_Days

# Register your models here.
admin.site.register(User)
admin.site.register(Non_Working_Days)