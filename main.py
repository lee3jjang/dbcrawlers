import sqlite3
from datetime import datetime
from stockpricecrawler import StockPriceCrawler
import pandas as pd
from utils import pd2db

if __name__ == '__main__':

    # 주가 데이터 수집
    spc = StockPriceCrawler()
    spc.set_code(['005830'])
    spc.set_daterange('2020-01-01', '2020-03-30')
    stock_price = spc.get_stock_price()
    stock_price.기준일자 = stock_price.기준일자.apply(lambda x: x.strftime('%Y-%m-%d'))

    conn = sqlite3.connect('stockpricecrawler.db')

    # 주가 데이터 저장
    pd2db(conn, stock_price, 'STOCK_PRICE_HIS', 'ignore')

    # # TICKER 데이터 저장 (사전 프로세스)
    # company_codes = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')[0][['회사명', '종목코드']]
    # company_codes.종목코드 = company_codes.종목코드.map('{:06d}'.format)
    # pd2db(conn, company_codes[['회사명', '종목코드']], 'TICKER', 'ignore')

    # conn.close()