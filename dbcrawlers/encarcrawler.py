import os
import time
import shutil
import logging
import pandas as pd
from glob import glob
from pathlib import Path
from random import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

# 로깅 설정
if not any([s == 'log' for s in os.listdir()]): os.mkdir('log')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
file_handler = logging.FileHandler('log/encarcrawler.log')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)


class UsedCarPriceCrawler:
    """엔카에서 중고차 가격 데이터를 수집합니다.

    Parameters
    ----------
    max_page : int
        페이지 최대 수
    headless : bool
        수집 과정 보이는지 여부

    Examples
    --------
    >>> url = 'http://www.encar.com/fc/fc_carsearchlist.do?carType=for&searchType=model&TG.R=B#!%7B%22action%22%3A%22(And.Hidden.N._.(C.CarType.N._.Manufacturer.%EB%B2%A4%EC%B8%A0.))%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A1%2C%22limit%22%3A20%7D'
    >>> ucpc = UsedCarPriceCrawler(page_max=3, headless=True)
    >>> ucpc.set_url(url)
    >>> usedcar_price = ucpc.get_usedcar_price()
    """
    
    def __init__(self, page_max=200, headless=True):
        self.page_max = page_max
        self.headless = headless

    def set_url(self, url):
        """수집할 url를 설정합니다.

        Parameters
        ----------
        url : str
            수집할 페이지
        """
        self.url = url
        
    def get_usedcar_price(self):
        """수집을 시작합니다.

        Returns
        -------
        DataFrame
            수집된 중고차 중고가 데이터프레임\
        
        Warnings
        --------
        url 설정 후 실행해야 함
        """
        self._get_source(self.url)
        return self._parse()

    def _get_source(self, url):
        
        chrome_options = webdriver.ChromeOptions()
        if self.headless:
            chrome_options.add_argument('headless')
        chrome_options.add_argument('disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(str(Path(__file__).parent / 'chromedriver'), options=chrome_options)

        # 폴더 생성
        if not any([s == 'temp' for s in os.listdir(str(Path(__file__).parent))]):
            os.mkdir(str(Path(__file__).parent / 'temp'))
        
        # 접속하기
        logger.info('첫 페이지에 접근합니다.')
        driver.get(self.url)

        # [20개씩 보기] → [50개씩 보기]로 변환
        viewer = Select(driver.find_element_by_css_selector('select#pagerow'))
        viewer.select_by_value('50')

        time.sleep(10)

        # 수집하기
        page = 1
        logger.info('수집을 시작합니다.')
        while(True):
            if(page > self.page_max):
                logger.info(f'수집을 종료합니다. (페이지 한계치({self.page_max} 페이지) 도달)')
                break
            with open(str(Path(__file__).parent / f'temp/carlist_{page:04d}.html'), 'w', -1, encoding='utf-8') as f:
                soup = BeautifulSoup(driver.find_element_by_xpath('//tbody[@id="sr_normal"]/ancestor::table').get_attribute('outerHTML'), 'lxml')
                html = str(soup)
                f.write(html)
            try:
                driver.find_element_by_css_selector('div#pagination').find_element_by_xpath(f'//a[@data-page="{page+1}"]').click()
            except NoSuchElementException:
                logger.info(f'수집을 종료합니다. (총 수집 페이지: {page})')
                break
            page += 1
            time.sleep(1+2*random())
        driver.close()
    
    def _parse(self):

        logger.info('파싱을 시작합니다.')
        result = []
        files = glob(str(Path(__file__).parent / 'temp/*.html'))
        for file in files:
            with open(file, 'r', -1, encoding='utf-8') as f:
                html = f.read()
            soup = BeautifulSoup(html, 'lxml')
            carlist_batch = soup.select('tr')[1:]
            result_batch = []
            for car in carlist_batch:
                name1 = car.select_one('span.cls > strong').text
                name2 = car.select_one('span.cls > em').text
                name3 = car.select_one('span.dtl > strong').text
                name4 = car.select_one('span.dtl > em').text
                yer = car.select_one('span.yer').text
                km = car.select_one('span.km').text
                fue = car.select_one('span.fue').text
                loc = car.select_one('span.loc').text
                ins = '' if car.select_one('span.ins') == None else car.select_one('span.ins').text
                ass = '' if car.select_one('span.ass') == None else car.select_one('span.ass').text
                prc = car.select_one('td.prc_hs').text
                link = car.select_one('a').attrs['href']
                result_batch.append((name1, name2, name3, name4, yer, km, fue, loc, ins, ass, prc, link))
            column_name = ['name1', 'name2', 'name3', 'name4', 'yer', 'km', 'fue', 'loc', 'ins', 'ass', 'prc', 'link']
            df = pd.DataFrame(result_batch, columns=column_name)
            result.append(df)
        df = pd.concat(result).reset_index(drop=True)
        df['link'] = 'http://www.encar.com' + df['link']
        shutil.rmtree(str(Path(__file__).parent / 'temp'))
        logger.info('파싱이 종료되었습니다.')
        return df