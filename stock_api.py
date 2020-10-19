from yahooquery import Ticker

def get_stock_info(stock_symbols):
    """
    This is to create stock object
    """
    stock_ticker = Ticker(stock_symbols)
    stock_summary = stock_ticker.summary_detail
    stock_quote = stock_summary
    res = []
    for key,value in stock_quote.items():
        stock_list = dict()
        stock_list['stock_symbol'] = key
        stock_list['open_price'] = value['open']
        stock_list['close_price'] = value['previousClose']
        res.append(stock_list)
    return res