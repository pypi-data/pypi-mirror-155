#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: opencv2 基础操作
import math
import numpy as np
import cv2


def rotate(image, angle, scale=1.0):
    """
    旋转图片(此方法只适合于小角度旋转，旋转90/180/270请调用 #rotate_90/#rotate_180/#rotate_270)
    :param image: 图片
    :param angle: 角度
    :param scale: 缩放比例
    :return:
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    m = cv2.getRotationMatrix2D(center, angle, scale)
    # rotated = cv2.warpAffine(image, m, (w, h))
    rotated = cv2.warpAffine(image, m, (w, h), borderValue=(255, 255, 255))

    return rotated


def rotate_270(image):
    """
    顺时针旋转270度（即：逆时针旋转90度）
    :param image:
    :return:
    """
    return np.rot90(image)


def rotate_180(image):
    """
    旋转180度
    :param image:
    :return:
    """
    img270 = np.rot90(image)
    return np.rot90(img270)


def rotate_90(image):
    """
    顺时针旋转90度（np.rot90为逆时针）
    :param image:
    :return:
    """
    img270 = np.rot90(image)
    img180 = np.rot90(img270)
    return np.rot90(img180)


def get_position_after_rotate(x, y, center_x, center_y, angle):
    """
    获取坐标点经过旋转后的新坐标
    计算原理：旋转是围绕中心点进行的（即：圆弧角），因此，要下计算x，y分别的旋转旋转半径
    三角函数的操作参考：https://docs.python.org/zh-cn/3/library/math.html#math.radians
    :param x: x
    :param y: y
    :param center_x: 旋转中心点X
    :param center_y: 旋转中心点Y
    :param angle: 旋转点角度
    :return:
    """
    # 旋转半径（即为：中心点跟该点的距离，勾股定理）
    # 与中心点的距离
    distance_x = abs(center_x - x)
    distance_y = abs(center_y - y)
    radius = pow(distance_x, 2) + pow(distance_y, 2)
    radius = np.sqrt(radius)

    sin = distance_y / radius
    src_angle = math.degrees(math.asin(sin))
    # 注意，此处的尺寸，越往下Y越大，越往右边X越大（与正常的）
    # print(f"原始角度：{src_angle},当前相对坐标：{x - center_x},{y - center_y}")
    if y > center_y:
        if x < center_x:
            src_angle = 180 - src_angle
        # print(f"点位于中心坐标【左下角】,角度:{src_angle}")
        # else:
        #     print(f"点位于中心坐标【右下角】,角度:{src_angle}")
    else:
        if x > center_x:
            src_angle = 360 - src_angle
            # print(f"点位于中心坐标【右上角】,角度:{src_angle}")
        else:
            src_angle = 180 + src_angle
            # print(f"点位于中心坐标【左上角】,角度:{src_angle}")
    final_angle = src_angle - angle
    return get_rount_point_by_angle(center_x, center_y, radius, final_angle)


def get_rount_point_by_angle(center_x, center_y, radius, angle):
    """
    获取指定中心点/半径的圆上，任意一点的坐标
    与正常的坐标系不一样，此处越下面，Y越大，主要却分
    :param center_x:
    :param center_y:
    :param radius:
    :param angle:
    :return:
    """
    from math import cos, sin, pi

    x = radius * cos(angle * pi / 180)
    y = radius * sin(angle * pi / 180)
    # print(f'角度：{angle},x:{x}/{y}')
    x1 = center_x + x
    y1 = center_y + y
    return [round(x1), round(y1)]


# 转灰度图：gray(x,y) = 0.299r(x,y) + 0.587g(x,y) + 0.114b(x,y)
def gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# 二值图
def birany(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    show_img(gray, 'gray')
    ret, birany_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return birany_img


# 通道拆分
def split(img):
    bule, green, red = cv2.split(img)
    # cv2.imshow('原始', img)
    # cv2.imshow('image_R', red)
    # cv2.imshow('image_G', green)
    # cv2.imshow('image_B', bule)
    # cv2.waitKey(-1)
    return bule, green, red


# 通道合并
def merge(b, g, r):
    return cv2.merge([b, g, r])


def show_img(img, title='CV_SHOW_IMG'):
    cv2.imshow(title, img)
    cv2.waitKey(-1)
    cv2.destroyAllWindows()


def judge_rotate(img_path):
    """
    判断图片表格的倾斜角度（方式1，后续是否可以参ocr返回的文字来识别角度？）
    :param img_path:
    :return:
    """
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    if len(lines) == 0:
        return 0
    angle = 0
    useful_line_count = 0
    for line in lines:
        rho, theta = line[0]  # line[0]存储的是点到直线的极径和极角，其中极角是弧度表示的
        a = np.cos(theta)  # theta是弧度
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))  # 直线起点横坐标
        y1 = int(y0 + 1000 * a)  # 直线起点纵坐标
        x2 = int(x0 - 1000 * (-b))  # 直线终点横坐标
        y2 = int(y0 - 1000 * a)  # 直线终点纵坐标
        # 倾斜的角度（取平均角度）
        t = float(y2 - y1) / (x2 - x1) if x2 != x1 else 0
        rotate_angle = math.degrees(math.atan(t))
        # 只能矫正30度以内度的线条
        if abs(rotate_angle) > 30:
            print(f"蓝色直线角度：{rotate_angle}忽略该线条")
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            continue
        print(f"红色直线角度：{rotate_angle}")
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        if rotate_angle < 0:
            rotate_angle = abs(rotate_angle)
        angle += rotate_angle
        useful_line_count += 1


def remove_red_stamp(image):
    """
    去除红色印章(容易误伤浅色字体)
    :param img:
    :return:
    """
    bule, green, red = split(image)
    # 多传入一个参数cv2.THRESH_OTSU，并且把阈值thresh设为0，算法会找到最优阈值
    thresh, ret = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 实测调整为95%效果好一些
    filter_condition = int(thresh * 0.95)

    _, red_thresh = cv2.threshold(red, filter_condition, 255, cv2.THRESH_BINARY)

    # 把图片转回 3 通道
    result_img = np.expand_dims(red_thresh, axis=2)
    result_img = np.concatenate((result_img, result_img, result_img), axis=-1)
    return result_img


def check_red(image_path):
    """抠红色（只有在白底黑字的情况下效果才比较好）
    HSV颜色空间
    """
    # https://zhuanlan.zhihu.com/p/95952096 定义的颜色范围 (0,43,35) 到 (10,255,255) AND (156,43,35) 到 (180,255,255)
    # https://blog.csdn.net/kakiebu/article/details/79476235 定义的颜色范围 (0,43,46) 到 (10,255,255) AND (156,43,46) 到 (180,255,255)

    # TODO 效果欠佳，后续再来看
    start_s = 60
    start_v = start_s - 8

    red1 = np.array([0, start_s, start_v])
    red2 = np.array([10, 255, 255])
    image = cv2.imread(image_path)
    cv2.imshow("src", image)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, red1, red2)
    print(mask.shape)
    cv2.imshow("red", mask)

    red_y_arr, red_x_arr = np.where(mask > 0)
    red_points = [
        (int(x), int(y)) for x, y in zip(red_x_arr, red_y_arr)
    ]
    # 转灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    for point in red_points:
        gray[point[1]][point[0]] = 0

    cv2.imshow("remove_red", gray)
    # 转二进制
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -2)
    cv2.imshow("binary", binary)

    # 第二范围先不用
    # red3 = np.array([156, start_s, start_v])
    # red4 = np.array([180, 255, 255])
    # hsv2 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # mask2 = cv2.inRange(hsv2, red3, red4)
    #
    # #  合并两个取色结果，重新生成mask
    # final_mask = conbine_mask(mask, mask2)
    # cv2.imshow("final", final_mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def conbine_mask(mask1, mask2):
    """
    合并两个mask中的255
    :param mask1:
    :param mask2:
    :return:
    """
    hei, win = mask1.shape
    # 转为1纬度
    mask1 = mask1.reshape(1, -1)[0]
    mask2 = mask2.reshape(1, -1)[0]
    final_list = []
    add_count = 0
    for (index, num) in enumerate(mask1):
        if num == 255 or mask2[index] == 255:
            final_list.append(255)
            add_count += 1
        else:
            final_list.append(0)
    print("acc_count:" + str(add_count))
    final_mask = np.array(final_list, dtype=np.uint8)
    final_mask = final_mask.reshape(hei, -1)
    print("===合并后的图")
    print(final_mask.shape)
    print(final_mask.size)
    return final_mask


if __name__ == '__main__':
    # img_path = "../data/table/img/倾斜表格/倾斜表格3.jpg"
    # img = cv2.imread(img_path)
    # rotate_img = rotate(img, 30)
    # cv2.imshow("旋转后", rotate_img)
    # cv2.waitKey(-1)
    # path = '/Users/chenjianghai/job/YR/2021/审计三期/数据/承装电力设施许可证_全国/1.jpeg'
    # images = cv2.imread(path)
    # images = remove_red_stamp(images)
    # cv2.imshow("红色印章", images)
    # cv2.waitKey(-1)
    # cv2.destroyAllWindows()
    # path = '/Users/chenjianghai/job/YR/2021/审计三期/数据/承装电力设施许可证_全国/1.jpeg'
    path = '../data/table/img/经费决算报告-国网福龙岩供电公司_1.jpg'
    check_red(path)

if __name__ == '__main2__':
    """
    合并图片示例
    """
    padding_width = 100
    padding_height = 10
    img1 = cv2.imread('../debug_10/1.png')
    rows1, cols1, deep1 = img1.shape
    print(f"图片1尺寸:{img1.shape}")
    img2 = cv2.imread('../debug_10/2.png')
    rows2, cols2, deep2 = img2.shape
    print(f"图片2尺寸:{img2.shape}")

    all_hei = rows1 + rows2 + padding_height * 2
    all_widht = cols1 + cols2 + padding_width * 2
    print(f"新图片尺寸:{all_hei}、{all_widht}")

    # 生成指定大小的空白图片
    import numpy as np

    final_matrix = np.zeros((all_hei, all_widht, 3), np.uint8)
    # 复制每张图片到汇总到图片上
    imgs = [img1, img2]
    start_row = 0
    start_col = 0
    current_row_cell_size = 0
    for img in imgs:
        rows1, cols1, deep1 = img.shape
        end_row = start_row + rows1
        end_col = start_col + cols1
        print(f"当前图片区域:{start_row}:{end_row};{start_col}:{end_col}")
        final_matrix[start_row:end_row, start_col:end_col] = img
        start_col = end_col + padding_width
        start_row = end_row + start_row
    cv2.imshow("合并", final_matrix)
    cv2.waitKey(-1)
    cv2.destroyAllWindows()
