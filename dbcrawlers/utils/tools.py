import os
import glob
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def convert_to_csv(path, filename, dtype=None):
    """
        Example
        -------
        >> convert_to_csv('data', '연동수수료_특약보종별_출재보험료') 
    """
    
    files = glob.glob(f'{path}/{filename}*.xlsx')
    result = []
    for f in files:
        data = pd.read_excel(f, dtype=dtype)
        result.append(data)
    tmp = pd.concat(result)
    tmp.to_csv(f'{path}/{filename}.csv', index=False)
    
def validate_uniqueness(df, group, var):
    """
        Description
        -----------
        데이터프레임 내 그룹별 변수가 유일하게 정의되는지를 판별합니다.
        
        Parameters
        ----------
        df : 검사할 데이터프레임
        group : 그룹핑할 변수
        var : 검사할 변수
        
        Example
        -------
        >> validate_uniqueness(contract, '증권번호', '증권개시일')    
    """

    if type(group) == list:
        x = df[group + [var]].drop_duplicates().groupby(group).size()
    else:
        x = df[[group, var]].drop_duplicates().groupby(group).size()
    return x[x>1].index

def generate_yearmonth(start_yyyymm, end_yyyymm, format=None):
    """
        Description
        -----------
        기준년월 리스트 생성
        
        Example
        -------
        >> yyyymm_list = generate_yyyymm("201701", "201912")
    """
    
    start_year, start_month = int(start_yyyymm[:4]), int(start_yyyymm[4:])
    end_year, end_month = int(end_yyyymm[:4]), int(end_yyyymm[4:])
    yyyymm_list = []
    year_month = datetime(start_year, start_month, 1)
    while(year_month <= datetime(end_year, end_month, 1)):
        if type(format) == type(None):
            yyyymm_list.append(year_month)
        else:
            yyyymm_list.append(year_month.strftime(format))
        year_month += relativedelta(months=1)
    return yyyymm_list

def generate_enddate(start_yyyymm, end_yyyymm, typ=1):
    """
        Description
        -----------
        기준년월말일자 리스트를 %Y%m%d 형식으로 생성
        
        Example
        -------
        enddate_list = generate_enddate((2017, 1), (2019, 12)) 
    """

    (start_year, start_month), (end_year, end_month) = start_yyyymm, end_yyyymm
    enddate_list = []
    year_month = datetime(start_year, start_month, 1)
    while(year_month <= datetime(end_year, end_month, 1)):
        enddate = year_month + relativedelta(months=1, days=-1)
        if typ==1:
            enddate_list.append(enddate.strftime('%Y%m%d'))
        elif typ==0:
            enddate_list.append(enddate)
        year_month += relativedelta(months=1)
    return enddate_list