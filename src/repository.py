from src.repo.users import User
from src.repo.administrators import Administrator
from src.repo.customers import Customer
from src.repo.flights import Flight
from src.repo.tickets import Ticket
from src.repo.airline_companies import AirlineCompany
from src.repo.countries import Country
from src.my_config import log, engine, Session, func
from random import randint as rnd
from datetime import datetime, timedelta


class Repository:

    def __init__(self):
        self.session = Session()
        self.tables_d = {
            User.__tablename__: User,
            Administrator.__tablename__: Administrator,
            Customer.__tablename__: Customer,
            Flight.__tablename__: Flight,
            Ticket.__tablename__: Ticket,
            AirlineCompany.__tablename__: AirlineCompany,
            Country.__tablename__: Country
        }

    def get_by_id(self, table_name: str, _id: int) -> object:
        """Finds the id given ,in a table."""
        table_name = '_'.join([w.capitalize() for w in table_name.split("_")])
        if table_name in self.tables_d.keys():
            table = self.tables_d[table_name]
            obj = self.session.query(table).get(_id)
            if obj:
                log.info(f"Finds object in {table_name} table")
                return obj
            else:
                log.info(f"cant find id: {_id} in {table_name} table")
        else:
            log.info(f"Failed, make sure: {table_name} is an existing table.")

    def get_all(self, kind: object) -> list:  ##TODO fix kind to table name
        """get all rows of a selected table into a list of obj"""
        try:
            table = self.session.query(kind).all()
            log.info(f"created a list of all {kind.__name__}")
            return table
        except Exception as e:
            log.info(f"Failed and didn't find the table: {kind}")
            log.error(f"{e}")

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
            log.info(f"Make sure ur parameters are as it should be")
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

        # no use for update because it's not a real database for now

    def add_all(self, object_list: object):
        """ Uses add() func on a list of objects."""
        count = 0
        for obj in object_list:
            try:
                self.session.add(obj)
                self.session.commit()
                count += 1
            except Exception as e:
                log.info(f"failed to add: {obj} objects to the database")
                log.error(f"{e}")
            finally:
                self.session.close()
        log.info(f"added {count} objects to the database")

    def remove(self, obj: object):
        """Removes an object from our dictionary"""
        if obj:
            try:
                self.session.delete(obj)
                log.info("Object deleted")
                self.session.commit()
            except Exception as e:
                log.info(f"Failed this object doesn't exist in database \n{e}")
                log.error(f"{e}")
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


if __name__ == '__main__':
    repo = Repository()
    dat = datetime(year=2022, month=9, day=22)
    repo.get_airlines_by_country("United States")
    # repo.get_flights_by_origin_country('France')
    # repo.get_flights_by_destination_country('France')

    # flt = repo.get_flights_by_departure_date(dat)
    # flt = repo.get_flights_by_landing_date(dat)


    # print(f"FLights: {str(flt[0].departure_time)[:4]}")

    pass
