#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: OCR 固定文件（电子证照）提取
import json
import math
import os
import re
import time
from pathlib import Path

import cv2

# 需调整的角度阀值
MAX_ANGLE = 0.3
from paddleocr.ppocr.utils.logging import get_logger
from yrocr.util.cvutil import rotate, rotate_90, rotate_180, rotate_270
from yrocr.ocr_base import invoke_ocr, get_ocr_point_rect, draw_text
from yrocr.util.ocr_util import get_template_file_path, remove_special_char, fix_box_rotate_position
from yrocr.util.util import read_json
from yrocr.resources.format_file_code_converter import convert_format_file_code

import paddlex as pdx

MULTILINE_TAG = '多行'
LEFT_RIGHT_TAG = 'LEFT_RIGHT'
logger = get_logger(name='ocr_format_file')
base_path = os.path.dirname(__file__)
DEBUG_FOLDER = 'debug'
if not os.path.exists(DEBUG_FOLDER):
    os.mkdir(DEBUG_FOLDER)

# 电子证照固定文件，需要加载方向分类器
base_path = os.path.dirname(__file__)
home_path = os.path.join(Path.home(), '.yrocr')
# 方向分类器
DIRECTION_CLS_PATH = os.environ.get('DIRECTION_CLS_PATH')
if not DIRECTION_CLS_PATH:
    DIRECTION_CLS_PATH = os.path.join(base_path, 'resources/pretrain/direction_cls1')
    if not os.path.exists(DIRECTION_CLS_PATH):
        DIRECTION_CLS_PATH = os.path.join(home_path, 'pretrain/direction_cls')
from yrocr.ocr_base import parpare_pretrain

parpare_pretrain(DIRECTION_CLS_PATH)
direction_predictor = pdx.deploy.Predictor(DIRECTION_CLS_PATH)
# 目前只有指定格式的电子证件才做方向自动判断(因为模型中只有这些数据，不确定其泛化能力)
# TODO 此处需要加上 营业执照横版竖版的，或许再来加
direction_file_arr = ['train_ticket', 'vat_special_invoice', 'val_general_invoice']

# 自定义检测、识别模型所在文件夹
PERSONA_MODEL_PATH = os.environ.get('PERSONA_MODEL_PATH')
if not PERSONA_MODEL_PATH:
    PERSONA_MODEL_PATH = os.path.join(base_path, 'resources/pretrain/personal')
    if not os.path.exists(PERSONA_MODEL_PATH):
        PERSONA_MODEL_PATH = os.path.join(home_path, 'pretrain/personal')


def ocr_fixed_format_file(img_path, format_file_code, drop_score=0.5, use_show_name=True, verbose_log=False):
    """
    识别固定格式的电子证照
    整体流程：
    1.读取图片数据流
    2.判断方向，如果存在90/180/270，则旋转，得到最新图片数据流
    3.读取最新图片流高度、宽度
    4.去除红色印章（后续待做）
    5.OCR TXT 识别
    6.组装识别结果(拆分、匹配、翻译)
    :param img_path: 图片路径
    :param format_file_code: 格式编码。如：audit/safety_production_license
    :param drop_score: 丢弃的分数
    :param use_show_name: 是否使用显示名称
    :param verbose_log: 是否显示冗余日志
    :return:
    """
    start = time.time()
    if not os.path.exists(img_path):
        return error_result(1001, 'code invalid')
    # TODO 后续优化，全程改为不落盘，直接返回image？ 有需要再落盘？
    src_file_name = Path(img_path).name
    image = cv2.imread(img_path).copy()
    direction, new_image = judge_input_img_direction_cls(format_file_code, image)
    if direction:
        image = new_image
    img_hei, img_width, deep = image.shape

    # TODO 去除红色印章(后续再来,目前效果不好)
    # TODO 变形的图片需要找到固定点进行拉伸
    # 参考https://www.pythonf.cn/read/140815

    txt_result = fixed_file_ocr(image, drop_score, format_file_code)
    codes = convert_format_file_code(txt_result, format_file_code)
    if len(codes) > 1:
        final_reulst = {}
        for code in codes:
            template_file = get_template_file_path(code)
            if not os.path.exists(template_file):
                return error_result(1001, 'code invalid')
            sub_result = assembly(img_hei, img_width, src_file_name, image.copy(), code, txt_result, template_file, use_show_name, verbose_log)
            for key in sub_result:
                final_reulst[key] = sub_result[key]
        logger.info(f'total elapse:{time.time() - start} s')
        return final_reulst

    else:
        format_file_code = codes[0]
        template_file = get_template_file_path(format_file_code)
        if not os.path.exists(template_file):
            return error_result(1001, 'code invalid')
        final_result = assembly(img_hei, img_width, src_file_name, image, format_file_code, txt_result, template_file, use_show_name, verbose_log)
        logger.info(f'total elapse:{time.time() - start} s')
        return final_result


