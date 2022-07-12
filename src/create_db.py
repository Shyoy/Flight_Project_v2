from repo.users import User
from repo.administrators import Administrator
from repo.customers import Customer
from repo.flights import Flight
from repo.tickets import Ticket
from repo.airline_companies import AirlineCompany
from repo.countries import Country
from src.my_config import engine, base


if __name__ == '__main__':
    # AirlineCompany.__table__.drop(engine)
    base.metadata.create_all(engine)
