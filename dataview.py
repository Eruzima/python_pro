# -*- codeing =utf-8 -*-
# @Time : 5/26/2022 10:35 AM
# @Author : Eru
# @File : dataview.py
# @Software : PyCharm

import numpy as np
import pandas
import json
import os
from pyecharts.charts import *
from pyecharts import options as opts


def main():
    champions = pandas.read_excel("LOL全英雄.xls")
    all_regions_en, all_regions, nums_by_reg, names, regions, nums, regions_hero = get_date(champions)
    introduction = ['这就是比尔吉沃特的仁慈', '艾欧里亚，昂扬不灭',
                    '我赐予这片土地，被我征服的荣幸', '虚空万岁',
                    '以敌人之血，祭我大诺克萨斯', '巨神已死，凡人永存',
                    '德玛西亚，武运必彰', '欢迎来到祖安',
                    '为了皮尔特沃夫', '见识下暗影岛之力吧',
                    '荣耀归于恕瑞玛', '为了弗雷尔卓德',
                    '一日为班德尔炮手，终身为班德尔炮手', '灾难始终慢我一步']
    colors = ['#66FFCC', '#00FF33', '#CCFFCC', '#660099',
              '#CCCCCC', '#0033CC', '#999999', '#009900',
              '#FFCC00', '#003300', '#CC9900', '#0099FF',
              '#66FF00', '#66CCFF']
    tab = Tab()
    allregion(tab, all_regions, nums_by_reg,regions_hero)
    heroes(tab, names, nums)
    region(tab, all_regions_en, all_regions, names, regions, nums, introduction, colors)
    tab.render_notebook()
    tab.render('eru.html')

def get_date(champions):
    all_regions_en = []
    all_regions = []
    dic_all_regions = {}
    if os.path.exists("regions.json"):
        with open(r'regions.json', 'r', encoding='utf-8') as f:
            dic_all_regions = json.load(f)
    for k, v in dic_all_regions.items():
        all_regions_en.append(k)
        all_regions.append(v)
    print(all_regions)

    names = []
    for name in champions['名字']:
        names.append(name)
    print(names)

    regions = []
    for region in champions['属地']:
        regions.append(region)
    print(regions)

    nums = []
    for stories in champions['小说及其作者']:
        num = 0
        for i in stories:
           if i == '(':
              num += 1
        nums.append(num)
    print(nums)

    nums_by_reg = [0 for i in range(0,len(all_regions))]
    region_num = 0
    for region in regions:
        for all_region in all_regions:
            if region == all_region:
                index = all_regions.index(all_region)
                nums_by_reg[index] += nums[region_num]
        region_num +=1
    print(nums_by_reg)

    regions_hero = []
    for all_region in all_regions:
        region_hero = 0
        for region in regions:
            if region == all_region:
                region_hero += 1
        regions_hero.append(region_hero)

    return all_regions_en, all_regions, nums_by_reg, names, regions, nums, regions_hero



def allregion(tab,all_regions,nums_by_reg,regions_hero):
    region = (
        Bar( init_opts = opts.InitOpts(
                    width="1000px",
                    height="650px",
                    theme='walden',
                    bg_color='black'
            )
        )
            .add_xaxis(all_regions)
            .add_yaxis('英雄数', regions_hero, category_gap="40%")  # 传入Y轴的值(列表)
            .set_global_opts(title_opts=opts.TitleOpts(title='Welcome To the World!!!',
                                                       title_textstyle_opts=opts.TextStyleOpts(font_size=20, color='#66CCFF'),
                                                       title_link='https://yz.lol.qq.com/zh_CN/',
                                                       pos_top='5'),
                             xaxis_opts=opts.AxisOpts(name='地区', axislabel_opts={"rotate": 30},
                                                      name_textstyle_opts=opts.TextStyleOpts(color='#66CCFF')),
                             yaxis_opts=opts.AxisOpts(name='数量', name_textstyle_opts=opts.TextStyleOpts(color='#66CCFF')),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         textstyle_opts=opts.TextStyleOpts(color='#66CCFF')),
                             tooltip_opts=opts.TooltipOpts(is_show=True,
                                                           trigger_on="mousemove|click",
                                                           textstyle_opts=opts.TextStyleOpts(color='#66CCFF')),
                             )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True,
                                                       position='insideTop', color='black'),
                             markpoint_opts=opts.MarkPointOpts(
                                 data=[
                                     opts.MarkPointItem(type_="max", name="最大值")
                                 ]))
        )

    line =(
        Line()
            .add_xaxis(all_regions)
            .add_yaxis('小说数', nums_by_reg,linestyle_opts=opts.LineStyleOpts(width=5))
            .set_global_opts(yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='left'),
                             markpoint_opts=opts.MarkPointOpts( data=[
                                     opts.MarkPointItem(type_="max", name="最大值")]))

    )

    region.overlap(line)
    pie = (
        Pie()
            .add('小说量', [list(z) for z in zip(all_regions, nums_by_reg)], rosetype="radius",
                 radius=['40%', '70%'], center=[1100, 340])
            .set_global_opts(legend_opts=opts.LegendOpts(is_show=True, orient='vertical',
                                                         pos_right='0', item_gap=2, legend_icon='circle',
                                                         textstyle_opts=opts.TextStyleOpts(color='#66CCFF'))
                             )
    )
    grid = Grid(init_opts=opts.InitOpts(
        width='1520px',
        height="700px",
        theme='walden',
        bg_color='black',
        page_title='Eru'
    ))
    grid.add(region, grid_opts=opts.GridOpts(pos_right='50%', pos_left='50', pos_bottom='70', pos_top='65'))
    grid.add(pie, grid_opts=opts.GridOpts(pos_right='0'))
    tab.add(grid, '宇宙')

