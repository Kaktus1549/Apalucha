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
from backend_logging.apalucha_logging import log

config_file = "./config.json"
with open(config_file) as f:
    config = json.load(f)

database = config["database"]
tables = config["database"]["tableNames"]
default_table = tables["default"]

engine = make_engine(database)

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

class TableRegistry(Base):
    __tablename__ = "table_registry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_names = Column(VARCHAR(255), nullable=False)
    runed = Column(Boolean, nullable=False, default=False)

def VoteRunFactory(table_name):
    class VoteRun(Base):
        __tablename__ = table_name
        ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
        Title = Column(VARCHAR(255), nullable=False)
        Team = Column(VARCHAR(255), nullable=False)
        FinalVoteCount = Column(Integer, nullable=True, default=0)
    return VoteRun

def create_table_if_not_exists(engine, tablename):
    # Create a table if it doesn't exist in the metadata.
    VoteRun = VoteRunFactory(tablename)
    VoteRun.__table__.create(bind=engine, checkfirst=True)

def add_table_to_registry(session, tablename):
    #Add a table name to the TableRegistry if it doesn't exist.
    table_registry = session.query(TableRegistry).filter(TableRegistry.table_names == tablename).first()
    if not table_registry:
        table_registry = TableRegistry(table_names=tablename)
        session.add(table_registry)
        session.commit()

def create_vote_table(session, tablename):
    # Create a vote table and add it to the TableRegistry
    add_table_to_registry(session, tablename)
    create_table_if_not_exists(session.bind, tablename)

Base.metadata.create_all(engine)
session = Session(engine)
# Create the default table if it doesn't exist
try:
    create_vote_table(session, default_table)
except Exception as e:
    log("ERROR", f"Got exception while adding table registry entry for table {default_table}: {e}")
    session.rollback()