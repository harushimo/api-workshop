"""
Initial database setup for the portfolio and stock symbols
"""

import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

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
    portfolio_name = Column(String(500),nullable=False)
    stocks =  relationship("Stock", secondary="portfolio_stocks")
    description = Column(String(500), nullable= False)

    @property
    def serialize(self):
        """
        This is return a serialize portfolio object
        """
        return {
            'id': self.id,
            'portfolio_name': self.portfolio_name,
            'stocks': self.stocks,
            'description': self.description
        }

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




