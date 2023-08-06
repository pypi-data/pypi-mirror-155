#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 后处理模块

import os

from paddleocr.ppocr.utils.logging import get_logger

from yrocr.util.ocr_util import get_post_process_file_path, split_format_file_code

logger = get_logger(name='ocr_format_file')
import importlib


def post_process(image, result, txt_result, format_file_code, use_show_name):
    """
    后处理
    备注：简单的后处理直接在模版中做，如：去除冒号
    复杂的后处理可以单独写逻辑处理。如：单位名称与住所重叠了。
    :param image: 图片
    :param result: 抽取结果
    :param txt_result: 纯文本识别结果
    :param format_file_code: 编码
    :param use_show_name 是否使用显示名称
    :return:
    """
    script_file_path = get_post_process_file_path(format_file_code)
    if not os.path.exists(script_file_path):
        logger.warning(f"{format_file_code} post process file not exists")
        return result
    module_name = get_module_name(format_file_code)
    action = importlib.import_module(module_name)
    return action.post_process(image, result, txt_result, use_show_name)


def calculate_rotate_angle(format_file_code, txt_result, is_fixed_format_file):
    """
    计算局部图片的倾斜角度
    :param format_file_code:
    :param img_path:
    :param txt_result:
    :param is_fixed_format_file:
    :return:
    """
    script_file_path = get_post_process_file_path(format_file_code)
    if not os.path.exists(script_file_path):
        logger.warning(f"{format_file_code} post process file not exists,use default rotate method")
        from yrocr.util.ocr_util import get_rotate_angle
        return get_rotate_angle(txt_result, is_fixed_format_file)
    module_name = get_module_name(format_file_code)
    action = importlib.import_module(module_name)
    if (hasattr(action, 'get_rotate_angle')):
        return action.get_rotate_angle(txt_result)
    else:
        logger.warning(f"{format_file_code} rotata  file not exists,use default rotate method")
        from yrocr.util.ocr_util import get_rotate_angle
        return get_rotate_angle(txt_result, is_fixed_format_file)


def get_module_name(format_file_code):
    """
    获取后处理脚本
    :param format_file_code:
    :return:
    """
    namespace, code = split_format_file_code(format_file_code)
    return f'yrocr.resources.post_process.{namespace}.{code}' if len(namespace) > 0 else f'yrocr.resources.post_process.{code}'


if __name__ == '__main__':
    # module_name = get_module_name('train_ticket')
    module_name = get_module_name('idcard_front')
    action = importlib.import_module(module_name)
    if (hasattr(action, 'get_rotate_angle')):
        print('属性')
    else:
        print('没熟悉')
