from sqlalchemy import Column, Integer, String
from src.my_config import engine, base, sha256


class User(base):
    __tablename__ = 'Users'
    _id = Column('user_id', Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    user_role = Column(String, nullable=False)

    def __init__(self, username: str, password: str, email: str, user_role: int):

        self.username = username
        self.password = sha256(password.encode('utf-8')).hexdigest()
        self.email = email
        self.user_role = user_role


if __name__ == '__main__':
    # print(Users.__name__)
    base.metadata.create_all(engine)
