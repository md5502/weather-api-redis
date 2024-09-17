
# Weather API Wrapper Service

## Overview
This project is a weather API wrapper that integrates with a third-party weather service ([WeatherAPI](https://www.weatherapi.com/)) to fetch real-time weather data. It uses Django with Django Rest Framework (DRF) for handling API requests and Redis for caching the weather data, improving performance by avoiding redundant API calls.

## Features
- Fetch current weather data and a 7-day forecast for any city using [WeatherAPI](https://www.weatherapi.com/).
- Caching of weather data using Redis to optimize repeated requests.
- API endpoint for searching weather by city name.
- Error handling for failed requests and non-2xx HTTP responses.
- Configurable cache expiration time (currently set to 1 hour).

## Project Structure

```
├── api
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
├── db.sqlite3
├── docker-compose.yml
├── manage.py
└── README.md
```

## Installation

### 1. Clone the repository:

   ```bash
   git clone https://github.com/md5502/weather-api-redis.git
   ```

### 2. Set up a virtual environment:

   If you haven't installed `virtualenv` yet, you can install it using:

   ```bash
   pip install virtualenv
   ```

   Create a virtual environment in the project directory:

   ```bash
   virtualenv venv
   ```

   Activate the virtual environment:

   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

### 3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### 4. Set up environment variables:

#### Obtaining the API Key

1. Visit [WeatherAPI](https://www.weatherapi.com/).
2. Sign up for a free account and generate an API key.
3. You will use this key to fetch weather data in the application.

### 5. Add API Key to the Database

To store your API key in the database, follow these steps:

1. Open your Django admin panel (after running migrations and creating a superuser).
2. Navigate to the `WeatherApiKey` model in the admin panel.
3. Add a new entry by pasting the API key you obtained from WeatherAPI.

Alternatively, you can create the API key directly using Django's `shell`:

```bash
python manage.py shell
```

In the shell:

```python
from api.models import WeatherApiKey

# Replace 'your_api_key_here' with your actual WeatherAPI key
WeatherApiKey.objects.create(api_key='your_api_key_here')
```


### 6. Run migrations:

   ```bash
   python manage.py migrate
   ```

### 7. Start the development server:

   ```bash
   python manage.py runserver
   ```

### 8. (Optional) If using Docker, run:

   ```bash
   docker compose -f docker-compose.yml up -d
   ```

## Usage

You can retrieve the weather data by making a GET request to the API endpoint with the city name:

Example:
```bash
GET http://localhost:8000/api/weather/london/
```

This will return the current weather and a 7-day forecast for London.

### Example Response:
```json
{
  "location": {
    "name": "London",
    "region": "City of London, Greater London",
    "country": "United Kingdom"
  },
  "current": {
    "condition": {
      "text": "Partly cloudy"
    },
    "last_updated": "2024-09-17 14:00",
    "temp_c": 18.5,
    "humidity": 65,
    "wind_kph": 13.0,
    "uv": 5.0
  },
  "forecast": [
    {
      "date": "2024-09-18",
      "maxtemp_c": 22.0,
      "mintemp_c": 15.0,
      "avgtemp_c": 18.5,
      "condition": {
        "text": "Sunny"
      },
      "maxwind_kph": 15.0,
      "daily_will_it_rain": 0,
      "daily_chance_of_rain": 0,
      "avghumidity": 65
    },
    ...
  ]
}
```

## Technologies Used

- **Django**: Web framework.
- **Django Rest Framework (DRF)**: For building REST APIs.
- **Redis**: In-memory data store for caching.
- **WeatherAPI**: Third-party weather service API.
- **Docker**: Containerization for easy setup.

## Contributions
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/md5502/weather-api-wrapper/issues).

## License
This project is licensed under the MIT License.

## Author
GitHub: [md5502](https://github.com/md5502)
