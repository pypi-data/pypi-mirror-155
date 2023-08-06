#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: OCR纯文本抽取

import cv2
from paddleocr.ppocr.utils.logging import get_logger

from yrocr.ocr_base import invoke_ocr

logger = get_logger(name='ocr_text')


def ocr_text(img_path, drop_score=0.5):
    """
    纯文本抽取，返回原始数据
    :param img_path: 图片路径
    :param drop_score: 可选参数
    :return: 返回结果如下
        [{
            'block_id': '1',
            'score': '0.99923944',
            'text': '其他费用表',
            'position': [
                [508.0, 103.0],
                [656.0, 103.0],
                [656.0, 137.0],
                [508.0, 137.0]
            ]
        }, {
            'block_id': '2',
            'score': '0.7450202',
            'text': '表四',
            'position': [
                [59.0, 140.0],
                [86.0, 140.0],
                [86.0, 157.0],
                [59.0, 157.0]
            ]
        }]
    """
    return invoke_ocr(cv2.imread(img_path), drop_score)


if __name__ == '__main__':
    img_path = '/Users/chenjianghai/job/YR/2021/OCR/公司内部测试数据/1.文本识别/3.四川大学项目审计报告_0.jpg'
    result = ocr_text(img_path)
    from yrocr.ocr_base import show_ocr_result
    show_ocr_result(img_path, result, f'debug/text.jpg')
