from sqlalchemy import Column, Integer, String, ForeignKey
from src.my_config import engine, base


class AirlineCompany(base):
    __tablename__ = 'Airline_Companies'
    _id = Column('airline_id', Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    country = Column(String(80), ForeignKey("Countries.country_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("Customers.customer_id"), nullable=False, unique=True)

    def __init__(self, name: str, country: str, user_id: int):
        self.name = name
        self.country = country
        self.user_id = user_id
        # self.flights = []


if __name__ == '__main__':
    # base.metadata.create_all(engine)
    pass