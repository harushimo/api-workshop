"""
Initial database setup for the portfolio and stock symbols
"""

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Stock(Base):
    """
    Creates the stock database
    """
    __tablename__ = 'stock'
    stock_symbol = Column(String(500), primary_key = True)
    open_price =  Column(Integer, nullable=False)
    close_price = Column(Integer, nullable=False)


class Portfolio(Base):
    """
    Portfolio database
    """
    __tablename = 'portfolio'
    portfolio_name = Column(String(500), primar_key = True)
    stocks =  Column(String(500), nullable = False)
    descripition = Column(String(500), nullable= False)


# Create Engine
engine = 'postgresql://'


