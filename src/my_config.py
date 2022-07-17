import logging
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy_utils import database_exists
from sqlalchemy.orm import sessionmaker
from hashlib import sha256
import os

# log format for the project ## TODO create a log file for info and debug
file_name = "repo\\repo.log"
formatter = logging.Formatter(datefmt='%d-%b-%y %H:%M:%S',
                              fmt=' - %(asctime)s - \n%(levelname)s: %(module)s.%(funcName)s -> %(message)s \n')
# handler = logging.FileHandler(file_name)
handler = logging.StreamHandler(stream=None)
handler.setFormatter(formatter)

log = logging.getLogger('repo_logger')
log.setLevel(logging.INFO)
log.addHandler(handler)


# Create engine and place it in the same folder
# database = 'sqlite:///DBFlight.db'
# database = 'sqlite:///C:\\src\\repo\\DBFlight.db'
dir_b = os.path.dirname(os.path.realpath(__file__))
connection_string = 'sqlite:///' + os.path.join(dir_b, 'DBFlight.db')
engine = create_engine(connection_string, echo=False)
base = declarative_base()


# Create a Session to then be used to edit the data on the database
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    # print(base.metadata.tables.keys())
    print(connection_string)
    # print(database_exists(database))
    # Inspector.get_table_names()
    pass
