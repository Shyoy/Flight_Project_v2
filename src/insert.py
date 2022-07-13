from src.repository import *
from faker import Faker
import json
import base64
from random import choice, randint, shuffle
from datetime import datetime, timedelta


def add_users(n: int): ##TODO connect to customer User
    repo = Repository()
    fake = Faker()
    for i in range(n):
        u = fake.simple_profile()
        # adds a new user
        password = fake.password(length=10, special_chars=False, upper_case=False)
        phone = fake.phone_number()
        n_user = User(u['username'], password, u['mail'], 'Customer')
        repo.add(n_user)

        # adds a new customer
        f_name = " ".join(u['name'].split()[:-1])
        l_name = u['name'].split()[-1]
        n_customer = Customer(f_name, l_name, u['address'], phone, n_user._id )
        repo.add(n_customer)



def add_airlines(n: int):
    """

    :param n: is the number of airlines to add must be an Integer
    :return: None
    """
    repo = Repository()
    fake = Faker()
    with open("data/airlines_data.json", encoding='utf-8') as f:
        airlines_data = json.load(f)

    for i in range(n):
        airline_d = choice(airlines_data)
        username = "_".join(airline_d["name"].strip().split(" "))
        email = username + "@gmail.com"
        password = fake.password(length=10, special_chars=False, upper_case=False)
        new_airline_user = User(username, password, email, 'Airline')

        repo.add(new_airline_user)
        new_airline = AirlineCompany(airline_d["name"], airline_d["country"], new_airline_user._id)
        repo.add(new_airline)


def add_flights(flights_per_airline: int, airlines_id: list):
    repo = Repository()
    fake = Faker()
    for _id in airlines_id:
        airline_obj = repo.get_by_id('Airline_Companies', _id)
        for i in range(flights_per_airline):
            country_a = repo.get_by_id('Countries', randint(1, 245)).country
            countrys = [airline_obj.country, country_a]
            shuffle(countrys)
            depart_time = fake.date_time_this_year(before_now=False, after_now=True)
            land_time = depart_time + timedelta(hours=randint(3, 12))
            print(depart_time)
            print(land_time)
            new_flight = Flight(airline_obj._id, countrys[0], countrys[1], depart_time, land_time)

            repo.add(new_flight)

def add_Tickets():
    repo = Repository()


def fill_country_table():
    repo = Repository()
    countrys = []
    with open("data/countries_flag.json") as f:
        countries_flags = json.load(f)
    for c in countries_flags:
        # print()
        countrys += [Country(c["country"], c["flag_base64"])]

    repo.add_all(countrys)


def update_all():
    repo = Repository()
    for i in range(1, 15):
        row_obj = repo.get_by_id('Users', i)
    # print(list(row_obj.__dict__.keys())[-1])
        repo.update('user_role', row_obj, 'Customer')
    pass


def delete_row(table_name: str, rows_id: list):
    repo = Repository()
    for _id in rows_id:
        row_obj = repo.get_by_id(table_name, _id)
        repo.remove(row_obj)


if __name__ == '__main__':
    repo = Repository()
    # fill_country_table()
    # add_users(4)
    # add_airlines(6)


    # print(blue_jet.name)
    add_flights(5, list(range(1, 18)))
    range(1, 18)


    # update_all()
    # delete_row('Countries', list([167]))


    pass
