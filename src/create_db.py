from repo.users import User
from repo.administrators import Administrator
from repo.customers import Customer
from repo.flights import Flight
from repo.tickets import Ticket
from repo.airline_companies import AirlineCompany
from repo.countries import Country
from src.my_config import engine, base, inspect, database


def create_db():
    """ creates the database in src  folder"""
    base.metadata.create_all(engine)


def restart_table(table_class: object):
    """drop and load a given table class"""
    table_class.__table__.drop(engine)
    base.metadata.create_all(engine)


def validate_db(tables: list):
    """
    this func should be used in init repo ,
    to make sure Database exist and with all the wanted table inside
    """
    inspector = inspect(engine)
    db_tables = sorted(inspector.get_table_names())
    needed_tables = sorted(tables)
    if db_tables != needed_tables:
        raise Exception(
            f"Something is wrong with the {database}, make sure"
            f" he is in src folder or try create a knew one with create_db.py")


if __name__ == '__main__':
    # Run to create a database in src folder in not created yet
    create_db()
    # restart_table(Ticket)
    # restart_table(Flight)
    pass
