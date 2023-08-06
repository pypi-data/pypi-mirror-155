#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 增值税电子普通发票识别测试用例

import json
import os
import shutil

from yrocr.ocr_fixed_format_file import ocr_fixed_format_file

# CODE = 'vat_ele_normal_invoice'
CODE = 'vat_invoice'

TEST_FILE_FOLDER = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/增值税普通发票'


def rename():
    """
    重命名原始文件，便于测试
    :return:
    """
    src = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/4类票据数据/增值税普通发票410_原始'
    index = 1
    for file in os.listdir(src):
        from pathlib import Path
        suffix = Path(file).suffix
        shutil.copy(os.path.join(src, file), os.path.join(TEST_FILE_FOLDER, f'{index}{suffix}'))
        index += 1


def test_single_vat_special_invoice(img_path):
    result = ocr_fixed_format_file(img_path, CODE, verbose_log=True, use_show_name=True)
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
            result['file_name'] = file
            data.append(result)
            if len(data) % 10 == 0:
                df = pd.DataFrame(data)
                df.to_excel(f'增值税电子普通发票_{len(data)}.xlsx', index=False)

    df = pd.DataFrame(data)
    df.to_excel('增值税电子普通发票.xlsx', index=False)
    print("finish")


def show_ocr_text_result():
    """
    直接ocr纯文本识别，查看效果
    :return:
    """
    img_path = '../resources/sample/vat_ele_normal_invoice.jpg'
    from yrocr import ocr_text
    from yrocr.ocr_base import show_ocr_result
    result = ocr_text(img_path)
    show_ocr_result(img_path, result, f'debug/vat_ele_normal_invoice.jpg')


if __name__ == '__main__':
    # rename()
    # show_ocr_text_result()
    # 校验模版
    test_single_vat_special_invoice('/Users/chenjianghai/job/YR/2021/OCR自研/数据/增值税普通发票/391.jpg')
    # test_single_vat_special_invoice('/Users/chenjianghai/job/YR/2021/OCR自研/数据/增值税专用发票/18.jpg')
    # test_single_vat_special_invoice(f'{TEST_FILE_FOLDER}/406.jpg')
    # test_rotate()
    # TODO 检测之前的证书可以
    # batch_test()
    import cv2
    # TODO 依次校验每张图片的效果
