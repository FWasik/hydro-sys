# Generated by Django 5.1.6 on 2025-02-06 19:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=models.CharField(
                max_length=9,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must contain exactly 9 digits.",
                        regex="^\\d{9}$",
                    )
                ],
            ),
        ),
    ]
