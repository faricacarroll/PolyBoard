import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Sell(Base):
    __tablename__ = 'sell'

    sell_id = Column(Integer, primary_key=True)
    item = Column(String(50), nullable=False)
    desc = Column(String(50))
    price = Column(Float)

engine = create_engine('sqlite:///bulletin.db')

Base.metadata.create_all(engine)
