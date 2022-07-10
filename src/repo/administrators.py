from sqlalchemy import Column, Integer, String
from src.my_config import engine, base


class Administrator(base):
    __tablename__ = 'Administrators'
    _id = Column('admin_id', Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    user_id = Column(Integer, nullable=False, unique=True)

    def __init__(self, first_name: str, last_name: str, user_id: int):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id


if __name__ == '__main__':

    base.metadata.create_all(engine)
