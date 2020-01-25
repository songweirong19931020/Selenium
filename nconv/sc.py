"""
@File : sc.py
@copyright : GG
@Coder: Leslie_s
@Date: 2020/1/25
"""
import requests
from lxml import html
import pandas as pd
import time
import pandas as pd
import datetime
import re
def new_load():
    headers = {

        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange',

        'accept-encoding':'gzip, deflate, br',

        'accept-language':'zh-CN,zh;q=0.8',
        'upgrade - insecure - requests': '1',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',# 需要填写

        }
    url = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0'
    r = requests.get(url, headers=headers,timeout=15,allow_redirects=False)
    r.encoding='utf-8'
    t1 = html.fromstring(r.text)
    pattern = r'{("cityName")(.+?)}'
    pattern1=r'{"(.+?)},'
    gg=re.findall(pattern,r.text)

    df = pd.DataFrame(gg)
    # df.to_csv('resulta.csv',columns=['城市','qznm','zynum','dednum'])
    df['city'] = df.loc[:,1].str.extract('([\u4e00-\u9fa5]{2,9})')

    df['确诊人数'] = df.loc[:,1].str[5:29]
    df['qzhm']=df.loc[:,['确诊人数']].astype('str')
    df['qznm']=df['qzhm'].str.extract('(\d{1,4})')

    df['治愈人数'] = df.loc[:,1].str[55:65]
    df['zy']=df.loc[:,['治愈人数']].astype('str')
    df['zynum']=df['zy'].str.extract('(\d{1,4})')

    df['死亡人数'] = df.loc[:,1].str[71:78]
    df['ded']=df.loc[:,['死亡人数']].astype('str')
    df['dednum']=df['ded'].str.extract('(\d{1,4})')
    df1 = df.loc[:,['city','qznm','zynum','dednum']]
    df1['create_time']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    list_reslut=[]
    for i in range(0,5):
        print('排名第'+str(i+1)+'城市为'+ str(df1['city'][i]+'***;确诊人数为'+ str(df1['qznm'][i])+'例；***;治愈人数为'
                             +  str(df1['zynum'][i])+'例；***;死亡人数为'+ str(df1['dednum'][i])))
        list_reslut.append('排名第'+str(i+1)+'城市为'+ str(df1['city'][i]+'***;确诊人数为'+ str(df1['qznm'][i])+'例；***;治愈人数为'
                             +  str(df1['zynum'][i])+'例；***;死亡人数为'+ str(df1['dednum'][i])))
    qg_qz = t1.xpath('//*[@class="confirmedNumber___3WrF5"]/span/span[1]/text()')
    qg_ys = t1.xpath('//*[@class="confirmedNumber___3WrF5"]/span/span[2]/text()')
    qg_zy = t1.xpath('//*[@class="confirmedNumber___3WrF5"]/span/span[3]/text()')
    qg_sw = t1.xpath('//*[@class="confirmedNumber___3WrF5"]/span/span[4]/text()')
    content = '全国确诊'+str(qg_qz)+'例;疑似'+ str(qg_ys)+'例;治愈'+str(qg_zy)+'例;死亡'+str(qg_sw)+'例;'+str(list_reslut).replace('[|]','')

    api = "https://sc.ftqq.com/SCU74542Tc98dcd7c67352195b034704430382be45e0ad688aa02d.send"

    title = "武汉疫情通报"
    data = {

    "text":title,

    "desp":content

    }

    req = requests.post(api,data = data)


    import pymysql as pm
    for row in df1.itertuples():
        conn = pm.connect(host='localhost', user='root', password='root', database='mydb', charset='utf8')
        cur = conn.cursor()
        sql = "insert into mydb.new_conv(city,qznm,zynum,dednum,create_time)\
                     values ({},{},{},{},{});".format('"' + str(getattr(row, 'city')) + '"',
                                                      '"' + str(getattr(row, 'qznm')) + '"',
                                                      '"' + str(getattr(row, 'zynum')) + '"',
                                                      '"' + str(getattr(row, 'dednum')) + '"',
                                                      '"' + str(getattr(row, 'create_time')) + '"',
                                                      )
        # cur.execute(sql)
        print(sql)
        cur.execute(sql)
        # print(row)
        cur.close()
        # commit 提交
        conn.commit()
        # 关闭MySQL链接
        conn.close()