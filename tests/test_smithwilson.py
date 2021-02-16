import numpy as np
import pytest

@pytest.fixture(scope='module')
def smith_wilson():
    from dbcrawlers.esg.yieldcurve import SmithWilson

    sw = SmithWilson(ufr=0.052)
    maturity = np.array([1, 2, 3, 5, 10, 20])
    interest_rate = np.array([0.01301, 0.01325, 0.01415, 0.01600, 0.01625, 0.01604])
    sw.set_interest_rate(maturity, interest_rate)
    sw.alpha = 0.1
    yield sw

def check_instantaneous_forward_rate(smith_wilson):
    assert pytest.approx(smith_wilson.instantaneous_forward_rate(np.array([60]))[0]) == 0.0503265270103466
    
