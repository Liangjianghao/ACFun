#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/27 23:46
# @Author : LiangJiangHao
# @Software: PyCharm

import scrapy
import os
import requests
import json
from scrapy.http import Request
import pymysql
from scrapy.spider import Spider
from acfun.items import AcfunItem
import time
import random
user_agent_list = [ \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

#
# connect = pymysql.Connect(
#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     passwd='123456',
#     db='ac_up',
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor
#
# )
# cursor = connect.cursor()
# def insertChatContent(userid,userImg,user_name,followed,bananaGold):
#     # 连接数据库
#     connect = pymysql.Connect(
#         host='127.0.0.1',
#         port=3306,
#         user='root',
#         passwd='123456',
#         db='ac_up',
#         charset='utf8mb4'
#     )
#     # 获取游标
#     cursor = connect.cursor()
#     sql="REPLACE into up_baseInfor (userid,userImg,user_name,followed,bananaGold)  values ('%s','%s', '%s','%s','%s')"%(userid,userImg,user_name,followed,bananaGold)
#     print(sql)
#     time.sleep(100)
#     cursor.execute(sql)
#     connect.commit()
# ******************************************************************
class Myspider(scrapy.Spider):
    name='acfun'
    allowed_domains=['https://apipc.app.acfun.cn']
    base_url='https://apipc.app.acfun.cn/v2/user/content/profile?app_version=5.10.2&market=appstore&origin=ios&resolution=750x1334&sys_name=ios&sys_version=12.0&userId=1'

    def start_requests(self):
        # for x in range(250000, 14500000):

        for x in range(11000000, 15000000):
            ua = random.choice(user_agent_list)
            self.headers = {
                # 'User-Agent': 'AcFun/5.10.2 (iPhone; iOS 12.0; Scale/2.00)',
                'User-Agent': ua,
            }
            url = 'https://apipc.app.acfun.cn/v2/user/content/profile?app_version=5.10.2&market=appstore&origin=ios&resolution=750x1334&sys_name=ios&sys_version=12.0&userId=%s' % x
            yield Request(url,headers=self.headers,callback=self.parse)
    def parse(self,response):
        # print(response.text)
        try:
            result = json.loads(response.text)
            iterm=AcfunItem()
            userid=result['vdata']['userId']
            userImg=result['vdata']['userImg']
            userName=result['vdata']['username']
            fenceNum=result['vdata']['followed']
            bananaGold=result['vdata']['bananaGold']
            sqlStr='%s,%s,%s,%s,%s'%(userid,userImg,userName,fenceNum,bananaGold)
            # print(sqlStr)
            # print(userName)
            if '\\' in userName:
                userName = userName.replace("\\", "\\\\")
            if "'" in userName:
                userName=userName.replace("'","\\'")
            if '"' in userName:
                userName = userName.replace('"', '\\"')
            if 'jpg' not in userImg:
                userImg=''
            print('正在抓取第%s条数据:%s,%s,%s,%s'%(userid,userid,userName,fenceNum,bananaGold))
            # insertChatContent(userid,userImg,userName,fenceNum,bananaGold)
            # print(userName)
            iterm['userId']=userid
            iterm['userImg']=userImg
            iterm['userName']=userName
            iterm['fenceNum']=fenceNum
            iterm['bananaGold']=bananaGold
            yield iterm
        except Exception as e:
            print('parseException:%s'%e)
            # time.sleep(10)
            # return

# from scrapy.http import Request,FormRequest
#
# class Myspider(scrapy.Spider):
#     name = 'acfun'
#     allowed_domains = ['https://apipc.app.acfun.cn']
#     header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  #设置浏览器用户代理
#
#     base_url='https://apipc.app.acfun.cn/v2/user/content/profile?app_version=5.10.2&market=appstore&origin=ios&resolution=750x1334&sys_name=ios&sys_version=12.0&userId=1'
#
#     def start_requests(self):
#         """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
#         print('第一次请求cookie')
#         print('********************************************')
#         base_url = 'https://apipc.app.acfun.cn/v2/user/content/profile?app_version=5.10.2&market=appstore&origin=ios&resolution=750x1334&sys_name=ios&sys_version=12.0&userId=1'
#
#         return [Request('https://account.app.acfun.cn/api/account/signin/normal',meta={'cookiejar':1},callback=self.parse)]
#
#     def parse(self, response):
#         print('相应cookie')
#         print('************************************')
#         Cookie1 = response.headers.getlist('Set-Cookie')                            #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
#         print('后台首次写入的响应Cookies：',Cookie1)
#
#         data = {                                                                    # 设置用户登录信息，对应抓包得到字段
#             'app_version': '5.10.2',
#             'cid': 'yU3geLTsD8vriBzy',
#             'market': 'appstore',
#             'origin': 'ios',
#             'resolution': '750x1334',
#             'sys_name': 'ios',
#             'sys_version': '12.0',
#             'username': '13152510458',
#             'password': 'l31415926'
#         }
#
#         print('登录中....!')
#         """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
#         # return [Request(
#         #                   url='https://account.app.acfun.cn/api/account/signin/normal',                        #真实post地址
#         #                   meta={'cookiejar':response.meta['cookiejar']},
#         #                   headers=self.header,
#         #                   formdata=data,
#         #                   callback=self.next,
#         #                                   )]
#
#         ACsession = requests.session()
#         response = ACsession.post('https://account.app.acfun.cn/api/account/signin/normal', data=data,verify=False).content
#         print(response)
#         print(ACsession.cookies.get_dict())
#         cookieData = json.dumps(ACsession.cookies.get_dict())
#         print(cookieData)
#
#     def next(self,response):
#         # 请求Cookie
#         Cookie2 = response.request.headers.getlist('Cookie')
#         print('登录时携带请求的Cookies：',Cookie2)
#
#         jieg = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息
#         print('登录响应结果：',jieg)
#
#         print('正在请需要登录才可以访问的页面....!')
#         for x in range(4778902, 6000000):
#             time.sleep(1000)
#             url = 'https://apipc.app.acfun.cn/v2/user/content/profile?app_version=5.10.2&market=appstore&origin=ios&resolution=750x1334&sys_name=ios&sys_version=12.0&userId=%s' % x
#             yield Request(url,headers=self.headers,meta={'cookiejar':True},callback=self.next2)
#         # yield Request('http://dig.chouti.com/user/link/saved/1',meta={'cookiejar':True},callback=self.next2)
#     def next2(self,response):
#         # print(response.text)
#         try:
#             result = json.loads(response.text)
#             iterm=AcfunItem()
#             userid=result['vdata']['userId']
#             userImg=result['vdata']['userImg']
#             userName=result['vdata']['username']
#             fenceNum=result['vdata']['followed']
#             bananaGold=result['vdata']['bananaGold']
#             sqlStr='%s,%s,%s,%s,%s'%(userid,userImg,userName,fenceNum,bananaGold)
#             # print(sqlStr)
#             # print(userName)
#             if '\\' in userName:
#                 userName = userName.replace("\\", "\\\\")
#             if "'" in userName:
#                 userName=userName.replace("'","\\'")
#             if '"' in userName:
#                 userName = userName.replace('"', '\\"')
#             if 'jpg' not in userImg:
#                 userImg=''
#             print('正在抓取第%s条数据:%s,%s,%s,%s'%(userid,userid,userName,fenceNum,bananaGold))
#             # insertChatContent(userid,userImg,userName,fenceNum,bananaGold)
#             # print(userName)
#             iterm['userId']=userid
#             iterm['userImg']=userImg
#             iterm['userName']=userName
#             iterm['fenceNum']=fenceNum
#             iterm['bananaGold']=bananaGold
#             yield iterm
#         except Exception as e:
#             print('parseException:%s'%e)
#             time.sleep(10)
#             return

# 带cookieJar
# import scrapy
# from scrapy.http import Request,FormRequest
#
# class PachSpider(scrapy.Spider):                            #定义爬虫类，必须继承scrapy.Spider
#     name = 'acfun'                                           #设置爬虫名称
#     allowed_domains = ['app.acfun.cn']                 #爬取域名
#     # start_urls = ['http://edu.iqianyue.com/index_user_login.html']     #爬取网址,只适于不需要登录的请求，因为没法设置cookie等信息
#
#     header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  #设置浏览器用户代理
#
#     def start_requests(self):       #用start_requests()方法,代替start_urls
#         """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
#         base_url = 'https://apipc.app.acfun.cn/v2/user/content/profile?app_version=5.10.2&market=appstore&origin=ios&resolution=750x1334&sys_name=ios&sys_version=12.0&userId=1'
#         login_url='http://www.acfun.cn/login/?returnUrl=http://www.acfun.cn/member/#area=post-history'
#         return [Request(login_url,meta={'cookiejar':1},callback=self.parse)]
#
#     def parse(self, response):     #parse回调函数
#
#         data = {                                                                    # 设置用户登录信息，对应抓包得到字段
#             'app_version': '5.10.2',
#             'cid': 'yU3geLTsD8vriBzy',
#             'market': 'appstore',
#             'origin': 'ios',
#             'resolution': '750x1334',
#             'sys_name': 'ios',
#             'sys_version': '12.0',
#             'username': '13152510458',
#             'password': 'l31415926'
#         }
#
#         # 响应Cookie
#         Cookie1 = response.headers.getlist('Set-Cookie')   #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
#         print(Cookie1)
#
#         print('登录中')
#         """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
#         return [scrapy.FormRequest(
#                                           url='https://account.app.acfun.cn/api/account/signin/normal',   #真实post地址
#                                           meta={'cookiejar':response.meta['cookiejar']},
#                                           # headers=self.header,
#                                           formdata=data,
#                                           callback=self.next,
#                                           )]
#     def next(self,response):
#         print('************************************************************')
#         print('next')
#         a = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息
#         print(a)
#         Cookie1 = response.headers.getlist('Set-Cookie')   #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
#         print(Cookie1)
#         """登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
#         # yield Request('http://www.acfun.cn/member/#area=post-history',meta={'cookiejar':True},callback=self.next2)
#
#         for x in range(10000000, 10100000):
#             url = 'https://apipc.app.acfun.cn/v2/user/content/profile?app_version=5.10.2&market=appstore&origin=ios&resolution=750x1334&sys_name=ios&sys_version=12.0&userId=%s' % x
#             yield Request(url,meta={'cookiejar':True},callback=self.next2)
#     def next2(self,response):
#         # 请求Cookie
#         # Cookie2 = response.request.headers.getlist('Cookie')
#         # print(Cookie2)
#         try:
#             result = json.loads(response.text)
#             iterm=AcfunItem()
#             userid=result['vdata']['userId']
#             userImg=result['vdata']['userImg']
#             userName=result['vdata']['username']
#             fenceNum=result['vdata']['followed']
#             bananaGold=result['vdata']['bananaGold']
#             sqlStr='%s,%s,%s,%s,%s'%(userid,userImg,userName,fenceNum,bananaGold)
#             # print(sqlStr)
#             # print(userName)
#             if '\\' in userName:
#                 userName = userName.replace("\\", "\\\\")
#             if "'" in userName:
#                 userName=userName.replace("'","\\'")
#             if '"' in userName:
#                 userName = userName.replace('"', '\\"')
#             if 'jpg' not in userImg:
#                 userImg=''
#             print('正在抓取第%s条数据:%s,%s,%s,%s'%(userid,userid,userName,fenceNum,bananaGold))
#             # insertChatContent(userid,userImg,userName,fenceNum,bananaGold)
#             # print(userName)
#             # iterm['userId']=userid
#             # iterm['userImg']=userImg
#             # iterm['userName']=userName
#             # iterm['fenceNum']=fenceNum
#             # iterm['bananaGold']=bananaGold
#             # yield iterm
#         except Exception as e:
#             print('parseException:%s'%e)
            # time.sleep(1)
            # return
