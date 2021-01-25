import codecs  # 用来存储爬取到的信息
from pybloom_live import ScalableBloomFilter  # 用于URL去重的
import requests  # 用于发起请求，获取网页信息
import json  # 处理json格式的数据
from bs4 import BeautifulSoup as bs  # 用于数据抽取
import time, datetime
import re  # 正则语言类库
import os
def savenews(data, new,m,d):
    fp = codecs.open('C:/Users/lsz/Desktop/概率论大作业/' +m+d+'/'+ new + '.txt', 'a+', 'utf-8')
    fp.write(json.dumps(data, ensure_ascii=False))
    fp.close()
def toTimeStamp(timeStr):
    return int(time.mktime(time.strptime(timeStr,"%Y-%m-%d %H:%M:%S")))
def getdetailpagebybs(url,mo,da):
    page = requests.get(url).content  # 使用requests.get方法获取网页代码，由于bs4可以自动解码URL的编码，所以此处不需要decode
    html = bs(page, "html.parser")  # 使用lxml解析器
    title = html.find(class_="main-title")
    date_source = html.find(class_="keywords")
    if "疫情"  in date_source.text:
        print(date_source.text)
        print(title.text)
        artibody = html.find(class_="article")  # 使用find方法，获取新闻网页中的article信息
        print(artibody.text)
        savenews(artibody.text,title.text,mo,da)
    elif "肺炎" in date_source.text:
        print(date_source.text)
        print(title.text)
        artibody = html.find(class_="article")  # 使用find方法，获取新闻网页中的article信息
        print(artibody.text)
        savenews(artibody.text,title.text,mo,da)
#2/27 1582732800 2/28 1582819200
def newscopy(m,d):
    if m == "12":
        etimeStr = '2019-'+m+'-'+d+' 00:00:00'
    else:
        etimeStr = '2020-'+m+'-'+d+' 00:00:00'
    etimeStamp = toTimeStamp(etimeStr)
    stimeStamp = etimeStamp+86400
    date = "2019-12-22"
    url = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&etime="+str(etimeStamp)+"&stime="+str(stimeStamp)+\
          "&ctime=1609067810&date="+date+"&k=&num=50&page="
    page = 0
    while page <5 :
        data = requests.get(url+str(page))
        if data.status_code == 200:
            data_json = json.loads(data.content)
            news = data_json.get("result").get("data")  # 获取result节点下data节点中的数据，此数据为新闻详情页的信息
            # 从新闻详情页信息列表news中，使用for循环遍历每一个新闻详情页的信息
            for new in news:
                try:
                    print("go")
                    getdetailpagebybs(new["url"],m,d)
                except Exception as e:
                    print("error")
        page +=1

for month in ["12","01","02","03","04","05","06"]:
    for day in ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28"]:
        path = 'C:/Users/lsz/Desktop/概率论大作业/'
        os.mkdir(path+'./'+month+day)
        newscopy(month,day)