import json

import requests
from django.core.cache import cache

from .models import WeatherApiKey

API_KEY = WeatherApiKey.objects.first().api_key

CODE_OK = 200
EXPIRATION_DATE = 3600

# To retrieve and deserialize cached data later
def get_data(key: str) -> dict | None:
    retrieved_data = cache.get(key=key)
    if retrieved_data:
        return retrieved_data
    return None


def get_weather_data(city_name: str) -> dict:
    # Normalize the key to prevent case-sensitive duplicates
    normalized_city_name = city_name.lower().strip()

    # Check if data already exists in cache
    cached_data = get_data(normalized_city_name)
    if cached_data:
        return {"data": cached_data, "error": None}

    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city_name}&days=7&aqi=no&alerts=no"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an exception for non-2xx responses
    except requests.exceptions.RequestException as e:
        return {"data": None, "error": f"Failed to fetch data: {e}"}

    if response.status_code != CODE_OK:
        return {"data": None, "error": f"Failed to fetch data, status code: {response.status_code}"}

    json_data = response.json()

    # Extract location data
    location = {
        "name": json_data["location"]["name"],
        "region": json_data["location"]["region"],
        "country": json_data["location"]["country"],
    }

    # Extract current weather data
    current = {
        "condition": json_data["current"]["condition"],
        "last_updated": json_data["current"]["last_updated"],
        "temp_c": json_data["current"]["temp_c"],
        "humidity": json_data["current"]["humidity"],
        "wind_kph": json_data["current"]["wind_kph"],
        "uv": json_data["current"]["uv"],
    }

    # Extract forecast data using list comprehension
    forecast = [
        {
            "date": day["date"],
            "uv": day["day"]["uv"],
            "maxtemp_c": day["day"]["maxtemp_c"],
            "mintemp_c": day["day"]["mintemp_c"],
            "avgtemp_c": day["day"]["avgtemp_c"],
            "condition": day["day"]["condition"],
            "maxwind_kph": day["day"]["maxwind_kph"],
            "daily_will_it_rain": day["day"]["daily_will_it_rain"],
            "daily_chance_of_rain": day["day"]["daily_chance_of_rain"],
            "daily_will_it_snow": day["day"]["daily_will_it_snow"],
            "daily_chance_of_snow": day["day"]["daily_chance_of_snow"],
            "avghumidity": day["day"]["avghumidity"],
        }
        for day in json_data["forecast"]["forecastday"]
    ]

    # Prepare data for Redis storage
    data = {"location": location, "current": current, "forecast": forecast}
    dump_data = json.dumps(data)

    cache.set(normalized_city_name, dump_data, EXPIRATION_DATE)

    return {"data": dump_data, "error": None}
