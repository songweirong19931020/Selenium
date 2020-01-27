"""
@File : jump.py
@copyright : GG
@Coder: Leslie_s
@Date: 2020/1/26
"""
import requests
from lxml import html
import pandas as pd
import time
import pandas as pd
import datetime
import re
import json

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
doc = r.text
test_com = r'(?P<first>"provinceName":"[\u4e00-\u9fa5]{1,9}"),(?P<second>"provinceShortName":"[\u4e00-\u9fa5]{1,9}"),(?P<three>"confirmedCount":\d{1,9})'
iter_dict = {}
gg_a = r'provinceName":(?P<first>"[\u4e00-\u9fa5]{1,9}"),"provinceShortName":(?P<second>"[\u4e00-\u9fa5]{1,9}"),"confirmedCount":(?P<three>\d{1,9})'
r=re.finditer(gg_a,doc)
train =  re.findall(gg_a,doc)
for i in r:
    print(i.group(1))
    provinceName=i.group(1)
    provinceShortName=i.group(2)
    confirmedCount=i.group(3)
    iter_dict.setdefault( provinceShortName,confirmedCount)
#
# result = re.finditer(test_com,r.text)
# for i in result:
#     print(i.group(1))
#
# search = re.finditer(test_com, r.text)
# print('group 0:', search.group(0))
# list_provincename=[]
# list_confircount=[]
# for match in matches_pro:
#     print(match.group(1))
#     list_provincename.append(match.group(1))
# for match in matches_confirmedCount:
#     print(match.group(1))
#     list_confircount.append(match.group(1))
#
# dic_result = dict(zip(list_confircount,list_provincename))
#
