from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from yahooquery import Ticker
from database import db, Stock, Portfolio

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'
db.init_app(app)
db.app = app

#Creating Database
db.create_all()


@app.route('/')
def stock_portfolio():
    return 'Welcome to stock portfolio creator'

@app.route('/stock-symbols/quote', methods=['POST'])
def retrieve_stock_quote():
    """
    Retrieve stock quotes
    """
    stock_symbols = request.data.decode('utf-8')
    stock_ticker = Ticker(stock_symbols)
    return jsonify(stock_ticker.summary_detail)


@app.route('/stock-symbols/portfolios', methods=['POST'])
def create_portfolios():
    """
    Creates the stock portfolio
    """
    portolio = retrieve_stock_quote()
    print(portolio)
    return portolio


@app.route('/test3')
def test_site_3():
    return "You are the test endpoint 3"


if __name__ == "__main__":
    app.run()