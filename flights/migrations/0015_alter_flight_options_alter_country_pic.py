# Generated by Django 4.0.6 on 2022-11-17 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0014_alter_flight_airline_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flight',
            options={'ordering': ['departure_time']},
        ),
        migrations.AlterField(
            model_name='country',
            name='pic',
            field=models.URLField(default='https://www.supercoloring.com/sites/default/files/styles/coloring_medium/public/cif/2022/03/question-mark-flag-emoji-coloring-page.png', null=True),
        ),
    ]
