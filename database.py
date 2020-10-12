"""
Initial database setup for the portfolio and stock symbols
"""

import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
import uuid

db = SQLAlchemy()

class Stock(db.Model):
    """
    Creates the stock database
    """
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String(500), nullable=False)
    open_price =  Column(Integer, nullable=False)
    close_price = Column(Integer, nullable=False)
    portfolios = relationship("Portfolio", secondary="portfolio_stocks")


class Portfolio(db.Model):
    """
    Portfolio database
    """
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(String(20), unique=True, nullable=False)
    portfolio_name = Column(String(500),nullable=False)
    stocks =  relationship("Stock", secondary="portfolio_stocks")
    description = Column(String(500), nullable= False)

class PortfolioStocks(db.Model):
    """
    Junction Table to represent M:N relationship between stocks and portfolios
    """
    __tablename__ = 'portfolio_stocks'
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'))
    stock_id = Column(Integer, ForeignKey('stock.id'))
    user = relationship(Stock, backref=backref('portfolio_stocks', cascade="all, delete-orphan"))
    portfolio = relationship(Portfolio, backref=backref('portfolio_stocks', cascade="all, delete-orphan"))




