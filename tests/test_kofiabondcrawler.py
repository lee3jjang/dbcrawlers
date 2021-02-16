import sys
import pytest
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture(scope='module')
def interest_rate():
    from dbcrawlers.kofiabondcrawler import InterestRateCrawler

    irc = InterestRateCrawler(headless=False)
    irc.set_daterange('2020-01-01', '2020-12-31')
    irc.set_maturity([1, 3, 5, 10 ,20])
    rate = irc.get_interest_rate()
    yield rate

def test_interest_rate_isworking(interest_rate):
    assert len(interest_rate) > 0