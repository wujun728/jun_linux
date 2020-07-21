""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# -*- coding:utf-8 -*-
# 导入cv模块
import os
import cv2 as cv
"""
安装以下模块
pip install --upgrade setuptools
pip install numpy Matplotlib
pip install opencv-python
"""
# 读取图像，支持 bmp、jpg、png、tiff 等常用格式
# r 显式声明字符串不用转义
img = cv.imread(os.getcwd()+"\\images\\heying.jpg")
# 创建窗口并显示图像
cv.namedWindow("Image")
cv.imshow("Image", img)
cv.waitKey(0)


