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
from stock_api import get_stock_info

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

    def update(self, json_obj):
        if 'portfolio_name' in json_obj:
            self.portfolio_name = json_obj['portfolio_name']
        if 'stocks' in json_obj:
             stock_dicts = get_stock_info(json_obj['stocks'])
             for obj in stock_dicts:
                 self.stocks.append(Stock(stock_symbol = obj['stock_symbol'],
                                   open_price = obj['open_price'],
                                   close_price = obj['close_price']))
        if 'description' in json_obj:
            self.description = json_obj['description']
    

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




