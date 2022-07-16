from src.repository import *
from faker import Faker
import json
# import base64
from random import choice, randint, shuffle
from datetime import datetime, timedelta


def add_administrators(amount: int):
    rep = Repository()
    fake = Faker()
    for i in range(amount):
        u = fake.simple_profile()
        # adds a new user
        password = fake.password(length=10, special_chars=False, upper_case=False)
        n_user = User(u['username'], password, u['mail'], 'Administrator')
        rep.add(n_user)

        # adds a new admin
        f_name = " ".join(u['name'].split()[:-1])
        l_name = u['name'].split()[-1]
        n_admin = Administrator(f_name, l_name, n_user._id)
        rep.add(n_admin)


def add_customers(amount: int):
    rep = Repository()
    fake = Faker()
    for i in range(amount):
        u = fake.simple_profile()
        # adds a new user
        password = fake.password(length=10, special_chars=False, upper_case=False)
        phone = fake.phone_number()
        n_user = User(u['username'], password, u['mail'], 'Customer')
        rep.add(n_user)

        # adds a new customer
        f_name = " ".join(u['name'].split()[:-1])
        l_name = u['name'].split()[-1]
        n_customer = Customer(f_name, l_name, u['address'], phone, n_user._id )
        rep.add(n_customer)


def add_airlines(amount: int):
    """
    :param amount: is the number of airlines to add must be an Integer
    :return: None
    """
    rep = Repository()
    fake = Faker()
    with open("data/airlines_data.json", encoding='utf-8') as f:
        airlines_data = json.load(f)

    for i in range(amount):
        airline_d = choice(airlines_data)
        username = "_".join(airline_d["name"].strip().split(" "))
        email = username + "@gmail.com"
        password = fake.password(length=10, special_chars=False, upper_case=False)
        new_airline_user = User(username, password, email, 'Airline')

        rep.add(new_airline_user)
        new_airline = AirlineCompany(airline_d["name"], airline_d["country"], new_airline_user._id)
        rep.add(new_airline)


def add_flights(flights_per_airline: int, airlines_id: list):
    rep = Repository()
    fake = Faker()
    for _id in airlines_id:
        airline_obj = rep.get_by_id('Airline_Companies', _id)
        for i in range(flights_per_airline):
            country_a = rep.get_by_id('Countries', randint(1, 245)).country
            countrys = [airline_obj.country, country_a]
            shuffle(countrys)
            depart_time = fake.date_time_this_year(before_now=False, after_now=True)
            land_time = depart_time + timedelta(hours=randint(3, 12))
            print(depart_time)
            print(land_time)
            new_flight = Flight(airline_obj._id, countrys[0], countrys[1], depart_time, land_time)

            rep.add(new_flight)


def add_tickets(amount: int):
    customer = None
    flight = None
    for i in range(amount):
        rep = Repository()
        flight = rep.get_by_id('Flights', randint(1, 6))
        customer = rep.get_by_id('Customers', randint(1, 50))
        ticket = Ticket(flight._id, customer._id)
        if flight.remaining_tickets > 0:
            rep.add(ticket)
            if ticket._id:
                flight.remaining_tickets -= 1
                rep.add(flight)
        else:
            print(f"Out of tickets for flight id: {flight._id} ")
            # print(type(tickets))

    # repo.add_all(tickets)


def fill_country_table():
    rep = Repository()
    countrys = []
    with open("data/countries_flag.json") as f:
        countries_flags = json.load(f)
    for c in countries_flags:
        countrys += [Country(c["country"], c["flag_base64"])]

    rep.add_all(countrys)


def update_all():
    rep = Repository()
    for i in range(1, 15):
        row_obj = rep.get_by_id('Users', i)
    # print(list(row_obj.__dict__.keys())[-1])
        rep.update('user_role', row_obj, 'Customer')
    pass


def delete_row(table_name: str, rows_id: list):
    """delete rows from a given table"""
    rep = Repository()
    for _id in rows_id:
        row_obj = rep.get_by_id(table_name, _id)
        rep.remove(row_obj)


if __name__ == '__main__':
    # # When you opened a new database, and you want to fill it use them all
    # fill_country_table()
    # add_administrators(5)
    # add_customers(100)
    # add_airlines(20)
    # add_flights(10, list(range(1, 21)))
    # add_tickets(200)



    # Which rows to update or delete
    # update_all()
    # delete_row('Countries', list([167]))


    pass
