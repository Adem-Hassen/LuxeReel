from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import Column, Integer, String,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from postgreConfig import Base
import datetime

client=AsyncIOMotorClient('mongodb://localhost:27017')
db=client['movies']


class Users(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)
    email=Column(String,unique=True,index=True)
    password=Column(String)
    phone_number=Column(String,unique=True,index=True)
    first_name=Column(String)
    last_name=Column(String)

    created_at=Column(DateTime,default=datetime.datetime.now())
    updated_at=Column(DateTime)
    
    tickets = relationship("Ticket", back_populates="owner")


class Ticket(Base):
    __tablename__="tickets"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,index=True)
    movie_name=Column(Integer,index=True)
    show_time=Column(DateTime,index=True)
    
    user_id_column=Column(Integer,ForeignKey("users.id"))

    owner = relationship("Users", back_populates="tickets")

