"""
@File : pyecharts.py
@copyright : GG
@Coder: Leslie_s
@Date: 2020/1/27
"""
# 导入Geo包，注意1.x版本的导入跟0.x版本的导入差别
from pyecharts.charts import Geo
# 导入配置项
from pyecharts import options as opts
# ChartType：图标类型，SymbolType：标记点类型
from pyecharts.globals import ChartType, SymbolType

# geo = Geo()
#
# # 地图类型，世界地图可换为world
# geo.add_schema(maptype="china")
# # 添加数据点
# geo.add("ChartType.HEATMAP", train, type_=ChartType.EFFECT_SCATTER)
# # 添加流向，type_设置为LINES，涟漪配置为箭头，提供的标记类型包括 'circle', 'rect', 'roundRect', 'triangle',
# # 'diamond', 'pin', 'arrow', 'none'
# # geo.add("geo-lines",
# #         [("上海", "广州"),
# #          ("上海", "新疆"),
# #          ("上海", "哈尔滨"),
# #          ("成都", "北京"),
# #          ("哈尔滨", "广州")],
# #         type_=ChartType.LINES,
# #         effect_opts=opts.EffectOpts(symbol=SymbolType.ARROW, symbol_size=5, color="yellow"),
# #         linestyle_opts=opts.LineStyleOpts(curve=0.2),
# #         is_large=True)
# # 不显示标签
# geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
# # 设置图标标题，visualmap_opts=opts.VisualMapOpts()为左下角的视觉映射配置项
# geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True), title_opts=opts.TitleOpts(title="Geo-Lines"))
# # 直接在notebook里显示图表
# geo.render_notebook()
# # 生成html文件，可传入位置参数
# geo.render("mychart1111.html")
#

'''
制作地图之前需要安装依赖包
pip install echarts-countries-pypkg 
pip install echarts-china-provinces-pypkg 
pip install echarts-china-cities-pypkg 
pip install echarts-china-counties-pypkg 
pip install echarts-china-misc-pypkg
pip install echarts-cities-pypkg---扩展包，用的时候在装

'''

###MAP###
from pyecharts.charts import Map,Geo
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
#将数据处理成列表
def map_img():
    import requests
    from lxml import html
    import pandas as pd
    import time
    import pandas as pd
    import datetime
    import re
    import json

    headers = {

        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange',

        'accept-encoding': 'gzip, deflate, br',

        'accept-language': 'zh-CN,zh;q=0.8',
        'upgrade - insecure - requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    # 需要填写

    }
    url = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0'
    r = requests.get(url, headers=headers, timeout=15, allow_redirects=False)
    r.encoding = 'utf-8'
    t1 = html.fromstring(r.text)
    doc = r.text
    for_map = r'"provinceShortName":(?P<second>"[\u4e00-\u9fa5]{1,9}"),"confirmedCount":(?P<three>\d{1,9})'
    train = re.findall(for_map, doc)
    map_1 = Map()
    map_1.set_global_opts(
        title_opts=opts.TitleOpts(title="2020年全国各省疫情分部"),
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
    pieces=[
            {"max": 100, "min": 0, "label": "0-100人"},
            {"max": 200, "min": 100, "label": "100-200人"},
            {"max": 1000, "min": 200, "label": "200-1000人"},
            {"max": 100000, "min": 1000, "label": "1000人以上"},
        ],

                                          )) #最大数据范围,
    ###归一化数据，将数据处理成echarts想要的格式
    name=[]
    count=[]
    for key,vaules in dict(train).items():
        name.append(str(key).replace('"',''))
        count.append(int(vaules))
    list2 = [[name[i],count[i]] for i in range(len(name))]
    map_1.set_series_opts(label_opts=opts.LabelOpts(is_show=False),label_pos='inside', is_label_show=True,
        is_map_symbol_show=False,    # 是否显示地图标记红点，默认为 True
        is_more_utils=True)
    map_1.add("2020年全国各省疫情",list2,maptype="china")
    map_1.render('yq.html')
    make_snapshot(snapshot, map_1.render(), "2020全国疫情报表.png")
    ###将数据导出为png


###数据转换为LINE平滑###
from pyecharts.charts  import Line
from pyecharts import options as opts
from pyecharts.faker import Faker
import requests
from lxml import html
import pandas as pd
import time
import pandas as pd
import datetime
import re
import pymysql as pm
def summary_qg():
    headers = {

        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange',

        'accept-encoding': 'gzip, deflate, br',

        'accept-language': 'zh-CN,zh;q=0.8',
        'upgrade - insecure - requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    # 需要填写

    }
    url = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=timeline&isappinstalled=0'
    r = requests.get(url, headers=headers, timeout=15, allow_redirects=False)
    r.encoding = 'utf-8'
    t1 = html.fromstring(r.text)
    qg_qz = t1.xpath('//*[@class="mapTop___2VZCl"]/p[2]/span/span[1]/span/text()')
    qg_ys = t1.xpath('//*[@class="mapTop___2VZCl"]/p[2]/span/span[2]/span/text()')
    qg_zy = t1.xpath('//*[@class="mapTop___2VZCl"]/p[2]/span/span[4]/span/text()')
    qg_sw = t1.xpath('//*[@class="mapTop___2VZCl"]/p[2]/span/span[3]/span/text()')
    qg_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    df_qg = pd.DataFrame(qg_qz)
    df_qg.columns=['qz']
    df_qg['ys']=qg_ys
    df_qg['zy']=qg_zy
    df_qg['sw']=qg_sw
    df_qg['create_time']=qg_time

    for row in df_qg.itertuples():
        conn = pm.connect(host='localhost', user='root', password='root', database='mydb', charset='utf8')
        cur = conn.cursor()
        sql = "insert into mydb.summary_cony(qz,ys,sw,zy,create_time)\
                     values ({},{},{},{},{});".format('"' + str(getattr(row, 'qz')) + '"',
                                                      '"' + str(getattr(row, 'ys')) + '"',
                                                      '"' + str(getattr(row, 'sw')) + '"',
                                                      '"' + str(getattr(row, 'zy')) + '"',
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


###画Line
a =Line()
a.add_xaxis(['2019-01-01'])
a.add_yaxis("全国确诊", qg_qz, is_smooth=True)
a.add_yaxis("全国死亡", qg_sw, is_smooth=True)
a.set_global_opts(title_opts=opts.TitleOpts(title="Line-smooth"))
a.render('ceshi.html')