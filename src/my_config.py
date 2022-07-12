import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from hashlib import sha256


# log format for the project
file_name = "C:\\Users\\shay.DESKTOP-JUNLQ3P\\PycharmProjects\\Flight_Project_v2\\src\\repo\\repo.log"
logging.basicConfig(filename=file_name, level=logging.INFO, format="<{asctime}--{name}--{levelname}>:\n{funcName} ->{message}",
                style="{")  ## TODO create a log file for info and debug
log = logging.getLogger()

# Create engine and place it in the same folder
engine = create_engine('sqlite:///DBFlight.db', echo=True)
base = declarative_base()

# Create a Session to then be used to edit the data on the database
Session = sessionmaker(bind=engine)



if __name__ == '__main__':
    print(file_name)