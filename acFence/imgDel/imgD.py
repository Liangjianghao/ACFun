#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/12/29 18:14
# @Author : LiangJiangHao
# @Software: PyCharm
import photomosaic as pm
from PIL import Image
imgPath='F:\ACFun\\acFence\imgDel\\2.jpg'

# im = Image.open(imgPath).convert('RGB')
# # 图片的宽度和高度
# w, h = im.size
# print(w,h)

image = pm.imread(imgPath)
# print(image)
pool = pm.make_pool('F:\ACimg\*.jpg')
print(type(pool))
mosaic = pm.basic_mosaic(image,pool,(10,10))
pm.imsave('save.jpg',mosaic)