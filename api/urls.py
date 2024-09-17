from django.urls import path

from .views import WeatherSearch

app_name = "api"

urlpatterns = [
    path("<str:city_name>/", WeatherSearch.as_view(), name="weather_search"),
]
