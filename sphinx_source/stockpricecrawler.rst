Stock Price Crawler
===================

Examples
--------

.. ipython:: python

   from dbcrawlers.stockpricecrawler import StockPriceCrawler

   spc = StockPriceCrawler()

   # 종목코드, 기준일자 설정
   spc.set_code(['005830', '005930', '105560']) 
   spc.set_daterange('2020-01-01', '2020-12-31') 

   # 수집시작
   stock_price = spc.get_stock_price()
   stock_price.head()


Model Reference
---------------

.. module:: dbcrawlers.stockpricecrawler

Model Class
^^^^^^^^^^^

.. autosummary::
    :toctree: generated/
    :template: class_custom.rst

    StockPriceCrawler