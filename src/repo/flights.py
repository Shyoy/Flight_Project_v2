from sqlalchemy import Column, Integer, String, DateTime
from src.my_config import engine, base
from datetime import datetime


class Flight(base):
    __tablename__ = 'Flights'
    _id = Column('flight_id', Integer, primary_key=True)
    airline_company_id = Column(Integer, nullable=False, unique=True)
    origin_country_id = Column(Integer, nullable=False, unique=True)
    destination_country_id = Column(Integer, nullable=False, unique=True)
    departure_time = Column(DateTime)
    landing_time = Column(DateTime)
    remaining_tickets = Column(Integer, nullable=False)

    def __init__(self,
                 airline_company_id: int, origin_country_id: int, destination_country_id: int,
                 departure_time: datetime, landing_time: datetime, remaining_tickets: int
                 ):
        self.airline_company_id = airline_company_id
        self.origin_country_id = origin_country_id
        self.destination_country_id = destination_country_id
        self.departure_time = departure_time
        self.landing_time = landing_time
        self.remaining_tickets = remaining_tickets


if __name__ == '__main__':
    # print(Flight.__name__)
    base.metadata.create_all(engine)