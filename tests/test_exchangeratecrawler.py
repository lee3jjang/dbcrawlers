import sys
import pytest
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture(scope='module')
def exchange_rate():
    from dbcrawlers.exchangeratecrawler import ExchangeRateCrawler

    erc = ExchangeRateCrawler()
    erc.set_code(['FX_USDKRW', 'FX_JPYKRW'])
    erc.set_daterange('2020-01-01', '2020-12-31')
    rate = erc.get_exchange_rate()
    yield rate

def test_isworking(exchange_rate):
    assert len(exchange_rate) == 498

def test_date(exchange_rate):
    check_startdate = exchange_rate['기준일자'].min() == datetime(2020, 1, 2)
    check_enddate = exchange_rate['기준일자'].max() == datetime(2020, 12, 31)
    assert check_startdate and check_enddate