def fixed_file_ocr(image, drop_score, format_file_code):
    det_model = os.path.join(PERSONA_MODEL_PATH, f'det_{format_file_code}')
    rec_model = os.path.join(PERSONA_MODEL_PATH, f'rec_{format_file_code}')
    if not os.path.exists(det_model):
        det_model = ''
    if not os.path.exists(rec_model):
        rec_model = ''

    # det_model = ''
    # rec_model = ''

    txt_result = invoke_ocr(image, drop_score, det_model=det_model, rec_model=rec_model)
    return txt_result
    # return invoke_ocr(image, drop_score)


def judge_input_img_direction_cls(format_file_code, image):
    """
    判断图像旋转方向分类
    :param format_file_code: 编码
    :param image: 图像数据
    :return: 是否进行了翻转
    """
    # 方向分类判断
    if direction_file_arr.__contains__(format_file_code):
        cls_result = direction_predictor.predict(image)
        category = str(cls_result[0]['category'])
        logger.info(f"方向分类返回，角度：{category}")
        if category == '0':
            return False, ''
        rotate_angle = 360 - int(category)
        if rotate_angle == 90:
            return True, rotate_90(image)
        elif rotate_angle == 180:
            return True, rotate_180(image)
        else:
            return True, rotate_270(image)
    return False, ''


def assembly(img_hei, img_width, src_file_name, image, format_file_code, txt_result, template_file, use_show_name, verbose_log):
    """
    组装文本识别成功，形成电子证照固定格式结果
    :param img_hei:
    :param img_width:
    :param src_file_name:
    :param image:
    :param format_file_code:
    :param txt_result:
    :param template_file:
    :param use_show_name:
    :param verbose_log:
    :return:
    """
    angle = caculate_rotate_angle(format_file_code, txt_result, True)
    if abs(angle) >= MAX_ANGLE:
        fix_box_rotate_position(img_width, img_hei, txt_result, angle)
        image = rotate(image, angle)
        # 也不需要落盘
        # if verbose_log:
        #     output = get_rotate_img_path(src_file_name, f'{DEBUG_FOLDER}')
        #     cv2.imwrite(output, image)
    else:
        logger.info(f"图片倾斜小角度:{angle}无需校正")
    return recognize_ocr_result(image, src_file_name, txt_result, template_file, format_file_code, use_show_name, verbose_log)


def caculate_rotate_angle(format_file_code, txt_result, is_fixed_format_file=True):
    from yrocr.post_process import calculate_rotate_angle
    return calculate_rotate_angle(format_file_code, txt_result, is_fixed_format_file)


