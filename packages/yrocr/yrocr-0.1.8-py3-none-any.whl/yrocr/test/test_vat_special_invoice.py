#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 增值税专用发票识别测试用例

import json
import os
import shutil

from yrocr.ocr_fixed_format_file import ocr_fixed_format_file

CODE = 'vat_invoice'
# CODE = 'vat_special_invoice'
"""
发票代码、发票号码、开票日期、 
购买方信息（名称、纳税人识别号、地址、电话、开户行及账号）
销售方信息（名称、纳税人识别号、地址、电话、开户行及账号）
开票人、收款人、复核、
货物或服务名称、规格型号、单位、数量、单价、金额明细、税率、税额明细
税额合计
"""

# 普通发票
TEST_FILE_FOLDER = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/增值税专用发票'


def rename():
    """
    重命名原始文件，便于测试
    :return:
    """
    src = '/Users/chenjianghai/job/YR/2021/OCR/data/发票1000_原始'
    TEST_FILE_FOLDER = '/Users/chenjianghai/job/YR/2021/OCR/data/发票1000'
    index = 1
    for file in os.listdir(src):
        if file.endswith("jpg") or file.endswith("JPG") or file.endswith("png") or file.endswith("jpeg"):
            from pathlib import Path
            suffix = Path(file).suffix
            shutil.copy(os.path.join(src, file), os.path.join(TEST_FILE_FOLDER, f'{index}{suffix}'))
            index += 1


def test_single_vat_special_invoice(img_path):
    result = ocr_fixed_format_file(img_path, CODE, verbose_log=True, use_show_name=False)
    print(json.dumps(result, indent=4, ensure_ascii=False))


def test_rotate():
    imgs = [
        '/Users/chenjianghai/job/YR/2021/OCR自研/数据/专用发票角度测试/0.jpg',
        '/Users/chenjianghai/job/YR/2021/OCR自研/数据/专用发票角度测试/90.jpg',
        '/Users/chenjianghai/job/YR/2021/OCR自研/数据/专用发票角度测试/180.jpg',
        '/Users/chenjianghai/job/YR/2021/OCR自研/数据/专用发票角度测试/270.jpg',
    ]
    for img in imgs:
        print(f"###########识别{img}")
        result = ocr_fixed_format_file(img, CODE, verbose_log=True)
        print(json.dumps(result, indent=4, ensure_ascii=False))


def batch_test():
    import pandas as pd
    data = []
    for file in os.listdir(TEST_FILE_FOLDER):
        if file.endswith("jpg") or file.endswith("JPG") or file.endswith("png") or file.endswith("jpeg"):
            img_file = os.path.join(TEST_FILE_FOLDER, file)
            print(f"###################################################正在识别{img_file}")
            result = ocr_fixed_format_file(os.path.join(TEST_FILE_FOLDER, file), CODE, verbose_log=False, use_show_name=False)
            print(json.dumps(result, indent=4, ensure_ascii=False))
            print(f"###################################################识别结果{img_file} finish.")
            result['name'] = file
            data.append(result)

    df = pd.DataFrame(data)
    df.to_excel('增值税专用发票.xlsx', index=False)
    print("finish")


def show_ocr_text_result():
    """
    直接ocr纯文本识别，查看效果
    :return:
    """
    img_path = '../resources/sample/vat_special_invoice.jpg'
    from yrocr import ocr_text
    from yrocr.ocr_base import show_ocr_result
    result = ocr_text(img_path)
    show_ocr_result(img_path, result, f'debug/vat_special_invoice.jpg')


def roteta_img(img_path, output):
    """
    旋转原始图片
    :param img_path:
    :return:
    """
    import cv2
    from yrocr.resources.post_process.util import juege_angle
    judge_txts = ['增值税专用发票']
    from yrocr import ocr_text
    from yrocr.util.cvutil import rotate
    txt_result = ocr_text(img_path, drop_score=0.01)
    angle = juege_angle(judge_txts, txt_result)
    print(f"##############旋转角度：{angle}")
    image = cv2.imread(img_path)
    image = rotate(image, angle)
    cv2.imwrite(output, image)


def batch_roteta():
    """
    批量纠正倾斜的角度
    :return:
    """
    input = '/Users/chenjianghai/job/YR/2021/OCR/data/发票1000_倾斜'
    output = '/Users/chenjianghai/job/YR/2021/OCR/data/发票1000_纠正倾斜'
    for file in os.listdir(input):
        if file.endswith("jpg") or file.endswith("JPG") or file.endswith("png") or file.endswith("jpeg"):
            roteta_img(os.path.join(input, file), os.path.join(output, file))


if __name__ == '__main__':
    # rename()
    # batch_roteta()
    # show_ocr_text_result()
    # 校验模版
    test_single_vat_special_invoice('../resources/sample/vat_special_invoice.jpg')
    # test_single_vat_special_invoice('/Users/chenjianghai/job/YR/2021/OCR/data/增值税专用发票/199.jpg')
    # test_single_vat_special_invoice(f'{TEST_FILE_FOLDER}/406.jpg')
    # test_rotate()
