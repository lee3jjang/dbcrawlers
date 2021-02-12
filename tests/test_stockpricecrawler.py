import sys
import pytest
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture(scope='module')
def stock_price():
    from dbcrawlers.stockpricecrawler import StockPriceCrawler

    spc = StockPriceCrawler()
    spc.set_code(['005830', '005930', '105560'])
    spc.set_daterange('2020-01-01', '2020-12-31')
    price = spc.get_stock_price()
    yield price

def test_isworking(stock_price):
    assert len(stock_price) == 744

def test_date(stock_price):
    check_startdate = stock_price['기준일자'].min() == datetime(2020, 1, 2)
    check_enddate = stock_price['기준일자'].max() == datetime(2020, 12, 30)
    assert check_startdate and check_enddate