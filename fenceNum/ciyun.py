#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/31 23:17
# @Author : LiangJiangHao
# @Software: PyCharm

import  os
import sys
import jieba.analyse
import pymysql
connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='ac_up',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)
cursor = connect.cursor()

def selectData():
    # 连接数据库
    sql='SELECT *FROM my_fence '
    cursor.execute(sql)
    data=cursor.fetchall()
    return data

lyric= ''
# f=open('YSYX.txt','r',encoding='gbk')
# for i in f:
#   lyric+=f.read()
fenceArr= selectData()
for fence in fenceArr:
    lyric+=fence['user_name']
print(lyric)
result=jieba.analyse.textrank(lyric,topK=50,withWeight=True)
keywords = dict()
for i in result:
  keywords[i[0]]=i[1]
print(keywords)

from PIL import Image,ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
image= Image.open('3.jpg')
graph = np.array(image)
wc = WordCloud(font_path='./fonts/simhei.ttf',background_color='White',max_words=50,mask=graph)
wc.generate_from_frequencies(keywords)
image_color = ImageColorGenerator(graph)
plt.imshow(wc)
plt.imshow(wc.recolor(color_func=image_color))
plt.axis("off")
plt.show()
wc.to_file('dream.png')