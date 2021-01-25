import json
import time
import random
import requests
import pprint
import pandas as pd
import openpyxl
import xlwt
import re


url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E7%96%AB%E6%83%85%E5%A4%8D%E5%B7%A5&page_type=searchall&page={}"

# 获取十页的数据
for i in range(50):
    page = i
    response = requests.get(url.format(page))
    # 数据转化为json数据结构
    data= response.json()
    datalist = []
    # pprint.pprint(data)
    # 提取出评论列表
    cards = data['data']['cards']
    for mid in cards:
        # 判断有无 mblog 有就打印，没有就None
        if mid.get('mblog',None):
            id = mid['mblog']['mid']

            # 服务器返回内容，用变量接受
            response = requests.get(
                "https://m.weibo.cn/comments/hotflow?id={id}&mid={id}&max_id_type=0".format(id=id))
            # 字典数据
            data = response.json()

            users = data.get('data', None)
            if users:
                users = users['data']

            if users:
                for user in users:
                    text = user['text']
                    id = user['user']['id']
                    name = user['user']['screen_name']
                    text = ''.join(re.findall('[\u4e00-\u9fa5]',text))
                    # print(text)
                    # print(id)
                    # print(name)
                    datalist.append({
                        # "用户ID": str(id),
                        # "用户名称": name,
                        "评论信息": text.replace("<a href='", "").replace("/n", "").replace("</a>", "").replace('<span class="url-icon">',"")
                    })

    df = pd.DataFrame(datalist)
    index = i
    df.to_excel("评论信息第五次{index}.xlsx".format(index=index))
    time.sleep(5)
