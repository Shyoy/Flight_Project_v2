from sqlalchemy import Column, Integer, String
from src.my_config import engine, base


class Country(base):
    __tablename__ = 'Countries'
    _id = Column('country_id', Integer, primary_key=True)
    country = Column(String(80), nullable=False, unique=True)
    pic_base64 = Column(String(1000))

    def __init__(self, country: str, pic_base64: str):
        self.country = country
        self.pic_base64 = pic_base64


if __name__ == '__main__':
    # new_country = Countries(country="Yeman")
    # engine.add
    pass