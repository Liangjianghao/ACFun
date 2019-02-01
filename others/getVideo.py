#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/1 21:00
# @Author : LiangJiangHao
# @Software: PyCharm
import os
import requests
import json
for x in range(1,1000):
    url='https://apipc.app.acfun.cn/v2/user/content?app_version=5.11.1&market=appstore&origin=ios&pageNo=%s&pageSize=20&resolution=750x1334&sort=0&status=2&sys_name=ios&sys_version=12.1.2&type=0&userId=1378895'%x
    headers={
        'deviceType':'0',
    }
    response=requests.get(url,headers=headers,verify=False).content
    res_json=json.loads(response)
    videoArr=res_json['vdata']['list']
    if len(videoArr)==0:
        break
    else:
        for video in videoArr:
            print(video['title'])