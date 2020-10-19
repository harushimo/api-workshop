from flask import Flask
from flask import jsonify
from flask import request
from flask_api import status
from flask_sqlalchemy import SQLAlchemy
from yahooquery import Ticker
from database import db, Stock, Portfolio, PortfolioStocks
import json
import uuid
import pprint
from stock_api import get_stock_info


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
    return jsonify(stock_object(stock_symbols))

   
@app.route('/portfolios', methods=['POST'])
def create_portfolios():
    """
    Creates the stock portfolio
    """
    rec_data = json.loads(request.data)
    print(json.loads(request.data))
    stock_info = rec_data['stocks']
    stock_dicts = get_stock_info(stock_info)
    pprint.pprint(stock_dicts)
    stock_objs = []
    for obj in stock_dicts:
        stock_objs.append(Stock(stock_symbol = obj['stock_symbol'],
                            open_price = obj['open_price'],
                            close_price = obj['close_price']))
    newPortfolio =  Portfolio(portfolio_name = rec_data['portfolio_name'],
                              portfolio_id = str(uuid.uuid4()),
                              stocks = stock_objs,
                              description = rec_data['description'])
    db.session.add(newPortfolio)
    db.session.commit()
    return jsonify({'message' : 'portfolio has been created'}), status.HTTP_201_CREATED

@app.route('/portfolios', methods=['GET'])
def get_portfolios():
    """
    This will generate URLs for all the portfolios
    """
    portfolios = db.session.query(Portfolio).all()
    res = []
    for p in portfolios:
        d = dict()
        d['name'] = p.portfolio_name
        d['url'] = f"http://localhost:5000/portfolios/{p.portfolio_id}"
        res.append(d)
    return json.dumps(res)
  
@app.route('/portfolios/<string:p_id>', methods=['GET'])
def get_portfolio(p_id):
    """
    This will retrieve single a portfolio information
    """
    p = Portfolio.query.filter_by(portfolio_id = p_id).first()
    stocks = Stock.query.join(PortfolioStocks).filter(Stock.id == PortfolioStocks.stock_id).filter(PortfolioStocks.portfolio_id == p.id).all()
    d = dict()
    d['portfolio_name'] = p.portfolio_name
    d['stocks'] = []
    for s in stocks:
        stock = dict()
        stock['stock_symbol'] = s.stock_symbol
        stock['open_price'] = s.open_price
        stock['close_price'] = s.close_price
        d['stocks'].append(stock)
    d['description'] = p.description
    return d


@app.route('/portfolios/<string:p_id>', methods=['PUT'])
def update_portfolio(p_id):
    """
    Updates the portfolio with new stocks
    """
    p = Portfolio.query.filter_by(portfolio_id = p_id).first()
    rec_data = json.loads(request.data)
    p.update(rec_data)
    db.session.commit()
    return jsonify({'message' : 'portfolio has been updated'}), status.HTTP_201_CREATED



@app.route('/portfolios/<string:p_id>', methods = ['DELETE'])
def delete_portfolio(p_id):
    """
    Deletes stock portfolio
    """
    print("We are in the delete portfolio")
    p = Portfolio.query.filter_by(portfolio_id = p_id).first()
    db.session.delete(p)
    db.session.commit   
    return jsonify({'message' : 'portfolio has been deleted'}), status.HTTP_200_OK


if __name__ == "__main__":
    app.run()
