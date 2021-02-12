.. image:: images/logo.svg
   :width: 50%
   :alt: statsmodels
   :align: left

:ref:`dbcrawlers <about:About dbcrawlers>` 는 웹에 존재하는 데이터를 수집하기 위한 클래스 및 함수들을 제공하는 파이썬 모듈입니다.

Introduction
============
``dbcrawlers`` 는 주가, 환율 등의 데이터를 편리하게 수집하기 위해 만들어졌습니다.
아래는 간단한 예제입니다:

.. ipython:: python

   from dbcrawlers.exchangeratecrawler import ExchangeRateCrawler

   erc = ExchangeRateCrawler()

   # 종목코드, 기준일자 설정
   erc.set_code(['FX_USDKRW', 'FX_JPYKRW']) 
   erc.set_daterange('2020-01-01', '2020-12-31') 

   # 수집시작
   exchange_rate = erc.get_exchange_rate()
   exchange_rate.head()

Citation
========

.. toctree::
   :maxdepth: 1

   install
   user-guide
   api
   about

Index
=====

:ref:`genindex`

:ref:`modindex`