def recognize_ocr_result(image, scr_file_name, txt_result, template_file, format_file_code, use_show_name=True, verbose_log=False):
    """
    使用模版文件匹配OCR识别结果
    :param image: 图片数据(经过方向旋转、角度旋转后的最新图片数据)
    :param scr_file_name: 原始文件名
    :param txt_result: TXT识别结果
    :param template_file: 模版文件
    :param format_file_code: 文件编码
    :param use_show_name: 是否使用显示名
    :param verbose_log: 是否显示冗余日志
    :return:
    """
    template = read_json(template_file)
    anchors = template['anchors']
    recognition_areas = template['recognition_areas']
    field_dict = get_field_show_name_dict(recognition_areas)
    anchor_indexs, find_anchors = match_anchors(anchors, txt_result)
    if len(find_anchors) == 0:
        logger.warning("未找到锚点")
        show_fixed_file_ocr_result(image, scr_file_name, txt_result, [])
        reg_result = post_process_result(image, get_default_empty_result(recognition_areas), txt_result, format_file_code, use_show_name)
        return trans(reg_result, field_dict, use_show_name)
    scale_rate1 = get_scale_rate_old(find_anchors, verbose_log)
    scale_rate = get_scale_rate(find_anchors, verbose_log)
    logger.info(f"旧版rate:{scale_rate1}。新版rate:{scale_rate}")
    # 根据实际的锚点位置，计算当前缩放比例下，各个待抽取框实际的位置
    # TODO 缩放比例是最关键的数据，后续看下怎么优化
    anchor = find_anchors[0]
    for area in recognition_areas:
        # 与营业执照left/top在当前比例下的差距
        left_dis = (area['left'] - anchor['left']) * scale_rate
        top_dis = (area['top'] - anchor['top']) * scale_rate
        # 计算真实的left、top、长度、宽度
        area['left'] = int(anchor['real_left'] + int(left_dis))
        area['top'] = int(anchor['real_top'] + int(top_dis))
        area['width'] = int(int(area['width'] * scale_rate))
        area['height'] = int(area['height'] * scale_rate)

    if verbose_log:
        # 显示识别结果
        show_fixed_file_ocr_result(image, scr_file_name, txt_result, recognition_areas)

    ocr_result = recognition_template_labeld_filed(txt_result, anchor_indexs, recognition_areas, verbose_log)
    ocr_result = post_process_result(image, ocr_result, txt_result, format_file_code, use_show_name)
    return trans(ocr_result, field_dict, use_show_name)


def show_fixed_file_ocr_result(src_image, scr_file_name, txt_result, recognition_areas):
    """
    展示识别的最终结果（包含文本结果以及识别区域）
    :param src_image:
    :param scr_file_name:
    :param txt_result:
    :param recognition_areas:
    :return:
    """
    image = src_image.copy()
    import numpy as np
    output = f'{DEBUG_FOLDER}/{scr_file_name}'
    for item in txt_result:
        position = item['position']
        xmin = min(position[0][0], position[1][0], position[2][0], position[3][0])
        ymax = max(position[0][1], position[1][1], position[2][1], position[3][1])
        box = [
            [position[0][0], position[0][1]],
            [position[1][0], position[1][1]],
            [position[2][0], position[2][1]],
            [position[3][0], position[3][1]]
        ]
        box = np.reshape(np.array(box), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True, (255, 0, 255), 1)
        text = item['text'] + '(' + item['score'] + ')'
        image = draw_text(image, text, xmin, ymax)
    # TODO 暂时屏蔽下
    # 绘制识别区域
    # for area in recognition_areas:
    #     xmin = area['left']
    #     ymin = area['top']
    #     xmax = xmin + area['width']
    #     ymax = ymin + area['height']
    #     box = [
    #         [xmin, ymin],
    #         [xmax, ymin],
    #         [xmax, ymax],
    #         [xmin, ymax],
    #     ]
    #     box = np.reshape(np.array(box), [-1, 1, 2]).astype(np.int64)
    #     image = cv2.polylines(np.array(image), [box], True, (0, 0, 255), 3)
    #     text = area['field_name']
    #     image = draw_text(image, text, xmin, ymax)

    cv2.imwrite(output, image)


def combine(ocr_result, reg_result, reg_priority_fields):
    combine_result = {}
    for field in ocr_result:
        combine_result[field] = reg_result[field] if (field in reg_priority_fields or len(
            ocr_result[field]) == 0) and field in reg_result else \
            ocr_result[field]

    return combine_result