def heroes(tab, names, nums):
    all_hero = []
    for i in range(len(names)):
        hero = [names[i], nums[i]]
        all_hero.append(hero)
    all_hero.sort(key=lambda tup: tup[1])
    print(all_hero)
    x = []
    y = []
    for i in range(len(names)):
        x.append(all_hero[i][0])
        y.append(all_hero[i][1])
    bar = (
        Bar(init_opts=opts.InitOpts(
            width='1520px',
            height="700px",
            theme='walden',
            bg_color='black'
            )
        )
            .add_xaxis(x)
            .add_yaxis('小说量', y, category_gap="50%")
            .reversal_axis()
            .set_global_opts(title_opts=opts.TitleOpts(title='这个故事，还没有完结'+'(英雄数:'+str(len(x))+')',
                                                       title_textstyle_opts=opts.TextStyleOpts(font_size=20,
                                                                                               color='#00CCFF'),
                                                       title_link='https://yz.lol.qq.com/zh_CN/champions/',
                                                       subtitle='LOL全英雄',
                                                       pos_top='5'),
                             legend_opts=opts.LegendOpts(is_show=True,
                                                         textstyle_opts=opts.TextStyleOpts(color='#00CCFF')),
                             tooltip_opts=opts.TooltipOpts(is_show=True,
                                                           trigger_on="mousemove|click",
                                                           textstyle_opts=opts.TextStyleOpts(color='#00CCFF')),
                             xaxis_opts=opts.AxisOpts(name='小说数量',
                                                      name_textstyle_opts=opts.TextStyleOpts(color='#00CCFF')),
                             datazoom_opts=opts.DataZoomOpts(range_start=93, range_end=100, orient="vertical",
                                                             pos_right='10')
                             )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True,
                                                       position='right', color='#00CCFF'),
                             markline_opts=opts.MarkLineOpts(
                                 data=[
                                     opts.MarkLineItem(x=min(y), name="最小值"),
                                     opts.MarkLineItem(x=max(y), name="最大值"),
                                     opts.MarkLineItem(x=np.mean(y), name="平均值")
                                 ])
                             )
    )
    tab.add(bar, '英雄')


def region(tab, all_regions_en, all_regions, names, regions, nums, introduction, colors):
    words_num = 0
    for c in all_regions:
        regions_num = 0
        x = []
        y = []
        for i in regions:
            if i == c:
                x.append(names[regions_num])
                y.append(nums[regions_num])
            regions_num += 1
        bar = (
            Bar( init_opts=opts.InitOpts(
                    width='840px',
                    height="680px",
                    theme='walden',
                )
            )
                .add_xaxis(x)
                .add_yaxis('小说量', y, category_gap="50%")
                .reversal_axis()
                .set_global_opts(title_opts=opts.TitleOpts(title=all_regions_en[words_num]+'(英雄数:'+str(len(x))+')',
                                                           title_textstyle_opts=opts.TextStyleOpts(font_size=20,
                                                                                                   color=colors[words_num]),
                                                           title_link='https://yz.lol.qq.com/zh_CN/region/'+all_regions_en[words_num]+'/',
                                                           subtitle=introduction[words_num],
                                                           pos_top='5'),
                                 legend_opts=opts.LegendOpts(is_show=True,textstyle_opts=opts.TextStyleOpts(color=colors[words_num])),
                                 tooltip_opts=opts.TooltipOpts(is_show=True,
                                                               trigger_on="mousemove|click",
                                                               textstyle_opts=opts.TextStyleOpts(color=colors[words_num])),
                                 xaxis_opts=opts.AxisOpts(name='小说数量',
                                                          name_textstyle_opts=opts.TextStyleOpts(color=colors[words_num])),
                                 datazoom_opts=opts.DataZoomOpts(range_start=20, range_end=80,
                                                                 orient="vertical", pos_left='7')
                                 )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=True,
                                                           position='right', color=colors[words_num]),
                                 markline_opts=opts.MarkLineOpts(
                                     data=[
                                         opts.MarkLineItem(x = min(y), name="最小值"),
                                         opts.MarkLineItem(x = max(y), name="最大值"),
                                         opts.MarkLineItem(x = np.mean(y), name="平均值")
                                     ])
                                 )
        )
        pie = (
            Pie()
               .add('小说量', [list(z) for z in zip(x, y)], radius=[80, 150], center=[1150, 175])
               .set_global_opts(legend_opts=opts.LegendOpts(is_show=True, orient='vertical',
                                                            pos_right='0',item_gap=2, legend_icon='circle',
                                                            textstyle_opts=opts.TextStyleOpts(color=colors[words_num]))
                                )
        )
        words_num += 1
        words = []
        for i in range(len(x)):
            hero = (x[i], y[i])
            words.append(hero)
        wc = (
            WordCloud()
                .add("", words, word_size_range=[20, 50],pos_left='700', pos_top='220', shape='rect')
        )
        grid = Grid(init_opts = opts.InitOpts(
                    width='1520px',
                    height="700px",
                    theme='walden',
                    bg_color='black'
        ))
        grid.add(bar, grid_opts=opts.GridOpts(pos_right="40%"))
        grid.add(pie, grid_opts=opts.GridOpts(pos_left="80%", pos_top='10%'))
        grid.add(wc, grid_opts=opts.GridOpts(pos_left="80%", pos_top='90%'))
        tab.add(grid, c)
    return tab

if __name__ == "__main__":
    main()


