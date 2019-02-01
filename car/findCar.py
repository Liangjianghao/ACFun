#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/27 21:34
# @Author : LiangJiangHao
# @Software: PyCharm
from io import *
from string import ascii_lowercase as al
import urllib
# def urliter() :
#     for i in range(5) :
#         print("%d/100"  % i)
#         for j in al  :
#             for k in al  :
#                 # yield "http://www.%02d%c%c%c%c.com" % (i, j, k, j, k)
#                 yield "http://www.ac%c%c%c%c.com" % ( k, j, k)

def urliter() :
    for j in al  :
        for k in al  :
            # yield "http://www.%02d%c%c%c%c.com" % (i, j, k, j, k)
            yield "http://www.ac%c%c%c%c.com" % (j,k, j, k)

logfile = open("car.txt", "w")
for u in urliter() :
    try :
        wp = urllib.request.urlopen(u)
        print("find " + u)
        logfile.write(u + "\n")
    except :
        pass
logfile.close()
