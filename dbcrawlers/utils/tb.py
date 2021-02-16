import os
import re
import pandas as pd
from .tools import *

def load_tb(filepath):
    """
        Description
        -----------
        Raw Data → 정제된 시산표로 변환
        
        Input
        -----
        path : 파일경로
        
        Output
        ------
        dataframe : 정제된 업무보고서
        
        Example
        -------
        from fss_rpt import load_tb
        ai059 = __load_tb('data/시산표_20170131.xlsx')
    """

    시산표 = pd.read_excel(filepath)
    시산표2 = 시산표.copy()
    시산표2 = 시산표2[~시산표2['Unnamed: 3'].isnull()]
    시산표2 = 시산표2.loc[:,~시산표2.iloc[0].isnull()]
    시산표2.columns = 시산표2.iloc[0].str.strip()
    시산표2.columns.name = None
    시산표2 = 시산표2.iloc[1:]
    시산표2 = 시산표2.query('계정과목 != " 계정과목"')
    시산표2 = 시산표2.fillna(0).reset_index(drop=True)
    시산표2 = 시산표2[['계정과목','계정과목명', '차    변', '대    변']]
    시산표2.columns = ['계정과목','계정과목명','차변','대변']
    시산표2.eval('잔액 = 차변 - 대변', inplace=True)
    시산표2[['차변','대변','잔액']] = 시산표2[['차변','대변','잔액']].astype(float)
    시산표2['계정과목'] = 시산표2['계정과목'].astype(str)
    시산표2 = 시산표2.query('계정과목 != "                      합             계"')
    return 시산표2

def load_tb_all(folderpath):
    """
        Description   
        -----------
        경로 안에 있는 사업실적표 전부 로드하여 dict 형태로 반환
        ※ 파일명 "시산표_yyyymmdd.xlsx" 형태로 되어 있어야 함 (매월 말일자)
        
        Input
        -----
        path : 파일들이 들어 있는 경로
        
        Output
        ------
        dict (key: 기준년월, value: 보고서 데이터프레임)
        
        Example
        -------
        rpt = load_rpt_all('data')
    """
    
    # 기준년월 생성 및 데이터 목록 유효성 검증
    m = re.compile('^시산표_\d{8}.xlsx$')
    data = [f for f in os.listdir(folderpath) if m.search(f)]
    enddate_list_data = list(map(lambda x: x[4:12], data))
    enddate_list_data.sort()
    start_enddate, end_enddate = enddate_list_data[0], enddate_list_data[-1]
    start_year, start_month = int(start_enddate[:4]), int(start_enddate[4:-2])
    end_year, end_month = int(end_enddate[:4]), int(end_enddate[4:-2])
    enddate_list = generate_enddate((start_year, start_month), (end_year, end_month))
    if enddate_list_data != enddate_list:
        raise('생성된 기준년월 리스트와 데이터 목록상 기준년월말일 불일치')

    # 데이터 로드
    tb = {}
    for enddate in enddate_list:
        tb[enddate[:6]] = load_tb(os.path.join(folderpath, f'시산표_{enddate}.xlsx'))
        
    return tb