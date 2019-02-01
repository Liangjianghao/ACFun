# -*-coding:utf-8
import os
import sys
import requests
import re
import time
import pymysql
import datetime
import json

# CREATE TABLE `danceZW` (
#   `Id` int(11) NOT NULL AUTO_INCREMENT,
#   `video_title` varchar(255) DEFAULT NULL COMMENT '视频标题',
#   `video_url` varchar(255) DEFAULT NULL COMMENT '视频地址',
#   `video_author` varchar(255) DEFAULT NULL COMMENT '视频作者',
#   `video_uploadtime` datetime DEFAULT NULL COMMENT'视频上传时间',
#   `playNum` int(11) DEFAULT NULL COMMENT '播放',
#   `danmuNum` int(11) DEFAULT NULL COMMENT '弹幕数',
#   `comments` int(11) DEFAULT NULL COMMENT '评论数',
#   `saveNum` int(11) DEFAULT NULL COMMENT '收藏数',
#   `xjNum` int(11) DEFAULT NULL COMMENT '香蕉数',
#   PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a站宅舞表';

yesterDay = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')


def insertChatContent(videoUrl, playNum, danmuNum, comments, saveNum, xjNum):
    # 连接数据库
    connect = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='acfun',
        charset='utf8mb4'
    )
    # 获取游标
    cursor = connect.cursor()
    sql = "INSERT INTO dance (videoUrl,playNum,danmuNum,comments,saveNum,xjNum) VALUES ('%s','%s', '%s','%s','%s','%s')" % (
    videoUrl, playNum, danmuNum, comments, saveNum, xjNum)
    print(sql)
    cursor.execute(sql)
    connect.commit()

with open('daceUrl.txt') as fileOpen:
    data=fileOpen.readlines()
print('需要解析%s条视频数据'%len(data))

UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
headers = {"User-Agent": UA, 'X-Requested-With': 'XMLHttpRequest'}
for index,url in enumerate(data):
    # url = 'http://www.acfun.cn/v/ac4383824'
    try:
        print('正在解析第%s条视频数据：%s'%(str(index+1),url))
        userInfoUrl='http://webapi.aixifan.com/query/user?userId=13215999'
        id = url.split('/ac')[1]
        detailUrl = 'http://www.acfun.cn/content_view.aspx?contentId=%s' % id
        response = requests.get(detailUrl,headers=headers).content
        jsonData = json.loads(response)
        # print(jsonData)
        playNum = jsonData[0]
        danmuNum = jsonData[4]
        contenNum = jsonData[1]
        saveNum = jsonData[5]
        xjNum = jsonData[6]
        insertChatContent(id, playNum, danmuNum, contenNum, saveNum, xjNum)
    except  Exception as e:
        print('报错 %s'%e)
        continue
    # time.sleep(0.5)