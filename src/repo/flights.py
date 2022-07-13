from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from src.my_config import engine, base
from datetime import datetime


class Flight(base):
    __tablename__ = 'Flights'
    _id = Column('flight_id', Integer, primary_key=True)
    airline_company_id = Column(Integer, nullable=False)  #FK
    origin_country = Column(Integer, nullable=False)  #FK
    destination_country = Column(Integer, nullable=False) #FK
    departure_time = Column(DateTime, nullable=False)
    landing_time = Column(DateTime, nullable=False)
    remaining_tickets = Column(Integer, default=150)

    def __init__(self,
                 airline_company_id: int, origin_country: int, destination_country: int,
                 departure_time: datetime, landing_time: datetime, remaining_tickets=150
                 ):
        self.airline_company_id = airline_company_id
        self.origin_country = origin_country
        self.destination_country = destination_country
        self.departure_time = departure_time
        self.landing_time = landing_time
        self.remaining_tickets = remaining_tickets


if __name__ == '__main__':
    # print(Flight.__name__)
    base.metadata.create_all(engine)
    pass