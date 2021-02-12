Exchange Rate Crawler
=====================

Examples
--------

.. ipython:: python

   from dbcrawlers.exchangeratecrawler import ExchangeRateCrawler

   erc = ExchangeRateCrawler()

   # 종목코드, 기준일자 설정
   erc.set_code(['FX_USDKRW', 'FX_JPYKRW']) 
   erc.set_daterange('2020-01-01', '2020-12-31') 

   # 수집시작
   exchange_rate = erc.get_exchange_rate()
   exchange_rate.head()

Model Reference
---------------

.. module:: dbcrawlers.exchangeratecrawler
    :synopsis: Exchange rate crawler

Model Class
^^^^^^^^^^^

.. autosummary::
    :toctree: generated/
    :template: class_custom.rst

    ExchangeRateCrawler