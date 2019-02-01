#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/27 15:03
# @Author : LiangJiangHao
# @Software: PyCharm
from PIL import Image
import os

def is_img(ext):
    ext = ext.lower()
    if ext == '.jpg':
        return True
    elif ext == '.png':
        return True
    elif ext == '.jpeg':
        return True
    elif ext == '.bmp':
        return True
    else:
        return False

thePath='F:\ACFun\\acFence\imgDel\ACimg'
listArr=os.listdir(thePath)

for file in listArr:
    try:
        filePath=thePath+'/'+file
        if is_img(os.path.splitext(filePath)[1]):
            print(filePath)
            im = Image.open(filePath).convert('RGB')
            # 图片的宽度和高度
            w,h = im.size
            print(w)
            region = im.crop((0, 0, 50, 50))
            region.save(filePath)
    except Exception as e:
        print(e)
        continue
