from stockpricecrawler import StockPriceCrawler

if __name__ == '__main__':
    spc = StockPriceCrawler()
    spc.set_code(['005830', '005930', '105560'])
    spc.set_daterange('2018-01-01', '2019-12-31')
    df = spc.get_stock_price()