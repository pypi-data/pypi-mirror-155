#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: ocr帮助类
import os
import re
from pathlib import Path
import cv2
from paddleocr.ppocr.utils.logging import get_logger

from yrocr.util.cvutil import get_position_after_rotate

logger = get_logger(name='ocr_util')
import functools
import math

current_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
TEMPLATE_PATH = os.path.join(current_dir, 'resources/templates')
POST_PROCESS_PATH = os.path.join(current_dir, 'resources/post_process')


def get_template_file_path(format_file_code):
    """
    获取识别模版路径
    :param format_file_code:
    :return:
    """
    namespace, code = split_format_file_code(format_file_code)
    return f'{TEMPLATE_PATH}/{namespace}/tpl_{code}.json' if len(
        namespace) > 0 else f'{TEMPLATE_PATH}/tpl_{code}.json'


def get_post_process_file_path(format_file_code):
    """
    获取后处理文件路径
    :param format_file_code:
    :return:
    """
    namespace, code = split_format_file_code(format_file_code)
    return f'{POST_PROCESS_PATH}/{namespace}/{code}.py' if len(
        namespace) > 0 else f'{POST_PROCESS_PATH}/{code}.py'


def split_format_file_code(format_file_code):
    """
    切割文件编码，返回namespace
    :param format_file_code:
    :return:
    """
    namespace = ''
    if format_file_code.__contains__("/"):
        index = format_file_code.index("/")
        namespace = format_file_code[0:index]
        format_file_code = format_file_code[index + 1:]

    return namespace, format_file_code


def remove_special_char(text):
    """
    去除特殊字符，包括：标点符号，ascii码小于19的
    :param text:
    :return:
    """
    text = re.sub('[\'!\"#$%&()*+,-./:;<=>?@，。?★、…【】《》？“”^！[\\]_\{\|\}（）：~\s]+', '', text)
    text = re.sub('[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+', '', text)
    return text


def get_rotate_angle(txt_result, is_fixed_format_file=False):
    """
    从OCRresult中获取倾斜角度（先从txtresult中获取）
    只获取+-30度的,且误差不能太大的，否则不进行修正（最大程度降低误差）
    :param img_path:
    :param is_format_file:
    :return: 倾斜角度，可能为负值。负值为向上翘（及：Y2 小于Y1）
    """
    sample_count = 10
    if is_fixed_format_file:
        # 如果是固定格式的电子证照识别，要以最大的字体的倾斜度为准
        # 左上、右上、右下、左下
        def compare(obj1, obj2):
            fonts1 = abs(obj1['position'][2][1] - obj1['position'][1][1])
            fonts2 = abs(obj2['position'][2][1] - obj2['position'][1][1])
            if fonts2 > fonts1:
                return 1
            elif fonts1 > fonts2:
                return -1
            else:
                return 0

        sample_count = 2
        txt_result = sorted(txt_result, key=functools.cmp_to_key(compare))
    else:
        # 按照文字长度排序，选择文字最长的一半文字最为参考
        def compare(obj1, obj2):
            if len(obj2['text']) > len(obj1['text']):
                return 1
            elif len(obj1['text']) > len(obj2['text']):
                return -1
            else:
                return 0

        txt_result = sorted(txt_result, key=functools.cmp_to_key(compare))
    txt_result = list(filter(lambda item: len('text') > 2, txt_result))
    if len(txt_result) == 0:
        return 0
    avg_angle = 0
    angles = []
    num = 0
    # 有出现0度角，则不修复
    sample_size = sample_count if len(txt_result) > sample_count else len(txt_result)
    for index in range(sample_size):
        item = txt_result[index]
        position = item['position']
        # 左上 - 右上
        ydis1 = position[1][1] - position[0][1]
        xdis1 = abs(position[1][0] - position[0][0])
        # 左下 - 右下
        ydis2 = position[2][1] - position[3][1]
        xdis2 = abs(position[3][0] - position[2][0])
        t1 = float(ydis1 / xdis1) if xdis1 > 0 else 0
        t2 = float(ydis2 / xdis2) if xdis2 > 0 else 0
        t = (t1 + t2) / 2
        rotate_angle = math.degrees(math.atan(t))
        logger.info(f"{item['text']}文字角度:{rotate_angle}")
        if rotate_angle == 0:
            logger.info(f"{item['text']}零度角，直接返回")
            return 0
        angles.append(rotate_angle)
        if abs(rotate_angle) < 30:
            avg_angle += rotate_angle
            num += 1
    if num == 0 or avg_angle == 0:
        return 0
    avg_angle = avg_angle / num
    # 如果有叫角度跟平均值过大，则忽略
    for angle in angles:
        rate = angle / avg_angle
        if rate > 5 or rate < 0.3:
            logger.info(f"角度超过偏离值：{rate},不进行纠正。当前角度：{angle},均值：{avg_angle}")
            return 0
    return avg_angle


def get_rotate_img_path(file_name, output):
    """
    获取旋转后（小角度旋转）的图片保存路径
    :param file_name: 原始文件名
    :param output: 输出路径
    :return:
    """

    # 调试模式下，保留原始的文件名
    suffix = Path(file_name).suffix
    name = Path(file_name).name
    name = name.replace(suffix, '')
    import random
    r = str(random.randint(0, 99))
    return os.path.join(output, name + "_rotate_" + r + suffix)


def get_direction_img_path(img_path, output, verbose_log=False):
    """
    获取方向翻转后的图片路径
    :param img_path:
    :param output:
    :param verbose_log:
    :return:
    """
    if verbose_log:
        # 调试模式下，保留原始的文件名
        suffix = Path(img_path).suffix
        name = Path(img_path).name
        name = name.replace(suffix, '')
        import random
        r = str(random.randint(0, 9999))
        return os.path.join(output, name + "_direction_" + r + suffix)

    else:
        import uuid
        uid = str(uuid.uuid4())
        tmp_id = ''.join(uid.split('-'))
        suffix = Path(img_path).suffix
        return os.path.join(output, tmp_id + "_direction" + suffix)


def fix_box_rotate_position(img_width, img_height, txt_result, angle):
    """
    根据旋转角度，修复ocr纯文本识别结果中的文本框坐标
    :param img_width: 图像宽度
    :param img_height: 图像高度
    :param txt_result: 文本识别结果
    :param angle: 旋转角度
    :return:
    """
    logger.info(f"校正图片旋转角度:{angle}")
    center_x = img_width / 2
    center_y = img_height / 2
    for item in txt_result:
        position = [
            get_position_after_rotate(point[0], point[1], center_x, center_y, angle)
            for point in item['position']
        ]
        # logger.info(f"旧的位置:{item['position']}")
        # logger.info(f"新的位置:{position}")
        item['position'] = position


if __name__ == '__main__':
    file_name = '123.txt'
    result = get_rotate_img_path(file_name, '/mnt')
    print(result)
