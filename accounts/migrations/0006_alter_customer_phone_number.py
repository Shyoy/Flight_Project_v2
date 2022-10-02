# Generated by Django 4.0.6 on 2022-09-21 22:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_airline_flights_remove_customer_flights'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=14, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(12)], verbose_name='phone number'),
        ),
    ]