import re
import bs4
import urllib.request
import urllib.parse
import json
import xlwt
import sqlite3
from bs4 import BeautifulSoup
import os
import xlrd
import openpyxl
import jieba
import jieba.analyse

f=open("C:/Users/ROG/Desktop/data/情感词典/情感词典.txt",'r',encoding="utf-8")
emotion_list=f.read().split()
f.close()

f=open("C:/Users/ROG/Desktop/data/情感词典/积极.txt",'r',encoding="utf-8")
positive=f.read().split()
f.close()

f=open("C:/Users/ROG/Desktop/data/情感词典/消极.txt",'r',encoding="utf-8")
negetive=f.read().split()
f.close()

f=open("C:/Users/ROG/Desktop/data/心态维度/愉快.txt",'r',encoding="utf-8")
happy=f.read().split()
f.close()

f=open("C:/Users/ROG/Desktop/data/心态维度/惊喜.txt",'r',encoding="utf-8")
suprise=f.read().split()
f.close()

f=open("C:/Users/ROG/Desktop/data/心态维度/感动.txt",'r',encoding="utf-8")
moved=f.read().split()
f.close()

f=open("C:/Users/ROG/Desktop/data/心态维度/担忧.txt",'r',encoding="utf-8")
worry=f.read().split()
f.close()

f=open("C:/Users/ROG/Desktop/data/心态维度/悲伤.txt",'r',encoding="utf-8")
sadness=f.read().split()
f.close()


#用于过滤掉爬取下来的数据中的特殊符号和英文字母以及数字，便于之后关键词的筛选
def format_text(txt):
    for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890' :
        txt = txt.replace(ch, " ")
    return txt


#运用jieba库将爬取的文本分词，以便之后心态词的提取
path="C:/Users/ROG/Desktop/data/数据.txt"
file=open(path,'r',encoding="utf-8")
content=file.read()
#读取之后过滤掉除了汉字外的其他字符
content=format_text(content)
#利用jieba.analyse计算分词的tf-idf值
tfidf=jieba.analyse.extract_tags(content,topK=1000,withWeight=True)
file.close()
#利用jieba将文本分词
words=jieba.lcut(content)
#建立字典对应词频
counts={}
for word in words:
    if len(word) == 1:  #单个字不计算在内
        continue
    else:
        counts[word] = counts.get(word, 0) + 1 #遍历所有词语，每出现一次其对应的值加1
items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序



#整合数据
f=open("C:/Users/ROG/Desktop/data/关键词.txt",'w+',encoding="utf-8")
for i in range(len(items)):
    word, count = items[i]
    if word in emotion_list:
        f.write(word)
        f.write(" ")
        f.write(str(count))
        f.write('\n')
f.close()


#按文件层次整合
file_path="C:/Users/ROG/Desktop/data/新闻内容/"
files=os.listdir(file_path)
all_data=open("C:/Users/ROG/Desktop/data/新闻内容/data.txt",'w+',encoding="utf-8")
for i in files:
    path=file_path+"/"+i
    content_files=os.listdir(path)
    for j in content_files:
        real_path=path+"/"+j
        f=open(real_path,'r',encoding="utf-8")
        content=f.read()
        content=format_text(content)
        all_data.write(content)
        f.close()
all_data=open("C:/Users/ROG/Desktop/data/新闻内容/data.txt",'r+',encoding="utf-8")
text=all_data.read()



#统计数据
sum=0
positive_num=0
negetive_num=0
happy_num=0
suprise_num=0
moved_num=0
worry_num=0
sadness_num=0
annoyed_num=0
#第一个if语句是过滤掉分词中除了心态词词典外的其他词
#遍历所有的分词，并将分词与各个维度的心态词碰撞，统计占比和词频
for i in range(0,len(tfidf)):
    if tfidf[i][0] in emotion_list:
        #分词碰撞成功，就加词频
        if tfidf[i][0] in positive:
            positive_num+=counts[tfidf[i][0]]
        if tfidf[i][0] in negetive:
            negetive_num += counts[tfidf[i][0]]
        if tfidf[i][0] in happy:
            happy_num+=counts[tfidf[i][0]]
        if tfidf[i][0] in suprise:
            suprise_num+=counts[tfidf[i][0]]
        if tfidf[i][0] in moved:
            moved_num+=counts[tfidf[i][0]]
        if tfidf[i][0] in worry:
            worry_num+=counts[tfidf[i][0]]
        if tfidf[i][0] in sadness:
            sadness_num+=counts[tfidf[i][0]]
        #sum是统计的总的心态词词频
        sum+=counts[tfidf[i][0]]
        print("Term:{0:<10}  Frequency:{1:<10}  Tf-Idf:{2:>10}".format(tfidf[i][0],counts[tfidf[i][0]],tfidf[i][1]))
print("{0} {1}".format(positive_num,negetive_num))
#积极心态词和消极心态词在心态词中的占比
print("积极心态占比：{}".format(positive_num/sum))
print("消极心态占比：{}".format(negetive_num/sum))
#各个维度心态词的词频
print("{0} {1} {2} {3} {4}".format(happy_num,suprise_num,moved_num,worry_num,sadness_num))



#绘图
import matplotlib.pyplot as plt
import numpy as np

#中文和负号的正常显示
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 使用ggplot的绘图风格
plt.style.use('ggplot')

# 构造数据
x_list=[]
y_list=[]
# f=open("C:/Users/ROG/Desktop/data/关键词.txt",'r',encoding="utf-8")
# lines=f.readlines()
# for line in lines:
#     data=line.split()
#     x_list.append(int(data[1]))
#     y_list.append(data[0])
# f.close()
N=len(x_list)
# 设置雷达图的角度，用于平分切开一个圆面
angles = np.linspace(0, 2 * np.pi, N, endpoint=False)


# 绘制雷达图
fig = plt.figure()
# 这里一定要设置为极坐标格式
ax = fig.add_subplot(111, polar=True)
# 绘制折线图
ax.plot(angles, x_list, 'o-', linewidth=2)
# 填充颜色
ax.fill(angles, x_list, alpha=0.25)
# 添加每个特征的标签
ax.set_thetagrids(angles * 180 / np.pi, y_list)
# 设置雷达图的范围
ax.set_ylim(0,250)
# 添加标题
plt.title('第四阶段多维情绪解析')
# 添加网格线
ax.grid(True)
# 显示图形
plt.savefig('polar_demo.png')
plt.show()


# 绘制坐标系
plt.xlabel('keyword')
plt.ylabel('frequency')
plt.title("square of 'x'")
plt.plot(x_list,y_list)
plt.show()


#绘制饼图
data = [0.854,0.146]
labels = ['积极','消极']

#用于突出重点
explode = [0,0.25]

# 将横、纵坐标轴标准化处理，保证饼图是一个正圆，否则为椭圆
plt.axes(aspect='equal')

# 自定义颜色
colors=['#9999ff','#ff9999','#7777aa','#2442aa','#dd5555'] # 自定义颜色

# 绘制饼图
plt.pie(x=data,  # 绘图数据
    explode = explode,  # 突出重点
    labels = labels,  # 添加绘制的标签
    colors = colors,  # 设置饼图的自定义填充色
    autopct = '%.1f%%',  # 设置百分比的格式，这里保留一位小数
    )

# 添加图标题
plt.title('有序复工阶段(20.3.10——20.6)总体心态分布')

# 保存图形
plt.savefig('pie_demo.png')
plt.show()
