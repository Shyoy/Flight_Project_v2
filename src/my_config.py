import logging as log
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from hashlib import sha256

log.basicConfig(level=log.INFO, format="{levelname}: {message}",
                style="{")  ## TODO create a log file for info and debug

engine = create_engine('sqlite:///DBFlight.db', echo=True)
base = declarative_base()

Session = sessionmaker(bind=engine)

