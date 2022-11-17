from datetime import timedelta

import os
import time
import django
from faker import Faker
import json


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flight_site.settings')
django.setup()

import accounts.models as acc_models
import flights.models as fly_models
from random import randint ,shuffle, choice
from django.utils import timezone


# def create_flight(n):

#     for f in range(1,5):
#         print(f'Floor {f}')
#         for new in range(n):
#             print(f'Room {n}')
#             created = False
#             while not created:
#                 beds = random.randint(2,6)
#                 floor = Floor.objects.get(number=f)
#                 new_room = Room(floor=floor, beds=beds)
#                 new_room.save()
#                 created = True
#                 print(f"created room {new_room.number}")



def fill_country_table():
    print('Inserting to country table')
    counter = 0
    with open("old_vr/src/data/countries_flag.json") as f:
        countries_flags = json.load(f)
    for country in countries_flags:
        
        try:
            if not country["flag_base64"]:
                print(country["country"])

            else:
                new_country = fly_models.Country.objects.create(
                    name=country["country"],
                    pic=country["flag_base64"]
                    )
                counter += 1
            
        except Exception as e:
            print('already got this country')

    return "Amount of countries added: ",counter


def add_flights(flights_per_airline: int, airlines_id: list):
    fake = Faker()
    all_countries = fly_models.Country.objects.all()
    for airline_id in airlines_id:
        airline_obj = acc_models.Airline.objects.get(id = airline_id)

        for _ in range(flights_per_airline):
            country_a = choice(all_countries)
            countries = [airline_obj.country, country_a]
            shuffle(countries)

            rand_hour = randint(3, 12)
            rand_min = choice([15,30,45])
            depart_time = timezone.datetime.astimezone(fake.date_time_between(
                    start_date =timezone.now(),
                    end_date =timezone.now()+ timedelta(days=365*2))
                    )
            land_time = depart_time + timedelta(hours=rand_hour,minutes=rand_min)
            print(depart_time)
            print(land_time)
            print()
            
            new_flight = fly_models.Flight.objects.create(
                airline = airline_obj,
                departure_time = depart_time,
                landing_time = land_time,
                origin_country = countries[0],
                destination_country = countries[1],
                )
            print(new_flight)
            print('Flight time', new_flight.flight_duration)





if __name__ == '__main__':
    print("Populating database")
    start = time.perf_counter()
    # print(fill_country_table())
    add_flights(100,[9,10,13])
    finish = time.perf_counter()
    print(f"Normal  finished in {round(finish-start,2)} seconds")