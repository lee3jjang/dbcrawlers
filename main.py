from stockpricecrawler import StockPriceCrawler

if __name__ == '__main__':
    spc = StockPriceCrawler()
    spc.set_code(['005830', '005930'])
    spc.set_daterange('2019-07-01', '2019-12-31')
    stock_price = spc.get_stock_price()
