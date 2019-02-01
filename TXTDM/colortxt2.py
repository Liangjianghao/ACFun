#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/28 20:38
# @Author : LiangJiangHao
# @Software: PyCharm
# -*- coding:utf-8 -*-
import os
from PIL import Image, ImageFont, ImageDraw
import argparse

# 命令行输入参数处理
# parser = argparse.ArgumentParser()
# parser.add_argument('file')
# parser.add_argument('-o','--output')

# 获取参数
# args = parser.parse_args()
# File = args.file
# OUTPUT = args.output

ascii_char = list(u"ABCDEF")


# 将像素转换为ascii码
def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ''
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256) / length
    return ascii_char[int(gray / unit)]


if __name__ == '__main__':
    im = Image.open("input.jpg", "r")
    WIDTH = int(im.width / 6)  # 高度比例为原图的1/6较好，由于字体宽度
    HEIGHT = int(im.height / 15)  # 高度比例为原图的1/15较好，由于字体高度
    im_txt = Image.new("RGB", (im.width, im.height), (231, 223, 223))
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
    txt = ""
    colors = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            pixel = im.getpixel((j, i))
            colors.append((pixel[0], pixel[1], pixel[2]))  # 记录像素颜色信息
            if (len(pixel) == 4):
                txt += get_char(pixel[0], pixel[1], pixel[2], pixel[3])
            else:
                txt += get_char(pixel[0], pixel[1], pixel[2])
        txt += '\n'
        colors.append((0, 0, 0))
    dr = ImageDraw.Draw(im_txt)
    font = ImageFont.load_default().font  # 获取字体
    x = y = 0
    # 获取字体的宽高
    font_w, font_h = font.getsize(txt[1])
    font_w *= 0.8
    font_h *= 0.7  # 调整后更佳

    # ImageDraw为每个ascii码进行上色
    for i in range(len(txt)):
        if (txt[i] == '\n'):
            x += font_h
            y = -font_w
        dr.text([y, x], txt[i], colors[i])
        y += font_w
    # 输出
    im_txt.save("output.png", encoding='utf-8')
