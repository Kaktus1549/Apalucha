from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

adminTable = "Admins"
userTable = "Users"
filmsTable = "Films"

Base = declarative_base()

class User(Base):
    __tablename__ = userTable
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Vote = Column(Integer, nullable=True)
class Admin(Base):
    __tablename__ = adminTable
    Username = Column(VARCHAR(255), primary_key=True, nullable=False)
    PasswordHash = Column(VARCHAR(255), nullable=False)
class Films(Base):
    __tablename__ = filmsTable
    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Title = Column(VARCHAR(255), nullable=False)
    Team = Column(VARCHAR(255), nullable=False)
    FinalVoteCount = Column(Integer, nullable=True, default=0)