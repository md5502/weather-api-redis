from django.db import models

# Create your models here.


class WeatherApiKey(models.Model):
    api_key = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.api_key
