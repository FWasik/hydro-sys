from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class HydroponicSystem(models.Model):
    types = [
        ("NFT", "Nutrient Film Technique"),
        ("DWC", "Deep Water Culture"),
        ("Ebb and Flow", "Ebb and Flow"),
        ("Aeroponics", "Aeroponics"),
        ("Drip", "Drip System"),
        ("Wick", "Wick System"),
    ]

    name = models.CharField(max_length=125, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="systems")
    type = models.CharField(max_length=50, choices=types)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    system = models.ForeignKey(
        HydroponicSystem, on_delete=models.CASCADE, related_name="measurements"
    )
    ph = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(14)],
        help_text="In the pH scale (0-14)",
    )
    temperature = models.FloatField(
        validators=[MinValueValidator(-1000), MaxValueValidator(1000)],
        help_text="In Celcius (°C)",
    )
    tds = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1000000)],
        help_text="Parts per million (ppm)",
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
