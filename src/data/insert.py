from src.repository import *
from faker import Faker
import json
import base64


def add_users():
    pass


def fill_country_table():
    repo = Repository()
    countrys = []
    with open("countries_flag.json") as f:
        countries_flags = json.load(f)
    for c in countries_flags:
        # print()
        countrys += [Country(c["country"], c["country"])]

    repo.add_all(countrys)


if __name__ == '__main__':
    # repo = Repository()
    # fake = Faker()
    fill_country_table()



    # codes = []
    # for i in range(len(countries)):
    # encoded = countries_flags[43]['flag_base64'].split(",")[1]
    # decoded = base64.b64decode(encoded)
    # print(type(decoded))




    # print(len(countries))
    # print(len(codes))
        # country = fake.country()
        # if country not in countries.json:
        #     countries.json += [country]

    # print(len(countries.json))