from sqlalchemy import Boolean, Column, ForeignKey,Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True,index=True)
    author_name = Column(String, index=True,unique=True)


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String, index=True,unique=True)
    author = Column(String)
    count_page = Column(Integer)

class User(Base):
    __tablename__ = "user"
    salt = Column(String)
    id = Column(Integer, primary_key=True,index=True)
    username = Column(Integer, unique=True,index=True)
    password = Column(String, index=True)


    
    