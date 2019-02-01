#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/2 20:18
# @Author : LiangJiangHao
# @Software: PyCharm

import pymysql
import os
import sys
import time
import datetime
from dateutil import parser
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
baseTable='db_xiju'
tableName='db_xijuPX'
baseTime='2008-5-1'
import json
# CREATE TABLE `fencePX` (
#       `Id` INT(11) NOT NULL AUTO_INCREMENT,
#       `userid` INT(11) NOT NULL COMMENT '用户id',
#       `userImg` VARCHAR(255) DEFAULT NULL COMMENT '用户头像',
#       `user_name` VARCHAR(255) DEFAULT NULL COMMENT'用户名',
#       `followed` INT(11) DEFAULT NULL COMMENT '粉丝数',
#       `video_uploadtime` date DEFAULT NULL COMMENT '上传时间',
#       PRIMARY KEY (`Id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='粉丝结果表';
connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='acfun',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)
cursor = connect.cursor()

def getinfor(timeStr):

    # sql = "SELECT * FROM %s  WHERE video_uploadtime<='%s' ORDER BY allPlayNum desc "%(baseTable,timeStr)
    sql='SELECT * FROM %s WHERE video_uploadtime<"%s" ORDER BY followed DESC LIMIT 20'%(baseTable,timeStr)
    print(sql)
    cursor.execute(sql)
    connect.commit()
    data = cursor.fetchall()
    return data

datetime_start = parser.parse(baseTime)
nowTime = datetime.datetime.now()  # 现在
def getFollowed(userid):
    # videoId='609656'
    url = 'https://apipc.app.acfun.cn/v2/user/content/profile?app_version=5.10.2&market=appstore&origin=ios&resolution=750x1334&sys_name=ios&sys_version=12.0&userId=%s' % userid
    header_dict = {'deviceType': '0'}
    response = requests.get(url, headers=header_dict, verify=False).content
    result = json.loads(response)
    fenceNum = result['vdata']['followed']
    return fenceNum


while datetime_start<nowTime:
    datetime_start = datetime_start + datetime.timedelta(days=5)
    print('处理时间段%s'%(datetime_start))
    videoArr=getinfor(datetime_start)
    print(len(videoArr))
    for index,video in enumerate(videoArr):
        try:
            userid = video['userid']
            userImg = video['userImg']
            user_name = video['user_name']
            followed = video['followed']
            if int(followed)>10000:
                followed=getFollowed(userid)
            video_uploadtime = video['video_uploadtime']
            sql = "insert into %s(userid,userImg,user_name,followed,video_uploadtime)values ('%s','%s', '%s','%s','%s')" % (tableName,userid,userImg,user_name,followed,datetime_start)
            # insertStr = "replace into DB_xiju (title,movie_id,rate,url,cover,uploadTime) values ('%s','%s', '%s','%s','%s','%s')" % (item['title'], item['id'], item['rate'], item['url'], item['cover'], item['uploadTime'])
            cursor.execute(sql)
        except Exception as e:
            continue


