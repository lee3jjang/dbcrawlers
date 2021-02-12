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
file_handler = logging.FileHandler('log/exchangeratecrawler.log')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

class ExchangeRateCrawler:
    """네이버에서 일별 환율 시계열 데이터를 수집합니다.

    Examples
    --------
    >>> erc = ExchangeRateCrawler()
    >>> erc.set_code(['FX_USDKRW', 'FX_JPYKRW'])
    >>> erc.set_daterange('2020-01-01', '2020-12-31')
    >>> exchange_rate = erc.get_exchange_rate()
    """
         
    def set_code(self, fx_codes):
        """수집할 환율의 환율코드를 설정합니다.

        Parameters
        ----------
        fx_codes : list
            종목코드 목록
        """
        
        self.fx_codes = fx_codes

    def set_daterange(self, start, end, format='%Y-%m-%d'):
        """수집할 날짜의 범위를 설정합니다.
            
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
        
    def get_exchange_rate(self):
        """설정에 따라 수집을 수행합니다.
            
        Returns
        -------
        DataFrame
            수집된 환율 데이터프레임

        Warnings
        --------
        fx codes와 date range 설정 후 실행해야 함
        """

        if not all([hasattr(self, 'fx_codes'), hasattr(self, 'start_date'), hasattr(self, 'end_date')]):
            raise Exception('사전 프로세스 오류')

        # 수집
        start_time_total = datetime.now()
        result = []
        logger.info(f'입력정보 (종목코드: {self.fx_codes}, 수집일자: {self.start_date.strftime("%Y.%m.%d")} ~ {self.end_date.strftime("%Y.%m.%d")})')
        for code in self.fx_codes:
            logger.info(f'수집을 시작합니다. (종목코드: {code})')
            start_time_each = datetime.now()
            page = 1
            while(True):
                url = f'https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd={code}&page={page}'
                # headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
                # res = requests.get(url, headers=headers, verify=True)
                # html = res.text
                data = pd.read_html(url)[0].dropna()

                if page != 1:
                    try:
                        if data.iloc[-1, 0] == result[-1].iloc[-1, 0]:
                            break
                    except:
                        break
                data.insert(0, '종목코드', code)
                result.append(data)
                date_min = datetime.strptime(data['날짜'].iloc[-1, 0], '%Y.%m.%d')
                if date_min <= self.start_date:
                    break
                page += 1
                time.sleep(0.01) # DELAY
            end_time_each = datetime.now()
            logger.info(f'수집을 종료합니다. (종목코드: {code}, 수집시간: {(end_time_each-start_time_each).seconds}초)')
                
        exchange_rate = pd.concat(result)
        exchange_rate.columns = ['종목코드', '기준일자', '매매기준율', '전일대비', '현찰_사실때', '현찰_파실때', '송금_보내실때', '송금_받으실때', 'TC_사실때', '외화수표_파실때']
        exchange_rate['기준일자'] = pd.to_datetime(exchange_rate['기준일자'], format='%Y.%m.%d')
        exchange_rate = exchange_rate.query('기준일자 <= @self.end_date and 기준일자 >= @self.start_date').reset_index(drop=True)
        exchange_rate = exchange_rate[['기준일자', '종목코드', '매매기준율', '전일대비', '현찰_사실때', '현찰_파실때', '송금_보내실때', '송금_받으실때', 'TC_사실때', '외화수표_파실때']]
        end_time_total = datetime.now()
        logger.info(f'수집결과 (수집시간: {(end_time_total-start_time_total).seconds}초, 데이터수: {len(exchange_rate):,}개)')
        return exchange_rate