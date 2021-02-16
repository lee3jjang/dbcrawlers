from datetime import datetime

def pd2db(conn, data, table_name, duplicates='ignore'):
    """
        pandas DataFrame을 DB에 insert 하는 utility
        사전에 db에 테이블이 있어야 함

        :params conn: DB connector
        :params data: DataFrame
        :params table_name str: 테이블명
        :params str duplicates: 중복 데이터 처리방법(ignore|replace)

        Example
        -------
        >> company_codes = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')[0][['회사명', '종목코드']]
        >> company_codes.종목코드 = company_codes.종목코드.map('{:06d}'.format)
        >> pd2db(cur, company_codes[['회사명', '종목코드']], 'replace')
    """

    if duplicates.upper() not in ['IGNORE', 'REPLACE']:
        raise Exception('duplicates 입력 오류')
    cols = data.shape[1]
    cur = conn.cursor()
    tmp = [df.values for _, df in data.iterrows()]
    cur.executemany(f'INSERT OR {duplicates.upper()} INTO {table_name.upper()} VALUES(?' + ',?'*(cols-1) + ')', tmp)
    conn.commit()