"""
@File : scary_conv.py
@copyright : GG
@Coder: Leslie_s
@Date: 2020/1/24
"""
import requests
from lxml import html
import pandas as pd
import time
import pandas as pd
import datetime
def load_conv():
    '''
    :param z_hz_name -汇总地区名称-大区
    :param z_s_name - 汇总地区 -城市
    :param z_qz_num - 确诊
    :param z_ys_num - 疑似

    :return:
    '''
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
    # with open ('cz.txt','a+',encoding='UTF-8') as f:
    #     f.writelines(r.text)
    #     f.close()
    re_hz = []
    result1 = []
    result2 = []
    result3 = []

    ###全国除武汉数据汇总
    for i in range(1,33):
        g = 1
        while g <= 40:
            z_hz_name= t1.xpath('//*[@class="fold___xVOZX"]' + '[' + str(i) + ']' + '/div' + '[' + str(g) + ']' + '/p[1]/text()')
            z_s_name = t1.xpath('//*[@class="fold___xVOZX"]'+'['+ str(i) +']'+'/div'+'['+ str(g) +']'+'/p[1]/span/text()')
            z_qz_num = t1.xpath('//*[@class="fold___xVOZX"]' + '[' + str(i) + ']' + '/div'+'['+ str(g) +']'+'/p[2]/text()')
            z_ys_num = t1.xpath('//*[@class="fold___xVOZX"]' + '[' + str(i) + ']' + '/div'+'['+ str(g) +']'+'/p[3]/text()')
        # s_name = t1.xpath('//*[@class="fold___xVOZX"][19]/div[1]/p[1]/text()')
            print('//*[@class="fold___xVOZX"]'+'['+ str(i) +']'+'/div'+'['+ str(g) +']'+'/p[1]/text()')
            re_hz.append(z_hz_name)
            result1.append(z_s_name)
            result2.append(z_qz_num)
            result3.append(z_ys_num)
            g+=1
    data_h = pd.DataFrame(result1)
    data_h['确诊'] = result2
    data_h['治愈'] = result3

    ###湖北数据
    hz_list = []
    hu_list1=[]
    hu_list2=[]
    hu_list3=[]
    for wh in range(1,11):
        print(t1.xpath('//*[@class="expand___wz_07"]/div/p/text()'))
        hz_list.append(t1.xpath('//*[@class="expand___wz_07"]/text()'))


        hz_sj = t1.xpath('//*[@class="expand___wz_07"]/div' + '[' +str(wh) + ']'+'/p[1]/text()')
        hb_name = t1.xpath('//*[@class="expand___wz_07"]/div' + '[' +str(wh) + ']'+'/p[1]/span/text()')
        hb_qz = t1.xpath('//*[@class="expand___wz_07"]/div' + '[' + str(wh) + ']' + '/p[2]/text()')
        hb_zy = t1.xpath('//*[@class="expand___wz_07"]/div' + '[' + str(wh) + ']' + '/p[3]/text()')
        hz_list.append(hz_sj)
        hu_list1.append(hb_name)
        hu_list2.append(hb_qz)
        hu_list3.append(hb_zy)
    data_hb = pd.DataFrame(hz_list)
    data_hb.columns =['sf_name']
    data_hb['hb_name'] = hu_list1
    data_hb['hb_qz'] = hu_list2
    data_hb['hb_zy'] = hu_list3
    data_hb['qs_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    qg_qz=t1.xpath('//*[@class="confirmedNumber___3WrF5"]/span/span[1]/text()')
    qg_ys = t1.xpath('//*[@class="confirmedNumber___3WrF5"]/span/span[2]/text()')
    qg_zy = t1.xpath('//*[@class="confirmedNumber___3WrF5"]/span/span[3]/text()')
    qg_sw = t1.xpath('//*[@class="confirmedNumber___3WrF5"]/span/span[4]/text()')
    # import re, codecs
    #
    # for row in data_hb.itertuples():
    #     file = codecs.open('5demo.xls', 'a+', 'utf-8')
    #     text = str(getattr(row, 'name')) + '\t' +str(getattr(row, 'hb_name'))  + '\t' + str(getattr(row, 'hb_qz')) + '\t' +str(getattr(row, 'hb_zy')) + '\n'
    #     file.write(text)
    #     file.close()

    content = '全国确诊'+str(qg_qz)+'例;疑似'+ str(qg_ys)+'例;治愈'+str(qg_zy)+'例;死亡'+str(qg_sw)+'例;'+str(data_hb)
    api = "https://sc.ftqq.com/SCU74542Tc98dcd7c67352195b034704430382be45e0ad688aa02d.send"

    title = "武汉疫情通报"
    data = {

    "text":title,

    "desp":content

    }

    req = requests.post(api,data = data)


    import pymysql as pm
    ###将所有数据导入mysql
    df2 = data_hb.astype(object).where(pd.notnull(data_hb), 0)
    for row in df2.itertuples():
        conn = pm.connect(host='localhost', user='root', password='root', database='mydb', charset='utf8')
        cur = conn.cursor()
        sql = "insert into mydb.concv(sf_name,hb_name,hb_qz,hb_zy,qs_time)\
                  values ({},{},{},{},{});".format('"'+str(getattr(row, 'sf_name'))+'"',
                                                   '"'+str(getattr(row, 'hb_name'))+'"',
                                                   '"' + str(getattr(row,'hb_qz')) +'"',
                                                   '"'+str(getattr(row,'hb_zy'))+'"',
                                                   '"'+str(getattr(row,'qs_time'))+'"')
        # cur.execute(sql)
        print(sql)
        cur.execute(sql)
        # print(row)
        cur.close()
        # commit 提交
        conn.commit()
        # 关闭MySQL链接
        conn.close()
        import pymysql as pm
        for row in df1.itertuples():
            conn = pm.connect(host='localhost', user='root', password='root', database='mydb', charset='utf8')
            cur = conn.cursor()
            sql = "insert into mydb.concv(sf_name,hb_name,hb_qz,hb_zy,qs_time)\
                         values ({},{},{},{},{});".format('"' + str(getattr(row, 'sf_name')) + '"',
                                                          '"' + str(getattr(row, 'hb_name')) + '"',
                                                          '"' + str(getattr(row, 'hb_qz')) + '"',
                                                          '"' + str(getattr(row, 'hb_zy')) + '"',
                                                          '"' + str(getattr(row, 'qs_time')) + '"')
            # cur.execute(sql)
            print(sql)
            cur.execute(sql)
            # print(row)
            cur.close()
            # commit 提交
            conn.commit()
            # 关闭MySQL链接
            conn.close()