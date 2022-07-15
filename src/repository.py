from src.repo.users import User
from src.repo.administrators import Administrator
from src.repo.customers import Customer
from src.repo.flights import Flight
from src.repo.tickets import Ticket
from src.repo.airline_companies import AirlineCompany
from src.repo.countries import Country
from src.my_config import log, engine, Session, func, inspect, database
# from create_db import validate_db
from random import randint as rnd
from datetime import datetime, timedelta


class Repository:

    def __init__(self):
        # Dictionary with table names as keys and table class name as value
        self.tables_d = {
            User.__tablename__: User,
            Administrator.__tablename__: Administrator,
            Customer.__tablename__: Customer,
            Flight.__tablename__: Flight,
            Ticket.__tablename__: Ticket,
            AirlineCompany.__tablename__: AirlineCompany,
            Country.__tablename__: Country
        }
        # makes sure all wanted tables exist in database
        # validate_db(list(self.tables_d.keys()))

        # Open session so we can edit database
        self.session = Session()

    def get_by_id(self, table_name: str, _id: int) -> object:
        """Finds the id given ,in a table."""

        # format table name
        table_name = '_'.join([w.capitalize() for w in table_name.split("_")])

        # Makes sure given table is in the database 
        if table_name in self.tables_d.keys():
            table_class = self.tables_d[table_name]

            # Gets row as object in the given table by id
            obj = self.session.query(table_class).get(_id)
            # Checks if he finds the id in the table
            if obj:
                log.info(f"Finds object in {table_name} table")
                return obj
            # Didn't and returns None
            else:
                log.info(f"cant find id: {_id} in {table_name} table")

        # When given table not in database return None
        else:
            log.info(f"Failed, make sure: {table_name} is an existing table.")

    def get_all(self, table_name: object) -> list:
        """get all rows of a selected table into a list of obj, empty or wrong returns None"""
        # format table name
        table_name = '_'.join([w.capitalize() for w in table_name.split("_")])

        # Makes sure given table is in the database
        if table_name not in self.tables_d.keys():
            log.info(f"Failed make sure 'obj' parm he is one of our tables object")
            return None

        # search the database for the table and returns it
        table_class = self.tables_d[table_name]
        table_objs = self.session.query(table_class).all()
        if table_objs:
            log.info(f"created a list of all {table_name}")
            return table_objs
        # if table is empty
        else:
            log.info(f"Failed {table_name} is an empty table")

    def add(self, kind: object):  ##TODO fix kind to table name
        """Add an object to a selected table"""
        try:
            self.session.add(kind)
            self.session.commit()
            log.info(f"Added a {kind}")
        except Exception as e:
            log.info(f"failed to add: {kind}")
            log.error(f"{e}")

    def update(self, col: str, obj: object, val: str):
        if type(obj) not in self.tables_d.values():
            log.info(f" Failed make sure ur parameters are as it should be")
            return None

        attr = list(obj.__dict__.keys())[1:]
        if col in attr:
            try:
                setattr(obj, col, val)
                self.session.commit()
                log.info(f"updated {obj.__tablename__} in column {col} id:{obj._id} ")
            except Exception as e:
                log.info(f"failed to update to: {val} \n\
                make sure you know the constraints of this table")
                log.error(f"{e}")
        else:
            log.info(f"Failed make sure that the column exist in table")

    def add_all(self, object_list: list):
        """ Adds a list of objects into the database"""
        count = 0

        # making sure all params in 'object_list' are param object
        if all(map(lambda x: type(x)not in self.tables_d.values() or x._id, object_list)):
            log.info(f"Failed make sure 'object_list' is a list filled with new table_objs")
            return None

        # loops all objects and try to commit them
        for obj in object_list:
            try:
                self.session.add(obj)
                self.session.commit()
                count += 1
            # some can fail because of database constrains ,log the error
            except Exception as e:
                log.info(f"failed to add: {obj} object to the database")
                log.error(f"{e}")
            # close session even if it failed so the next commit will not fail
            finally:
                self.session.close()
        log.info(f"added {count} objects out of {len(object_list)} to the database")

    def remove(self, obj: object):
        """Removes an object from our dictionary"""
        # check that obj is one of the tables object
        if type(obj) in self.tables_d.values():
            # Deletes it and try to commit it
            try:
                self.session.delete(obj)
                log.info("Object deleted")
                self.session.commit()
            # if table object already gone and not in database yet
            except Exception as e:
                log.info(f"Failed this object doesn't exist in database \n{e}")
                log.error(f"{e}")
        # When obj is not a table object
        else:
            log.info(f"Failed 'obj' Must be a table object ")

    def get_airlines_by_country(self, country: str) -> list:
        """ search Airline_Companies table for country parm """

        # Check for country in table and return a list
        airlines = self.session.query(AirlineCompany). \
            filter(AirlineCompany.country.ilike(f"%{country}%")).all()

        # Check if airlines list is None
        if airlines:
            log.info(f"Found {len(airlines)} airlines in {country}")
            return airlines
        # Return None
        else:
            log.info(f"Failed '{country}' country doesnt exist in the database")

    def get_flights_by_origin_country(self, country: str) -> list:
        """ search Flights table for country parm in origin col """

        # Check for country in table and return a list
        flights = self.session.query(Flight). \
            filter(Flight.origin_country.ilike(f"%{country}%")).all()

        # Check if flights list is None
        if flights:
            log.info(f"Found {len(flights)} flights from {country}")
            return flights
        # Return None
        else:
            log.info(f"Failed '{country}' country doesnt exist in the database")

    def get_flights_by_destination_country(self, country: str) -> list:
        """ search Flights table for country parm in destination col """

        # Check for country in table and return a list
        flights = self.session.query(Flight). \
            filter(Flight.destination_country.ilike(f"%{country}%")).all()

        # Check if flights list is None
        if flights:
            log.info(f"Found {len(flights)} flights to {country}")
            return flights
        # Return None
        else:
            log.info(f"Failed '{country}' country doesnt exist in the database")

    def get_flights_by_departure_date(self, date: datetime) -> list:
        """ search Flights table for date parm in departure_date col """
        depart_day = date.date()

        # Check for date in table and return a list
        flights = self.session.query(Flight). \
            filter(func.date(Flight.departure_time) == depart_day).all()

        # Check if flights list is None
        if flights:
            log.info(f"Found {len(flights)} departing flights at {depart_day}")
            return flights
        # Return None
        else:
            log.info(f"Failed this date: '{depart_day}' doesnt exist in the database")

    def get_flights_by_landing_date(self, date: datetime) -> list:
        """ search Flights table for date parm in landing_date col """
        lan_day = date.date()

        # Check for date in table and return a list
        flights = self.session.query(Flight). \
            filter(func.date(Flight.landing_time) == lan_day).all()

        # Check if flights list is None
        if flights:
            log.info(f"Found {len(flights)} incoming flights at {lan_day}")
            return flights
        # Return None
        else:
            log.info(f"Failed this date: '{lan_day}' doesnt exist in the database")


if __name__ == '__main__':  ## TODO foreignkey in data base and uniqe constraint and on delete
    repo = Repository()
    # print(repo.session)
    # dat = datetime(year=2022, month=9, day=22)
    # repo.get_airlines_by_country("United States")
    # repo.get_flights_by_origin_country('France')
    # repo.get_flights_by_destination_country('France')

    # flight = repo.get_by_id('Flights', 22)
    # repo.remove(repo.get_by_id('Flights', 22))
    ticket1 = Ticket(3232, 212)
    # ticket2 = Ticket(666, 321)
    # ticket3 = Ticket(121, 545)
    # ticket4 = Ticket(1, 3)

    repo.add_all([ticket1])

    # flt = repo.get_flights_by_departure_date(dat)
    # flt = repo.get_flights_by_landing_date(dat)

    # print(f"FLights: {str(flt[0].departure_time)[:4]}")

    pass
