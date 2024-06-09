from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import json
from os import getenv
from sys import path
apalucha = getenv("apalucha")
if apalucha is None:
    apalucha = "."
path.append(apalucha)
from sql.sql_config import make_engine

config_file = "./config.json"
with open(config_file) as f:
    config = json.load(f)

database = config["database"]
tables = config["database"]["tableNames"]

engine = make_engine(database, False)

Base = declarative_base()

# Checks if tables exists with correct columns, if not, creates them    

class User(Base):
    __tablename__ = tables['user']
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Vote = Column(Integer, nullable=True)

class Admin(Base):
    __tablename__ = tables['admin']
    Username = Column(VARCHAR(255), primary_key=True, nullable=False)
    PasswordHash = Column(VARCHAR(255), nullable=False)

class Films(Base):
    __tablename__ = tables['films']
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Title = Column(VARCHAR(255), nullable=False)
    Team = Column(VARCHAR(255), nullable=False)
    FinalVoteCount = Column(Integer, nullable=True, default=0)


Base.metadata.create_all(engine)