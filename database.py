from sqlalchemy import Column, ForeignKey, Integer, String, DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(200), nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    imageurl = Column(String(300), nullable=True)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'fullname': self.full_name,
            'username': self.username,
            'email': self.email,
            'imageurl': self.imageurl
        }


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    date_modified = Column(DateTime(timezone=True), server_default=func.now())
    date_added = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'date_modified': self.date_modified,
            'date_added': self.date_added,
            'user_id': self.user_id
        }


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(300), nullable=False)
    price = Column(Float, nullable=False)
    date_modified = Column(DateTime(timezone=True), server_default=func.now())
    date_added = Column(DateTime(timezone=True), onupdate=func.now())
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    category = relationship(Category)
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date_modified': self.date_modified,
            'date_added': self.date_added,
            'category_id': self.category_id,
            'user_id': self.user_id
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
