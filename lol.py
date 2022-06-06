# -*- codeing =utf-8 -*-
# @Time : 5/23/2022 9:53 AM
# @Author : Eru
# @File : lol.py
# @Software : PyCharm

import urllib.request,urllib.response
import xlwt
import json

def main():
#获得索引
    baseurl = "https://yz.lol.qq.com/v1/zh_cn/search/index.json"
    js = askurl(baseurl)
    index = json.loads(js)
#获得信息
    regions = get_regions(index)
    save_regions(regions)
    champions, num = get_champions(index, regions)
    champions, num = new_champions(champions, num, "祖安花火", "泽丽", "zeri", "祖安", "射手", "2022-01-05", '"这里是我的归属，也是大家的归属"', "意料之外的火花(作者：Michael Luo)")
    champions, num = new_champions(champions, num, "炼金男爵", "烈娜塔·戈拉斯克", "renata glasc", "祖安", "辅助", "2022-02-01", '"我们不一定要当敌人，让我来改变你的看法"', "分秒不差(作者：Dana Luery Shaw)")
    champions, num = new_champions(champions, num, "虚空女皇", "贝尔维斯", "Bel’Veth", "虚空之地", "战士", "2022-05-20", '"这个世界永远不会被遗忘，由我，噬母的孩子取而代之。"', "风车(作者：Jared Rosen)")
    champions = update_champions(champions, "annie", "魔眼与余烬", "Conor Sheehy")
    champions = update_champions(champions, "talon", "陌生旅人", "Brooke Jaffe")
    champions = update_champions(champions, "pantheon", "战争之殇", "L J Goulding")
    champions = update_champions(champions, "vex", "苦难的意义", "John O’bryan")
    champions = update_champions(champions, "sona", "脆弱的馈赠", "Dana Luery Shaw")
    champions = update_champions(champions, "taric", "星体中的脸庞", "Rowan Williams")
    champions = update_champions(champions, "malzahar", "先知的盛宴", "Jared Rosen")
    champions = update_champions(champions, "sejuani", "死亡冬日", "Graham Mcneill")
    champions = update_champions(champions, "olaf", "死亡冬日", "Graham Mcneill")
    champions = update_champions(champions, "taliyah", "裂谷的沙", "Dana Luery Shaw")
    champions = update_champions(champions, "kaisa", "裂谷的沙", "Dana Luery Shaw")
#保存信息
    savepath = "LOL全英雄.xls"
    save_champions(champions, savepath, num)

#得到地区字典
def get_regions(index):
    regions = {}
    for i in index["factions"]:
        regions[i["slug"]]= i["name"]
    regions["unaffiliated"] = "符文之地"
    print(regions)
    return regions

def save_regions(regions):
    x = json.dumps(regions,ensure_ascii=False)
    print(x)
    with open('regions.json', 'w', encoding = 'utf-8') as f:
        f.write(x)
    f.close()

#添加一个英雄
def new_champions(champions, num, no, name,slug, region, roles, date, word, stories):
    champion = [no, name, slug, region, roles, date, word, stories]
    champions.append(champion)
    print(champion)
    num += 1
    return champions, num

#更新一个英雄的小说
def update_champions(champions, name, story, author):
    for i in champions:
        if i[2] == name:
            i[7] = i[7] + "    " + story + '(作者：' + author + ')'
    return champions

#得到所有英雄数据
def get_champions(index, regions):
    champions = []
    num = 0
    for i in index['champions']:
        champions.append(get_champion(i["slug"], regions))
        num += 1
    return champions, num

#得到单个英雄数据
def get_champion(name,regions):
    url = "https://yz.lol.qq.com/v1/zh_cn/champions/"+name+"/index.json"
    js = askurl(url)
    if name == "gnar":
        js = js[:18384] + ',' + js[18384:]
    all = json.loads(js)

    hero = all["champion"]
    modules = all["modules"]
    champion = []

    champion.append(hero["title"])
    champion.append(hero["name"])
    champion.append(all["id"])
    for k, v in regions.items():
        if hero["associated-faction-slug"] == k:
            champion.append(v)
    roles = ""
    for i in hero["roles"]:
        role = str(i["name"]) + "  "
        roles += role
    roles = roles[0:-2]
    champion.append(roles)
    champion.append(hero["release-date"][0:10])
    champion.append(hero["biography"]["quote"])
    stories = ""
    for i in modules:
        if i["type"] == "story-preview":
            if str(i["subtitle"])[-1] == "著":
                story = str(i["title"]) + "(作者：" + str(i["subtitle"])[0:-1] + ")    "
            else:
                story = str(i["title"]) + "("+str(i["subtitle"]) + ")    "
            stories += story
    stories = stories[0:-4]
    if len(stories) == 0:
        stories = "这是一个孤儿!"
    champion.append(stories)
    print(champion)
    return champion

#保存数据
def save_champions(champions, savepath, num):

    book = xlwt.Workbook(encoding = "utf-8", style_compression = 0)
    sheet = book.add_sheet('LOL全英雄', cell_overwrite_ok = True)
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Microsoft YaHei'
    style.font = font
    col = ("称号", "名字", "英文名", "属地", "角色定位", "登录日期", "引言", "小说及其作者")
    for i in range(0, 8):
        sheet.write(0, i, col[i], style)

    for i in range(0, num):
        champion = champions[i]
        for j in range(0, 8):
            if j == 2:
                sheet.write(i + 1, j, champion[j].title(), style)
            else:
                sheet.write(i + 1, j, champion[j], style)

    book.save(savepath)

#发送url请求
def askurl(url):
    head = {
        "user-agent" : "Mozilla / 5.0 (Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 100.0.4896.60 Safari / 537.36"
    }
    request = urllib.request.Request(url, headers=head)
    json = ""
    try:
        response = urllib.request.urlopen(request)
        json = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return json

if __name__ == "__main__":
    main()
