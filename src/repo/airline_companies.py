from sqlalchemy import Column, Integer, String
from src.my_config import engine, base


class AirlineCompany(base):
    __tablename__ = 'Airline_Companies'
    _id = Column('airline_id', Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    country = Column(String(80), nullable=False)
    user_id = Column(Integer, nullable=False, unique=True)
    user_role = Column(Integer, nullable=False)

    def __init__(self, name: str, country: str, user_id: int, user_role: int):
        self.name = name
        self.country = country
        self.user_id = user_id
        self.user_role = user_role
        # self.flights = []


if __name__ == '__main__':
    base.metadata.create_all(engine)
