# Generated by Django 5.1.6 on 2025-02-06 12:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("systems", "0003_rename_created_at_hydroponicsystem_timestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="measurement",
            name="ph",
            field=models.FloatField(
                help_text="In the pH scale (0-14)",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(14),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="tds",
            field=models.FloatField(
                help_text="Parts per million (ppm)",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(1000000),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="temperature",
            field=models.FloatField(
                help_text="In Celcius (°C)",
                validators=[
                    django.core.validators.MinValueValidator(-1000),
                    django.core.validators.MaxValueValidator(1000),
                ],
            ),
        ),
    ]
