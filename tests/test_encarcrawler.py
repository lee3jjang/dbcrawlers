import sys
import pytest
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture(scope='module')
def usedcar_price():
    from dbcrawlers.encarcrawler import UsedCarPriceCrawler

    url = 'http://www.encar.com/fc/fc_carsearchlist.do?carType=for&searchType=model&TG.R=B#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.N._.Manufacturer.%EB%B2%A4%EC%B8%A0.))%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A20%7D'
    ucpc = UsedCarPriceCrawler(page_max=3, headless=True)
    ucpc.set_url(url)
    price = ucpc.get_usedcar_price()
    yield price

def test_usedcar_price_isworking(usedcar_price):
    assert len(usedcar_price) > 0