from src.repository import *
from faker import Faker
import json
import base64


def add_users(n: int):
    fake = Faker()
    user_list = []
    for i in range(n):
        u = fake.simple_profile()
        password = fake.password(length=10, special_chars=False, upper_case=False)
        new_user = [u['username'], password, u['mail'], 3]
        print(new_user)
        # user_list += [new_user]


    # repo.add_all(user_list)
    pass


def fill_country_table():
    repo = Repository()
    countrys = []
    with open("data/countries_flag.json") as f:
        countries_flags = json.load(f)
    for c in countries_flags:
        # print()
        countrys += [Country(c["country"], c["flag_base64"])]

    repo.add_all(countrys)


if __name__ == '__main__':
    # fill_country_table()
    add_users(5)




    # codes = []
    # for i in range(len(countries)):
    # encoded = countries_flags[43]['flag_base64'].split(",")[1]
    # decoded = base64.b64decode(encoded)
    # print(type(decoded))