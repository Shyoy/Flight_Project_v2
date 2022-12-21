from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.my_config import engine, base


class Customer(base):
    __tablename__ = 'Customers'
    _id = Column('customer_id', Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    address = Column(String(80))
    phone_no = Column(String(25), unique=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False, unique=True)
    # Tickets = relationship("Ticket", backref='customer')

    def __init__(self,
                 first_name: str, last_name: str, address: str,
                 phone_no: str, user_id: int):

        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone_no = phone_no
        self.user_id = user_id


if __name__ == '__main__':
    # base.metadata.create_all(engine)
    pass