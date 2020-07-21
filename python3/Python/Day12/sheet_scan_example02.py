# -*- coding:utf-8 -*-
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import cv2 as cv

# 加载原图，可在项目imgs/example02目录下找到
img = cv.imread("test01.jpg")

# cv.resizeWindow("enhanced", 240, 280);
# 打印原图
cv.imshow("orgin", img)

# 灰度化
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 打印灰度图
cv.imshow("gray", gray)

# 高斯滤波，清除一些杂点
blur = cv.GaussianBlur(gray, (3, 3), 0)

# 自适应二值化算法
thresh2 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 131, 4)

# 打印二值化后的图
cv.imshow("thresh2", thresh2)

# 寻找轮廓
image, cts, hierarchy = cv.findContours(thresh2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# 打印找到的轮廓
print("轮廓数：", len(cts))

# 对拷贝的原图进行轮廓标记
contour_flagged = cv.drawContours(img.copy(), cts, -1, (0, 0, 255), 3)
# 打印轮廓图
cv.imshow("contours_flagged", contour_flagged)
# 按像素面积降序排序
list = sorted(cts, key=cv.contourArea, reverse=True)

# 遍历轮廓
for ct in list:
    # 周长，第1个参数是轮廓，第二个参数代表是否是闭环的图形
    peri = 0.01 * cv.arcLength(ct, True)
    # 获取多边形的所有定点，如果是四个定点，就代表是矩形
    approx = cv.approxPolyDP(ct, peri, True)
    # 只考虑矩形
    if len(approx) == 4:

        # 从原图中提取所需的矫正图片
        ox = four_point_transform(img, approx.reshape(4, 2))
        # 从原图中提取所需的矫正图片
        tx = four_point_transform(gray, approx.reshape(4, 2))

        # 打印矫正后的灰度图
        cv.imshow("tx", tx)

        # 对矫正图进行高斯模糊
        blur = cv.GaussianBlur(tx, (3, 3), 0)

        # 对矫正图做自适应二值化
        thresh2 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 131, 4)

        # 打印矫正后的二值化图
        cv.imshow("tx_thresh2", thresh2)

        # 获取轮廓
        r_image, r_cts, r_hierarchy = cv.findContours(thresh2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # 打印得到轮廓数量
        print("第二层轮廓数：", len(r_cts))

        # 用于存储答案的python list变量
        question_list = []
        for r_ct in r_cts:
            # 转为矩形，分别获取 x，y坐标，及矩形的宽和高
            x, y, w, h = cv.boundingRect(r_ct)

            # 过滤掉不符合答案坐标和长宽的选项
            if x > 2 and y > 2 and w > 20 and h > 20:
                # cv.drawContours(ox, r_ct, -1, (0, 0, 255), 1)
                question_list.append(r_ct)

        print("答案总数：", len(question_list))

        # 按坐标从上到下排序
        questionCnts = contours.sort_contours(question_list, method="top-to-bottom")[0]

        #  使用np函数，按5个元素，生成一个集合
        for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):

            # 每一个行5个答案，从左到右排序
            cnts = contours.sort_contours(questionCnts[i:i + 5])[0]

            # 存储一行题里面的每个答案
            ans_list = []
            for (j, cc) in enumerate(cnts):
                # 生成全黑画布
                mask = np.zeros(thresh2.shape, dtype="uint8")
                # 将每一个答案按轮廓写上去，并将填充颜色设置成白色
                tpp = cv.drawContours(mask, [cc], -1, 255, -1)
                # 两个图片做位运算
                mask = cv.bitwise_and(thresh2, thresh2, mask=mask)
                # 统计每个答案的像素
                total = cv.countNonZero(mask)

                # 添加到集合里面
                ans_list.append((total, j))

            # 按像素大小排序
            ans_list = sorted(ans_list, key=lambda x: x[0], reverse=True)

            max_ans_num = ans_list[0][1]
            max_ans_size = ans_list[0][0]
            print("答案序号：", max_ans_num, "列表：", ans_list)

            # 给选中答案，标记成红色
            cv.drawContours(ox, cnts[max_ans_num], -1, (0, 0, 255), 2)

        cv.imshow("answer_flagged", ox)

        # 最大的轮廓就是我们想要的，之后的就可以结束循环了
        break

# 阻塞等待窗体关闭
cv.waitKey(0)
