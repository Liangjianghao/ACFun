#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/31 22:36
# @Author : LiangJiangHao
# @Software: PyCharm

# CREATE TABLE `my_fence` (
#   `Id` INT(11) NOT NULL AUTO_INCREMENT,
#   `userid` INT(11) NOT NULL COMMENT '用户id',
#   `userImg` VARCHAR(255) DEFAULT NULL COMMENT '用户头像',
#   `user_name` VARCHAR(255) DEFAULT NULL COMMENT'用户名',
#   `signature`VARCHAR(255) DEFAULT NULL COMMENT '签名',
#   PRIMARY KEY (`Id`)
# ) ENGINE=INNODB DEFAULT CHARSET=utf8mb4 COMMENT='我的粉丝表';

import requests
import json
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

def insertChatContent(userid,userImg,user_name,signature):
    # 连接数据库
    sql="insert into my_fence (userid,userImg,user_name,signature)  values ('%s', '%s','%s','%s')"%(userid,userImg,user_name,signature)
    print(sql)
    cursor.execute(sql)
    connect.commit()

def getMyFence():

        headers={
            'cookie':'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2215d73da62fd9c8-0606423841ad3a-5d4e211f-1fa400-15d73da62fe907%22%7D; bdshare_firstime=1512471171405; Hm_lvt_bc75b9260fe72ee13356c664daa5568c=1513908197,1515983987; uuid=7054b7f721dd7d8fdb90c2d4c040ea63; analytics=GA1.2.604105877.1501587428; isOneVisit=false; did=web_aK1j0K0TANykhrrYobsnYGdevYWb; _did=web_6585289934B1F575; __guid=261359883.2815942274202437000.1537879038313.7878; _did=web_599696032CEED67D; sign_remind=1; isCloseVisit=false; mobile_conf=2ec3; session_id=3768672262197037; Hm_lvt_2af69bc2b378fb58ae04ed2a04257ed1=1546074896,1546145963,1546152133,1546162379; clientlanguage=zh_CN; ac__avi=101048931971f2d053bb707d3f3bb0537c97cebac30brpcx1c37653c25e51ec266262f5e66f786ad; supernova=1; cur_req_id=272266556AF76300_self_819124dc9a0eb1d12be6716164d9925a; cur_group_id=272266556AF76300_self_819124dc9a0eb1d12be6716164d9925a_0; stochastic=NGt3aHN2NGJqOXE%3D; acPasstoken=ChVpbmZyYS5hY2Z1bi5wYXNzdG9rZW4ScDkBjWcReo6sqAONjZnl-YZoqpLsbsI-EShYVp5kf-HTobqi3O8TRjNw5r1VRyvGvsXHwSw_uRBFYf8E-LDmN7yymq1xD8Z5qjlrZdlu-cyD1zT2h5jpwWAvxTp-UEkXVLAp45M03c6s7j60_6pWqxsaEoOWYyUQ8Zxpgde9rUJFI3Px7iIgnekrNYnuwBEKAgsdzszbBeTribuot5xDFDW22BJkcd0oBTAB; acPostHint=e79a61323ff0898f71a30fff94d314d1dea3; ac_username=%E8%B0%81%E4%B9%9F%E5%88%AB%E6%83%B3%E6%94%BE%E5%81%87; auth_key_ac_sha1=2044405668; auth_key_ac_sha1_=SdND8W+FRjoUuUQ2gKHH5+3nBBo=; auth_key=12576531; ac_userimg=http://cdn.aixifan.com/dotnet/artemis/u/cms/www/201708/18180103aga6o2te.jpg; checkEmail=1; checkMobile=1; userGroupLevel=1; checkReal=1; monitor_count=167; Hm_lpvt_2af69bc2b378fb58ae04ed2a04257ed1=1546248411; userLevel=27; online_status=18599'
        }

        for x in range(1,450):
            print('正在抓取第%s页'%x)
            getFenceUrl='http://www.acfun.cn/api/friend.aspx?name=getFollowedList&pageNo=%s&pageSize=10'%x
            response=requests.get(getFenceUrl,headers=headers).content
            # print(response)
            res_json=json.loads(response)
            fenceList=res_json['friendList']
            if len(fenceList)==0:
                return
            else:
                for fence in fenceList:
                    userId=fence['userId']
                    userName=fence['userName']
                    userImg=fence['userImg']
                    if 'signature' in fence.keys():
                        signature=fence['signature']
                    else:
                        signature=''

                    if signature=='':
                        signature

                    if '\\' in userName:
                        userName = userName.replace("\\", "\\\\")
                    if "'" in userName:
                        userName = userName.replace("'", "\\'")
                    if '"' in userName:
                        userName = userName.replace('"', '\\"')

                    if '\\' in signature:
                        signature = signature.replace("\\", "\\\\")
                    if "'" in signature:
                        signature = signature.replace("'", "\\'")
                    if '"' in signature:
                        signature = signature.replace('"', '\\"')
                    insertChatContent(userId,userImg,userName,signature)


getMyFence()