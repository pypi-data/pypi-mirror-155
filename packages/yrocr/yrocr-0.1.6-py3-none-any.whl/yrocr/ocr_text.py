#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: OCR纯文本抽取

import cv2
from paddleocr.ppocr.utils.logging import get_logger
import click
from yrocr.cli import ocr_cli
from yrocr.ocr_base import invoke_ocr

logger = get_logger(name='ocr_text')


@ocr_cli.command("text")
@click.option("-p", "--img_path", prompt="the image path", help="the image path", required=True)
@click.option("-s", "--drop_score", prompt="the drop score", help="the drop score,default 0.5", required=False, default=0.5)
def ocr_text(img_path, drop_score=0.5):
    """
    图像纯文本抽取
    """
    result = invoke_ocr(cv2.imread(img_path), drop_score)
    click.echo(result)
    return result


if __name__ == '__main__':
    img_path = '/Users/chenjianghai/job/YR/2021/OCR/公司内部测试数据/1.文本识别/3.四川大学项目审计报告_0.jpg'
    result = ocr_text(img_path)
    from yrocr.ocr_base import show_ocr_result

    show_ocr_result(img_path, result, f'debug/text.jpg')