def recognition_template_labeld_filed(result, anchor_indexs, recognition_areas, verbose_log=False):
    """
    识别模版标注的待抽取字段（多行自动合并）
    需要自动补全所有字段
    :param result: ocr结果
    :param recognition_areas: 标注的识别区域
    :return:
    """
    # 最终结果
    src_ocr_result = {}
    # 保留每个区域的位置信息，便于最后的判断
    for index, item in enumerate(result):
        rect = get_ocr_point_rect(item['position'])
        if index in anchor_indexs:
            continue
        if verbose_log:
            logger.info("==========判断文本：[" + item['text'] + "]区域：" + json.dumps(rect) + "是否为目标字段")
        field, area = judge_field(item['text'], rect, recognition_areas, verbose_log)
        if field:
            field_val = item['text']
            # 如果模版中有处理函数，则处理之
            if 'replace_re' in area and 'replace_val' in area:
                # logger.info("正则处理识别结果,主要用于处理特殊字符")
                field_val = re.sub(area['replace_re'], area['replace_val'], field_val)
            if not field in src_ocr_result or len(src_ocr_result[field]) == 0:
                src_ocr_result[field] = [
                    {
                        'text': field_val,
                        'rect': rect
                    }
                ]
            else:
                sub_list = src_ocr_result[field]
                sub_list.append({
                    'text': field_val,
                    'rect': rect
                })
                src_ocr_result[field] = sub_list
    if verbose_log:
        logger.info("模版识别原始结果：" + json.dumps(src_ocr_result, ensure_ascii=False))
    final_ocr_result = {

    }
    for key in src_ocr_result:
        sub_list = src_ocr_result[key]
        # get_final_field_val 这个方法很重要
        if len(sub_list) == 1:
            final_ocr_result[key] = get_final_field_val(key, sub_list[0]['text'])
        else:
            # 多个值的情况，要抽取为数组
            if key.endswith(MULTILINE_TAG):
                full_text = ''
                h_range = []
                # 得到该行的上下范围
                for item in sub_list:
                    rect = item['rect']
                    if len(full_text) == 0:
                        full_text = item['text']
                        h_range = [rect['top'], rect['height']]
                    else:
                        if judge_fonts_on_same_line(h_range[0], h_range[1], rect['top'], rect['height']):
                            full_text += item['text']
                        else:
                            full_text += "\r" + item['text']
                            h_range = [rect['top'], rect['height']]
                final_ocr_result[key] = full_text
            elif key.endswith(LEFT_RIGHT_TAG):
                # 仅需左右排序（不需要按照高度从上到下排序）
                # 但是在签发日期字段上，具体日期是打印在固定的"年、月、日"上的，容易导致月日出现在年之前。
                # 因此，针对单行值的情况，直接按照左右的顺序排，忽略高度即可
                import functools
                def compare(item1, item2):
                    left1 = item1['rect']['left']
                    left2 = item2['rect']['left']
                    if left1 < left2:
                        return -1
                    elif left1 < left2:
                        return 1
                    else:
                        return 0

                sub_list = sorted(sub_list, key=functools.cmp_to_key(compare))
                full_text = ''
                for item in sub_list:
                    full_text += item['text']
                full_text = get_final_field_val(key, full_text)
                final_ocr_result[key] = full_text

            else:
                full_text = ''
                for item in sub_list:
                    full_text += item['text']
                full_text = get_final_field_val(key, full_text)
                final_ocr_result[key] = full_text

    # 补齐Key
    for area in recognition_areas:
        if area['field_name'] not in final_ocr_result:
            final_ocr_result[area['field_name']] = ''
    if verbose_log:
        logger.info("模版识别结果：" + json.dumps(final_ocr_result, ensure_ascii=False, indent=4))
    return final_ocr_result


def judge_fonts_on_same_line(top1, height1, top2, height2):
    """
    判断两行文字的高度是否在同一高度行内(二者共同的高度，占用最小的应在50%以上)
    :param top1: 点1开始高度
    :param height1: 点1长度
    :param top2: 点2top
    :param height2: 点2长度
    :return:
    """
    max1 = top1 + height1
    max2 = top2 + height2

    if top1 > max2 or max1 < top2:
        return False
    height = min(max1, max2) - max(top1, top2)
    rate1 = height / height1
    rate2 = height / height2
    rate = max(rate1, rate2)
    return rate > 0.5


