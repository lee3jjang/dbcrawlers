import sys
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture(scope="module")
def year_months():
    from dbcrawlers.utils import generate_yearmonth
    year_months = generate_yearmonth("201703", "201912", format="'%y.%m")
    yield year_months

def test_generate_yearmonth_length(year_months):
    assert len(year_months) == 34

def test_generate_yearmonth_format(year_months):
    assert year_months[0] == "\'17.03"
