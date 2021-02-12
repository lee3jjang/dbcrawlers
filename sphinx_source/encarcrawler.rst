Encar Crawler
=============

Examples
--------

.. ipython:: python

   from dbcrawlers.encarcrawler import UsedCarPriceCrawler

   ucpc = UsedCarPriceCrawler(page_max=3, headless=True)

   # URL 설정
   url = 'http://www.encar.com/fc/fc_carsearchlist.do?carType=for&searchType=model&TG.R=B#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.N._.Manufacturer.%EB%B2%A4%EC%B8%A0.))%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A20%7D'
   ucpc.set_url(url)

   # 수집시작
   usedcar_price = ucpc.get_usedcar_price()
   usedcar_price.head()


Model Reference
---------------

.. module:: dbcrawlers.encarcrawler

Model Class
^^^^^^^^^^^

.. autosummary::
    :toctree: generated/
    :template: class_custom.rst

    UsedCarPriceCrawler