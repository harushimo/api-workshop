"""
Initial database setup for the portfolio and stock symbols
"""

import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

db = SQLAlchemy()

class Stock(db.Model):
    """
    Creates the stock database
    """
    __tablename__ = 'stock'
    stock_symbol = Column(String(500), primary_key = True)
    open_price =  Column(Integer, nullable=False)
    close_price = Column(Integer, nullable=False)


class Portfolio(db.Model):
    """
    Portfolio database
    """
    __tablename = 'portfolio'
    portfolio_name = Column(String(500), primary_key = True)
    stocks =  Column(String(500), nullable = False)
    descripition = Column(String(500), nullable= False)




