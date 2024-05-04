from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base

Base = declarative_base()
'''
User: SQLAlchemy model for representing users in the database, including ID, name, username, and hashed password.
'''
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


