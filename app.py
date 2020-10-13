from flask import Flask
from flask import jsonify
from flask import request
from flask_api import status
from flask_sqlalchemy import SQLAlchemy
from yahooquery import Ticker
from database import db, Stock, Portfolio, PortfolioStocks
import json
import uuid

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


@app.route('/portfolios', methods=['POST'])
def create_portfolios():
    """
    Creates the stock portfolio
    """
    rec_data = json.loads(request.data)
    print(json.loads(request.data))
    stock_info = Ticker(rec_data['stocks'])
    print((stock_info))
    newPortfolio =  Portfolio(portfolio_name = rec_data['portfolio_name'],
                              portfolio_id = str(uuid.uuid4()),
                              stocks = [],
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
  
    
# TO DO Read Flask SQL ALCHEMY API
# TO DO URLLIB2 testing
@app.route('/portfolios/<string:p_id>', methods=['GET'])
def get_portfolio(p_id):
    """
    This will retrieve single a portfolio information
    """
    p = Portfolio.query.filter_by(portfolio_id = p_id).first()
    stocks = Stock.query.join(PortfolioStocks).filter(Stock.id == PortfolioStocks.stock_id).filter(PortfolioStocks.portfolio_id == p_id).all()
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


# @app.route('/portfolios', methods=['POST'])
# def update_portfolio():
#     """
#     Updates the portfolio with new stocks
#     """


# @app.route('/portfolios', methods = ['DELETE'])
# def delete_portfolio():
#     """
#     Deletes stock portfolio
#     """
#     db.session.delete(newPortfolio)
#     db.session.commit()
    

if __name__ == "__main__":
    app.run()