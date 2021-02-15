import sys
import pytest
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture(scope='module')
def product_number():
    from dbcrawlers.cetizencrawler import PnoCrawler

    pno_crawler= PnoCrawler()
    pno = pno_crawler.crawling()
    yield pno

@pytest.fixture(scope='module')
def usedphone_price(product_number):
    from dbcrawlers.cetizencrawler import UsedPhonePriceCrawler
    
    pno_temp = product_number.loc[lambda df: df.model.str.contains("SM")]
    models = list(pno_temp['pno'].unique())[:3]
    uppc = UsedPhonePriceCrawler(models)
    usedphone_price = uppc.crawling()
    yield usedphone_price

@pytest.fixture(scope='module')
def newphone_price(product_number):
    from dbcrawlers.cetizencrawler import NewPhonePriceCrawler
    pno_temp = product_number.loc[lambda df: df.model.str.contains("SM")]
    models = list(pno_temp['pno'].unique())[:3]
    nppc = NewPhonePriceCrawler(models)
    newphone_price = nppc.crawling()
    yield newphone_price

def test_models_price_isworking(product_number):
    assert len(product_number) > 0

def test_usedphone_price_isworking(usedphone_price):
    assert len(usedphone_price) > 0

def test_newphone_price_isworking(newphone_price):
    assert len(newphone_price) > 0