def get_default_empty_result(recognition_areas):
    """
    默认的空白识别结果
    :param recognition_areas:
    :return:
    """
    result = {}
    for area in recognition_areas:
        result[area['field_name']] = ''
    return result


def get_final_field_val(field, field_val):
    """
    获取最终的字段值(只处理startswith、endswith)
    :param field: 字段，如：住所、营业期限
    :param field_val: 字段值：如：住所福州XX，营业期限xx
    :return:
    """
    # 开头N个字，包含字段名的，则直接去掉
    if len(field_val) == 0:
        return field_val

    if str.startswith(field_val, field):
        return str.replace(field_val, field, '')
    if str.endswith(field_val, field):
        return str.replace(field_val, field, '')
    # 可以考虑下面的这个不处理（经常容易出问题）
    # 如果是两个字段拼凑的，此处会有点问题。性别民族 =》 性别男民族汉
    # pre = field_val
    # if len(field_val) > len(field):
    #     pre = field_val[:len(field)]
    #     for i in range(len(field)):
    #         pre = str.replace(pre, field[i], '')
    #     return pre + field_val[len(field):]
    # else:
    #     for i in range(len(field_val)):
    #         field_val = str.replace(field_val, field[i], '')
    #     return field_val
    return field_val


def judge_field(text, rect, areas, verbose_log=False):
    """
    对比识别区域，返回匹配率最高的待抽取区域
    匹配做法： 判断哪个待识别区域包含该区域的百分比最高（标注时，已经标注了字段的最大可能区域）
    :param text: 文本
    :param rect: 文本所在的矩形
    :param areas: 识别区域
    :return:
    """
    # 特殊情况1：若判断的文本为：法定代表人：xxx，而法定代表人又是需要抽取的字段，则直接命中
    for area in areas:
        if str.startswith(text, area['field_name']):
            if verbose_log:
                logger.info("特例1：文本：【{}】前缀匹配字段名：{}".format(text, area['field_name']))
            return area['field_name'], area

    score = 0
    field = None
    match_area = None
    for area in areas:
        cur = calculate_cover_rate(text, rect, area, verbose_log)
        if cur > score:
            score = cur
            field = area['field_name']
            match_area = area
    if score > 0.3:
        if verbose_log:
            logger.info(f"文本【{text}】命中字段：【{field}】最高得分:{score}")
        return field, match_area
    return None, None


def calculate_cover_rate(text, rect, area, verbose_log=False):
    """
    判断area包括rect区域的百分比（重叠区域）
    :param rect: {
        "left": xmin,
        "top": ymin,
        "width": width,
        "height": hei
    }
    :param area:{
        "left": xmin,
        "top": ymin,
        "width": width,
        "height": hei
    }
    :param verbose_log 冗余日志
    :return:
    """
    p1_x = rect['left']
    p1_y = rect['top']
    p2_x = p1_x + rect['width']
    p2_y = p1_y + rect['height']
    ocr_area = rect['width'] * rect['height']
    p3_x = area['left']
    p3_y = area['top']
    p4_x = p3_x + area['width']
    p4_y = p3_y + area['height']

    if p1_x > p4_x or p2_x < p3_x or p1_y > p4_y or p2_y < p3_y:
        return 0.00
    width = min(p2_x, p4_x) - max(p1_x, p3_x)
    height = min(p2_y, p4_y) - max(p1_y, p3_y)
    cover_area = width * height
    score = cover_area / ocr_area
    if verbose_log:
        logger.info(f"文本[{text}]属于字段[{area['field_name']}]的概率为:{score}")
    return score


