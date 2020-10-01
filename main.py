import sqlite3
from datetime import datetime
from stockpricecrawler import StockPriceCrawler

if __name__ == '__main__':
    # 데이터 수집
    spc = StockPriceCrawler()
    spc.set_code(['005830'])
    spc.set_daterange('2020-01-01', '2020-06-30')
    stock_price = spc.get_stock_price()

    # DB 저장
    conn = sqlite3.connect('stockpricecrawler.db')
    cur = conn.cursor()
    last_update_date, last_modified_by = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'lee3jjang'
    tmp = [(df['기준일자'].strftime('%Y-%m-%d'), df['회사코드'], df['종가'], df['시가'], df['고가'], df['저가'], df['거래량'], last_update_date, last_modified_by) for _, df in stock_price.iterrows()]
    # cur.executemany('INSERT OR REPLACE INTO STOCK_PRICE_HIS VALUES(?,?,?,?,?,?,?,?,?)', tmp)
    cur.executemany('INSERT OR IGNORE INTO STOCK_PRICE_HIS VALUES(?,?,?,?,?,?,?,?,?)', tmp)
    conn.commit()
    conn.close()
