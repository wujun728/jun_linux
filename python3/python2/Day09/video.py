""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# -*- coding: utf-8 -*-
import os
import cv2
import sys
import importlib
importlib.reload(sys)


def CatchUsbVideo(window_name, camera_idx):
    cv2.namedWindow(window_name)
    # 视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)
    # 告诉OpenCV使用人脸识别分类器
    classfier = cv2.CascadeClassifier(os.getcwd()+"\\haarcascade\\haarcascade_frontalface_alt2.xml")
    # 识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)
    count = 0

    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
            break
        # 将当前帧转换成灰度图像
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(faceRects) > 0:  # 大于0则检测到人脸
           count=count+1
    return count


if __name__ == '__main__':
    result = CatchUsbVideo("识别人脸区域", os.getcwd()+'\\video\\xiaojiejie.mp4')
    if result > 0:
        print('视频中有人！！')
    else:
        print('视频中无人！！')


