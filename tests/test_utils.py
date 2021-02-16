import sys
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

def test_generate_yearmonth_length():
    from dbcrawlers.utils import generate_yearmonth
    year_months = generate_yearmonth((2017, 3), (2019, 12))
    assert len(year_months) == 34

def test_generate_yearmonth_format():
    from dbcrawlers.utils import generate_yearmonth
    year_months = generate_yearmonth((2017, 3), (2019, 12), '\'%y.%m')
    assert year_months[0] == "\'17.03"
