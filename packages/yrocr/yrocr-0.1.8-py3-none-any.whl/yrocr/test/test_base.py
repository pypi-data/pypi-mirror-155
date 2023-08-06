#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 基础功能测试用例

from yrocr import ocr_text
from yrocr.ocr_base import show_ocr_result

if __name__ == '__main__':
    # 识别并展示文本识别结果
    img_path = 'data/text.jpg'
    result = ocr_text(img_path)
    show_ocr_result(img_path, result, f'data/show_text_result.jpg')
