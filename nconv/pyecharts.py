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


###MAP###
from pyecharts.charts import Map,Geo
from pyecharts import options as opts
#将数据处理成列表
map_1 = Map()
map_1.set_global_opts(
    title_opts=opts.TitleOpts(title="2019年全国各省疫情分部"),
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
###将数据导出为png
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot
make_snapshot(snapshot, map_1.render(), "2020全国疫情报表.png")