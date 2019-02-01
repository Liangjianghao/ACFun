#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/10/3 23:59
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import sys
import requests
from lxml import html
import pymysql
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import time
import random
# CREATE TABLE `doubanDM` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `title` VARCHAR(255) DEFAULT NULL COMMENT '电影名',
#   `directors` VARCHAR(255) DEFAULT NULL COMMENT '导演',
#   `rate` FLOAT DEFAULT NULL COMMENT '评分',
#   `url` VARCHAR(255) DEFAULT NULL COMMENT '地址',
#   `idnumber` INT(11) DEFAULT NULL COMMENT 'idnumber',
#   `date` DATE DEFAULT NULL COMMENT '上映日期',
#   `type` VARCHAR(255) DEFAULT NULL COMMENT '类型',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='豆瓣动漫';

connect = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='douban',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)
cursor = connect.cursor()
UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"
headers = {"User-Agent": UA}

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",

]

# headers = {'User-Agent': random.choice(user_agent)}

print(headers)
# f=open('1.html','w+b')
def getUptime(url):
    # url = 'https://movie.douban.com/subject/30337185/'
    # print(url)
    response = requests.get(url, headers=headers,verify=False).content
    # print(response)
    # f.write(response)
    # f.close()
    selector = html.fromstring(response)
    # typeSelect = selector.xpath('//*[@id="info"]/span[4]/text()')
    typeSelect = selector.xpath('//*[@id="info"]/span[contains(text(),"类型")]/following-sibling::*/text()')[0]

    # print(type(typeSelect))

    # print(typeSelect)
    movietype=typeSelect[0]
    # productInfo = selector.xpath('//*[@id="info"]/span[8]/text()')
    # productInfo = selector.xpath('//*[@id="info"]/span[contains(text(),"-")]/text()')
    productInfo = selector.xpath('//*[@id="info"]/span[contains(text(),"首播")]/following-sibling::*/text()')

    # print('1')
    if '(' in productInfo[0]:
        uptime = productInfo[0].split('(')[0]
    else:
        uptime=productInfo[0]
    if len(uptime) == 4:
        uptime = '%s-1-1' % uptime
    # print(len(productInfo))
    # print(uptime)

    return movietype,uptime

qFile=open('error.txt','w+')
with open('dm.txt',encoding='utf-8') as file:
    data=file.readlines()
print(len(data))
for index,video in enumerate(data):
    if index<=70:
        continue
    try:
        print('正在解析第%s条电影数据：%s'%(str(index+1),video))
        arr=video.split('----')
        # print(arr)
        title=arr[0]
        directors=arr[2]
        idnumber=arr[3]
        url=arr[4]
        rate=arr[1]
        type,uptime=getUptime(url.strip())
        # print(type,uptime)
        sql = 'replace into doubanDM (title,directors,rate,url,idnumber,date,type)values ("%s","%s","%s","%s","%s","%s","%s")' % (title,directors,rate,url,idnumber,uptime,type)
        # print(sql)
        cursor.execute(sql)
        connect.commit()
        time.sleep(3)
    except Exception as e:
        print(e)
        qFile.write(str(index)+'----'+url+'\n')
        continue
#1335
qFile.close()

