from sqlalchemy import Column, Integer
from src.my_config import engine, base


class Ticket(base):
    __tablename__ = 'Tickets'
    _id = Column('ticket_id', Integer, primary_key=True)
    flight_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=False)

    def __init__(self, flight_id: int, customer_id: int):
        self.flight_id = flight_id
        self.customer_id = customer_id


if __name__ == '__main__':
    # log.debug("hey")
    base.metadata.create_all(engine)
