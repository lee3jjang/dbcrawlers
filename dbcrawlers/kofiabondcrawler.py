import os
import time
import shutil
from pathlib import Path
import pandas as pd
from datetime import datetime
from selenium import webdriver

class InterestRateCrawler:
    """금융투자협회(kofiabond)에서 최종호가수익률 데이터를 수집합니다.

    Parameters
    ----------
    tab_sleep : float
        탭 이동 후 멈춤시간
    click_sleep : float
        클릭 후 멈춤시간
    download_sleep : float
        다운로드 후 멈춤시간
    headless : bool
        headless 여부

    Examples
    --------
    >>> irc = InterestRateCrawler(headless=True)
    >>> irc.set_daterange('2020-01-01', '2020-12-31')
    >>> irc.set_maturity([1, 3, 5, 10 ,20])
    >>> interest_rate = irc.get_interest_rate()
    """
    
    def __init__(self, tab_sleep=5, click_sleep=1, download_sleep=1, headless=True):
        # 변수 설정
        self.tab_sleep = tab_sleep
        self.click_sleep = click_sleep
        self.download_sleep = download_sleep
        self.headless = headless

        self.PATH = Path(__file__).parent.absolute()

        # 키 : 만기, 값 : 순서
        self.bond_map = {
            1: 0,
            3: 1,
            5: 2,
            10: 3,
            20: 4,
            30: 5,
        }

        # 남아있는 파일 제거
        self.download_path = f"C:\\Users\\{os.environ['USERNAME']}\\Downloads"
        if any(['최종호가 수익률.xls' == s for s in os.listdir(self.download_path)]):
            os.remove(self.download_path + '/최종호가 수익률.xls')

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

    def set_maturity(self, maturities):
        """수집할 금리의 만기를 설정합니다.

        Parameters
        ----------
        maturities : list

        Warnings
        --------
        list 안에 연 단위 숫자형으로 입력해야 함
        """
        self.maturities = maturities

    def get_interest_rate(self):
        """설정에 따라 수집을 수행합니다.
            
        Returns
        -------
        DataFrame
            수집된 금리 데이터프레임
        Warnings
        --------
        maturities와 date range 설정 후 실행해야 함
        """

        # temp 폴더 생성
        os.makedirs(f"{self.PATH}/temp", exist_ok=True)

        chrome_options = webdriver.ChromeOptions()
        if self.headless:
            chrome_options.add_argument('headless')
        chrome_options.add_argument('disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome('chromedriver', options=chrome_options)
        url = 'http://www.kofiabond.or.kr/websquare/websquare.html?w2xPath=/xml/bondint/lastrop/BISLastAskPrc.xml&divisionId=MBIS01010010000000&serviceId=&topMenuIndex=0&w2xHome=/xml/'
        driver.get(url)

        # 기간별 이동
        driver.find_element_by_css_selector('li#tabContents1_tab_tabs2').click()

        time.sleep(self.tab_sleep)

        # 프레임 선택
        driver.switch_to.frame(driver.find_element_by_css_selector('iframe#tabContents1_contents_tabs2_body'))

        # 채권 종류 선택
        for i in [9, 10, 13, 15, 1, 2]:
            driver.find_element_by_css_selector(f'input#chkAnnItm_input_{i}').click()
        for maturity in self.maturities:
            driver.find_element_by_css_selector(f'input#chkAnnItm_input_{self.bond_map[maturity]}').click()
        
            
        # 조회일자 선택
        driver.find_element_by_css_selector('input#startDtDD_input').clear()
        driver.find_element_by_css_selector('input#startDtDD_input').send_keys(self.start_date.strftime('%Y%m%d'))
        driver.find_element_by_css_selector('input#endDtDD_input').clear()
        driver.find_element_by_css_selector('input#endDtDD_input').send_keys(self.end_date.strftime('%Y%m%d'))

        # 조회
        driver.find_element_by_css_selector('a#group154').click()
        time.sleep(self.click_sleep)

        # 다운로드
        driver.find_element_by_css_selector('a#grpExcel').click()

        # result 폴더로 이동
        while(not any(['최종호가 수익률.xls' == s for s in os.listdir(self.download_path)])):
            time.sleep(self.download_sleep)
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        shutil.move(self.download_path + '/최종호가 수익률.xls', f'{self.PATH}/temp/risk_free_interest_rate_{now}.xlsx')

        # 추가 가공
        rf_interest_rate = pd.read_excel(f'{self.PATH}/temp/risk_free_interest_rate_{now}.xlsx')
        rf_interest_rate = rf_interest_rate.set_index('일자')
        rf_interest_rate.columns = rf_interest_rate.columns.str.extract(r'(\d+)년')[0]
        rf_interest_rate = rf_interest_rate.drop(['최고', '최저'], axis=0)
        rf_interest_rate = rf_interest_rate.reset_index()
        rf_interest_rate['일자'] = rf_interest_rate['일자'].astype('datetime64[ns]')
        driver.close()

        # temp 폴더 삭제
        shutil.rmtree(f'{self.PATH}/temp')

        return rf_interest_rate
