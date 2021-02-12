import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from mypackage import mymodule
from mypackage import mymodule2

def test_addition():
    assert mymodule.myaddition(4, 2) == 6

def test_subtraction():
    assert mymodule2.mysubtraction(4, 2) == 3