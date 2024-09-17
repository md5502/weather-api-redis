import json

from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .utils import get_weather_data


class WeatherSearch(APIView):


    def get(self, request, city_name):
        data = get_weather_data(city_name)
        if data["data"]:
            data = json.loads(data["data"])

            return Response(data)
        return Response(data["error"])

