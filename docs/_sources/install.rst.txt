Installing dbcrawlers
=====================

현재 dbcrawlers는 Source를 통한 설치만 지원하고 있습니다.
향후 PyPI를 통한 설치도 지원할 예정입니다.


Python Support
--------------

dbcrawlers는 Python 3.9를 지원합니다.


PyPI (pip)
----------

현재 pip를 통한 설치방법은 제공하고 있지 않습니다.
향후에 추가될 예정입니다.


Installation from Source
------------------------

가장 최신의 소스코드는 `github repository <https://github.com/lee3jjang/dbcrawlers>`__ 에서 받을 수 있습니다.
혹은 아래처럼 git를 통해 설치해주세요:

.. code-block:: bash
    
    pip install git+https://github.com/lee3jjang/dbcrawlers


Dependencies
------------
현재 최소 dependencies는:

* `Python <https://www.python.org>`__ >= 3.9
* `numpydoc <https://numpydoc.readthedocs.io/en/latest/>`__
* `nbsphinx <https://nbsphinx.readthedocs.io/>`__ >= 0.8.1
* `sphinx_material <https://bashtage.github.io/sphinx-material/>`__


Optional Dependencies
---------------------

* `IPython <https://ipython.org>`__ >= 5.0 은 sphinx 문서를 만들기 위해 필요합니다.
* `pytest <https://docs.pytest.org/en/latest/>`__ 는 test를 수행하기 위해 필요합니다.