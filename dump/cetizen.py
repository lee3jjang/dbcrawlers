import urllib.request as req
from urllib.parse import urlparse, urlencode
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
from .DBCrawler import DBCrawler

class PnoCrawler(DBCrawler):

    def __init__(self, conn):
        super().__init__(conn)
        self.table_name = 'CETIZEN_PNO'
        self._create_table()

        url = 'https://price.cetizen.com/'
        res = req.Request(url)
        html = req.urlopen(res).read().decode('cp949')
        self.soup = BeautifulSoup(html, 'html.parser')
        self.wireless = {
            'wireless_1[]': 'S',
            'wireless_2[]': 'K',
            'wireless_3[]': 'L',
            'wireless_7[]': 'SELF',
            'wireless_1,2[]': 'S,K',
            'wireless_1,3[]': 'S,L',
            'wireless_2,3[]': 'K,L',
            'wireless_1,2,3[]': 'S,K,L',
            'wireless_1,2,3,7[]': 'S,K,L,SELF',
            'wireless_9[]': '해당없음',
            'wireless_0[]': '해외'
        }

    def _create_table(self):
        """
            Description
            -----------
            테이블 생성
        """
        
        query = """
            CREATE TABLE IF NOT EXISTS {table_name} (
            	PNO TEXT PRIMARY KEY,	
                MODEL TEXT,
                WIRELESS TEXT
            )
        """.format(table_name=self.table_name)
        self.cur.execute(query)
        self.conn.commit()
    
    def _get_info(self, tag):
        tag2 = tag.find_all('li', {'style': re.compile('^float:left')})
        pno = urlparse(tag2[0].a['href']).query.split('&')[1].split('=')[1]
        name = tag2[0].text
        model = tag2[1].text
        price = tag2[2].text
        return pno, name, model, price

    def _get_info_wireless(self, wireless):
        # id=make_0 인 애들 말고 하나씩 더 있어서 2개씩 중복됨(drop_duplicates 해야 함)
        tag = self.soup.find_all('div', {'name': wireless[0]})
        result = []
        for i in range(len(tag)):
            result.append([wireless[1], *self._get_info(tag[i])])
        pno = pd.DataFrame(result, columns=['WIRELESS', 'PNO', 'MODEL', '중고시세', '증감'])
        pno = pno[['PNO', 'MODEL', 'WIRELESS']].drop_duplicates().reset_index(drop=True)
        return pno

    def run(self):
        """
            conn = sqlite3.connect('external_data.db')
            pc = PnoCrawler(conn)
            pc.run()
        """
        result = []
        for wl in self.wireless.items():
            result.append(self._get_info_wireless(wl))
        pno = pd.concat(result)
        pno.to_sql(name=self.table_name, con=self.conn, if_exists='replace', index=False)


class UsedPhonePriceCrawler(DBCrawler):

    def __init__(self, conn):
        super().__init__(conn)
        self.table_name = 'CETIZEN_USED_PHONE_PRICE'
        self._create_table()
    
    def _create_table(self):
        """
            Description
            -----------
            테이블 생성
        """
        
        query = """
            CREATE TABLE IF NOT EXISTS {table_name} (
            	BASE_DATE TEXT,	
                PNO TEXT,
                LOW NUMBER,
                MID NUMBER,
                HIGH NUMBER,
                PRIMARY KEY(BASE_DATE, PNO)
            )
        """.format(table_name=self.table_name)
        self.cur.execute(query)
        self.conn.commit()

    def set_pno(self, pnos):
        """
            Description
            -----------
            수집할 단말기 코드들 설정
            
            Input
            -----
            pno : 7296(SM-A102N 자급), 7320(SM-G986N U+), 7329(SM-R175)
            
            Example
            -------
            conn = sqlite3.connect('external_data.db')
            uppc = UsedPhonePriceCrawler(conn)
            uppc.set_pno(['7296', '7320', '7329'])
        """
        
        self.pnos = pnos

    @staticmethod
    def get_used_phone_price(pnos):
        """
            Description
            -----------
            크롤러 실행
            
            Example
            -------
            conn = sqlite3.connect('external_data.db')
            uppc = UsedPhonePriceCrawler(conn)
            uppc.set_pno(['7296', '7320', '7329'])
            uppc.run()
        """

        result = []
        start_time = datetime.now()
        
        print('[{}] 데이터 수집을 시작합니다. (pno: {}개)'.format(start_time.strftime('%Y/%m/%d %H:%M:%S'), len(pnos)))
        for pno in pnos:
            params = {'q': 'info', 'pno': pno}
            url = 'https://market.cetizen.com/market.php'
            url_params = '{}?{}'.format(url, urlencode(params))
            html = req.urlopen(url_params).read().decode('cp949')
            soup = BeautifulSoup(html, 'html.parser')
            txt = soup.find_all('script', {'type': "text/javascript"})[18].text
            start = txt.find('[')
            end = txt.find(']')
            txt = txt[start:end+1].replace('\r\n\t', '')\
                .replace('date', '"date"').replace('mid', '"mid"').replace('high', '"high"').replace('low', '"low"')
            data = eval(txt)
            for dt in data:
                result.append((dt['date'], pno, dt['low'], dt['mid'], dt['high']))
        used_phone_price = pd.DataFrame(result, columns=['BASE_DATE', 'PNO', 'LOW', 'MID', 'HIGH']).reset_index(drop=True)
        used_phone_price[['LOW', 'MID', 'HIGH']] = used_phone_price[['LOW', 'MID', 'HIGH']].astype(float)
        end_time = datetime.now()
        print('[{}] 데이터 수집을 종료합니다. (pno: {}개, 수집시간: {}초, 데이터수: {:,}개)'.format(end_time.strftime('%Y/%m/%d %H:%M:%S'), len(pnos), (end_time-start_time).seconds, len(used_phone_price)))
        return used_phone_price

    def run(self):
        """
            Description
            -----------
            크롤러 실행
            
            Example
            -------
            conn = sqlite3.connect('external_data.db')
            cur = conn.cursor()
            cur.execute('SELECT PNO FROM CETIZEN_PNO')
            pnos = list(map(lambda x: x[0], cur.fetchall()))
            uppc = UsedPhonePriceCrawler(conn)
            uppc.set_pno(pnos)
            uppc.run()
        """

        used_phone_price = self.get_used_phone_price(self.pnos)
        used_phone_price.to_sql(name=self.table_name, con=self.conn, if_exists='replace', index=False)