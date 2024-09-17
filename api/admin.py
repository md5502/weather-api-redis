from django.contrib import admin

# Register your models here.
from .models import WeatherApiKey

admin.site.register(WeatherApiKey)