def get_scale_rate_old(find_anchors, verbose_log=False):
    """
    判断图像缩放比例
    之前逻辑：
        锚点匹配：锚点的文本完全匹配
        比例计算：1个锚点时，取长宽比例；多个锚点时，取任意两点的距离作为参照


    现在逻辑：
        锚点匹配：锚点的文本完全匹配
        比例计算：1个锚点时，取Y轴中心点与实际Y轴中心点比较；多个锚点时，取每个Y轴中心点互相做比较
    :param find_anchors:
    :param verbose_log:
    :return:
    """

    # 旧的方式，重新采用全匹配的进行计算
    find_anchors = list(filter(lambda item: item['match_full'], find_anchors))
    if len(find_anchors) == 0:
        logger.info("无锚点，默认返回1")
        return 1
    if len(find_anchors) == 1:
        logger.info("找到一个锚点:" + json.dumps(find_anchors[0], ensure_ascii=False))
        scale_rate1 = find_anchors[0]['real_width'] / find_anchors[0]['width']
        scale_rate2 = find_anchors[0]['real_height'] / find_anchors[0]['height']
        scale_rate = (scale_rate1 + scale_rate2) / 2
    else:
        logger.info("找到{}个锚点".format(len(find_anchors)))
        scale_rate = 0.0
        first = find_anchors[0]
        if verbose_log:
            logger.info("锚点1：" + json.dumps(first, ensure_ascii=False))
        for index in range(1, len(find_anchors)):
            cur = find_anchors[index]
            if verbose_log:
                logger.info("锚点" + str(index + 1) + "：" + json.dumps(cur, ensure_ascii=False))
            labeld_dis = point_distance(first['left'], first['top'], cur['left'], cur['top'])
            real_dis = point_distance(first['real_left'], first['real_top'], cur['real_left'], cur['real_top'])
            cur_rate = real_dis / labeld_dis
            scale_rate += cur_rate
            if verbose_log:
                logger.info('第{}个锚点,缩放比例：{}'.format(index + 1, cur_rate))
            # str(index + 1)
        scale_rate = scale_rate / (len(find_anchors) - 1)
    logger.info("最终缩放比例:{}".format(scale_rate))
    return scale_rate


def get_scale_rate(find_anchors, verbose_log=False):
    """
    新版本的缩放比例计算
    :param find_anchors:
    :param verbose_log:
    :return:
    """
    if len(find_anchors) == 1:
        logger.info("找到一个锚点:" + json.dumps(find_anchors[0], ensure_ascii=False))
        # 只有一个，如果是全匹配的，采用高度+宽度，如果半匹配的，采用高度
        if find_anchors[0]['match_full']:
            scale_rate1 = find_anchors[0]['real_width'] / find_anchors[0]['width']
            scale_rate2 = find_anchors[0]['real_height'] / find_anchors[0]['height']
            scale_rate = (scale_rate1 + scale_rate2) / 2
        else:
            scale_rate = find_anchors[0]['real_height'] / find_anchors[0]['height']
    else:
        # 全匹配的，取中心点坐标，半匹配的，取起点中心点的坐标
        logger.info("找到{}个锚点".format(len(find_anchors)))
        scale_rate = 0.0
        first = find_anchors[0]
        first_x = first['left'] + first['width'] / 2
        first_y = first['top'] + first['height'] / 2
        first_real_x = first['real_left'] + first['real_width'] / 2
        first_real_y = first['real_top'] + first['real_height'] / 2
        if not first['match_full']:
            first_x = first['left']
            first_real_x = first['real_left']

        if verbose_log:
            logger.info("锚点1：" + json.dumps(first, ensure_ascii=False))
        for index in range(1, len(find_anchors)):
            cur = find_anchors[index]
            cur_x = cur['left'] + cur['width'] / 2
            cur_y = cur['top'] + cur['height'] / 2
            cur_real_x = cur['real_left'] + cur['real_width'] / 2
            cur_real_y = cur['real_top'] + cur['real_height'] / 2
            if not cur['match_full']:
                cur_x = cur['left']
                cur_real_x = cur['real_left']

            if verbose_log:
                logger.info("锚点" + str(index + 1) + "：" + json.dumps(cur, ensure_ascii=False))
            labeld_dis = point_distance(first_x, first_y, cur_x, cur_y)
            real_dis = point_distance(first_real_x, first_real_y, cur_real_x, cur_real_y)
            cur_rate = real_dis / labeld_dis
            scale_rate += cur_rate
            if verbose_log:
                logger.info('第{}个锚点,缩放比例：{}'.format(index + 1, cur_rate))
            # str(index + 1)
        scale_rate = scale_rate / (len(find_anchors) - 1)
    logger.info("最终缩放比例:{}".format(scale_rate))
    return scale_rate


