import os
import time
import logging
import requests
import pandas as pd
from datetime import datetime

# 로깅 설정
if not any([s == 'log' for s in os.listdir()]): os.mkdir('log')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
file_handler = logging.FileHandler('log/stockpricecrawler.log')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

class StockPriceCrawler(object):
    """네이버에서 일별 주가 시계열 데이터를 수집합니다.

    Examples
    --------
    >>> spc = StockPriceCrawler()
    >>> spc.set_code(['005830', '005930', '105560'])
    >>> spc.set_daterange('2019-01-31', '2019-12-31')
    >>> stock_price = spc.get_stock_price()
    """

    def __init__(self):
        pass
        
    def set_code(self, company_codes):
        """주가를 수집할 회사의 회사코드 설정

        Parameters
        ----------
        company_codes : list
            종목코드 list
        """
        
        self.company_codes = company_codes
        
    def set_daterange(self, start, end, format='%Y-%m-%d'):
        """수집할 날짜 범위 설정
            
        Parameters
        ----------
        start : str
            수집시작일
        end : str
            수집종료일
        format : str
            수집일 입력 
            
        Warnings
        --------
        (start date, end date) both days inclusive
        """

        self.start_date = datetime.strptime(start, '%Y-%m-%d')
        self.end_date = datetime.strptime(end, '%Y-%m-%d')
        if self.start_date > self.end_date:
            raise Exception('날짜 범위 입력 오류')

    def get_stock_price(self):
        """설정에 따라 수집 수행
            
        Returns
        -------
        DataFrame
            수집된 주가 데이터프레임

        Warnings
        --------
        company code와 date range 설정 후 실행해야 함
        """

        if not all([hasattr(self, 'company_codes'), hasattr(self, 'start_date'), hasattr(self, 'end_date')]):
            raise Exception('사전 프로세스 오류')

        start_time_total = datetime.now()
        result = []
        logger.info(f'입력정보 (종목코드: {self.company_codes}, 수집일자: {self.start_date.strftime("%Y.%m.%d")} ~ {self.end_date.strftime("%Y.%m.%d")})')
        for code in self.company_codes:
            logger.info(f'수집을 시작합니다. (종목코드: {code})')
            start_time_each = datetime.now()
            page = 1
            while(True):
                url = f'https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'
                headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                res = requests.get(url, headers=headers, verify=False)
                html = res.text
                data = pd.read_html(html)[0].dropna()     
                           
                if page != 1:
                    try:
                        if data.iloc[-1, 0] == result[-1].iloc[-1, 0]:
                            break
                    except:
                        break
                data.insert(0, '종목코드', code)
                result.append(data)
                date_min = datetime.strptime(data['날짜'].iloc[-1], '%Y.%m.%d')
                if date_min <= self.start_date:
                    break
                page += 1
                time.sleep(0.01) # DELAY
            end_time_each = datetime.now()
            logger.info(f'수집을 종료합니다. (종목코드: {code}, 수집시간: {(end_time_each-start_time_each).seconds}초)')
        stock_price = pd.concat(result)
        stock_price.columns = ['종목코드', '기준일자', '종가', '전일비', '시가', '고가', '저가', '거래량']
        stock_price['기준일자'] = pd.to_datetime(stock_price['기준일자'], format='%Y.%m.%d')
        stock_price = stock_price.query('기준일자 <= @self.end_date and 기준일자 >= @self.start_date').reset_index(drop=True)
        stock_price = stock_price[['기준일자', '종목코드', '종가', '시가', '고가', '저가', '거래량']]
        end_time_total = datetime.now()
        logger.info(f'수집결과 (수집시간: {(end_time_total-start_time_total).seconds}초, 데이터수: {len(stock_price):,}개)')
        return stock_price