def post_process_result(image, ocr_result, txt_result, format_file_code, use_show_name):
    from yrocr.post_process import post_process
    return post_process(image, ocr_result, txt_result, format_file_code, use_show_name)


def trans(result, field_dict, use_show_name):
    if not use_show_name:
        return result
    ret_data = {}
    for key in result:
        if key in field_dict:
            ret_data[field_dict[key]] = result[key]
        else:
            # 保留原始字段
            ret_data[key] = result[key]
    return ret_data


def get_field_show_name_dict(recognition_areas):
    """
    获取字段名==》显示名dict
    :param recognition_areas:
    :return:
    """
    field_dict = {}
    for area in recognition_areas:
        field_dict[area['field_name']] = area['show_name'] if 'show_name' in area else area['field_name']
    return field_dict


def match_anchors(anchors, result):
    """
    匹配锚点，返回所有匹配的锚点
    锚点先去除特殊字符，避免匹配失败
    :param anchors:
    :param result:
    :return:
    """
    find_anchors = []
    text_dict = {}
    # 命中锚点在ocr结果中的索引
    anchor_indexs = []
    for index, item in enumerate(result):
        text = remove_special_char(item['text'])
        text_dict[text] = (index, item['position'])
    for anchor in anchors:
        text = remove_special_char(anchor['text'])
        # 此处寻找锚点的发生逻辑
        # 之前匹配逻辑：template中配置的锚点的文本（去除特殊字符后）与 OCR文本识别结果block完全一致
        # 目前匹配逻辑：template中配置的锚点的文本（去除特殊字符后）与 OCR文本识别结果block的开始一致即可。
        if text in text_dict:
            anchor_indexs.append(text_dict[text][0])
            position = text_dict[text][1]
            rect = get_ocr_point_rect(position)
            anchor['match'] = True
            # 完成匹配
            anchor['match_full'] = True
            anchor['real_left'] = rect['left']
            anchor['real_top'] = rect['top']
            anchor['real_width'] = rect['width']
            anchor['real_height'] = rect['height']
            find_anchors.append(anchor)
        else:
            if 'prefix_match' in anchor and anchor['prefix_match'] == 'yes':
                for reg_text in text_dict:
                    if reg_text.startswith(text):
                        item = text_dict[reg_text]
                        # 半匹配的锚点，有可能既是锚点，又包含要识别的内容，因此，不加入到索引中
                        # anchor_indexs.append(item[0])
                        position = item[1]
                        rect = get_ocr_point_rect(position)
                        anchor['match'] = True
                        # 完成匹配
                        anchor['match_full'] = False
                        anchor['real_left'] = rect['left']
                        anchor['real_top'] = rect['top']
                        anchor['real_width'] = rect['width']
                        anchor['real_height'] = rect['height']
                        find_anchors.append(anchor)
                        break

    return anchor_indexs, find_anchors


def point_distance(x1, y1, x2, y2):
    """
    计算两个点之间的距离
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    x = x1 - x2
    y = y1 - y2
    return math.sqrt((x ** 2) + (y ** 2))


def error_result(code, msg):
    return {'code': code, 'msg': msg}


def success_result(code, msg):
    return {'code': code, 'msg': msg}


if __name__ == '__main__':
    # code = 'idcard'
    # img_path = f'resources/sample/idcard.jpg'
    # img_path = '/Users/chenjianghai/个人资料/身份证测试数据/吴-倾斜身份证.jpg'
    img_path = '/Users/chenjianghai/job/YR/OCR/公司内部测试数据/3.电子证照/1.身份证/160.jpg'
    result = ocr_fixed_format_file(img_path, 'idcard', verbose_log=True)
    print(result)
