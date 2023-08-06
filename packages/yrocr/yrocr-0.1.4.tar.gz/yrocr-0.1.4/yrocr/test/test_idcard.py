#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 身份证测试用例
import json
import os
import shutil

import pandas as pd

from yrocr.ocr_fixed_format_file import ocr_fixed_format_file

CODE = 'idcard'
TEST_FILE_FOLDER = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证'
TEST_FILE_FOLDER2 = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证_彩色'
from pathlib import Path


def test_pdf_2_images():
    """
    从1开始编号
    :return:
    """
    target = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证_原始'
    src_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证PDF'
    for file in os.listdir(src_folder):
        if file.endswith("pdf") or file.endswith("PDF"):
            from yrocr.util.util import pdf_2_images
            pdf_2_images(os.path.join(src_folder, file), target, True)
        elif file.endswith("JPEG"):
            shutil.copy(os.path.join(src_folder, file), os.path.join(target, file))
            print("复制成功")


def rename():
    """
    从1开始编号
    :return:
    """
    src_folder = '/Users/chenjianghai/job/YR/2021/营销档案/图像原始分类数据/idcard'
    index = 1
    for file in os.listdir(src_folder):
        if file.endswith("jpg") or file.endswith("JPG") or file.endswith("png") or file.endswith("jpeg"):
            suffix = Path(file).suffix
            shutil.copy(os.path.join(src_folder, file), os.path.join(TEST_FILE_FOLDER, f'{index}{suffix}'))
            index += 1


def single_test(img_path):
    result = ocr_fixed_format_file(img_path, CODE, verbose_log=True, use_show_name=False)
    print(json.dumps(result, indent=4, ensure_ascii=False))


def batch_test():
    import pandas as pd
    data = []
    for file in os.listdir(TEST_FILE_FOLDER):
        if file.endswith("jpg"):
            img_file = os.path.join(TEST_FILE_FOLDER, file)
            print(f"###################################################正在识别{img_file}")
            result = ocr_fixed_format_file(os.path.join(TEST_FILE_FOLDER, file), CODE, verbose_log=True)
            print(json.dumps(result, indent=4, ensure_ascii=False))
            print(f"###################################################识别结果{img_file} finish.")
            result['file_name'] = file
            data.append(result)
            if len(data) % 50 == 0:
                df = pd.DataFrame(data)
                df.to_excel(f'身份证_1026_{len(data)}.xlsx', index=False)

    df = pd.DataFrame(data)
    df.to_excel('身份证_1026.xlsx', index=False)
    print("finish")


def show_ocr_text_result():
    """
    直接ocr纯文本识别，查看效果
    :return:
    """
    img_path = '/Users/chenjianghai/个人资料/身份证测试数据/吴_正反面.jpg'
    from yrocr import ocr_text
    from yrocr.ocr_base import show_ocr_result
    result = ocr_text(img_path, drop_score=0.01)
    show_ocr_result(img_path, result, f'debug/idcard11.jpg')


def test_predict_by_personal_rec_model(img_path):
    from paddleocr.tools.infer import predict_det


if __name__ == '__main__':
    # TODO 遗留： 同一张图片上，翻转90度了怎么办（个性化度判断长度高度）
    # rename()
    # single_test(f'{TEST_FILE_FOLDER}/203.jpg')
    single_test('/Users/chenjianghai/job/YR/2021/OCR自研/模型问题数据/身份证/数据/韩永生 身份证.jpg')
    # batch_test()
    # show_ocr_text_result()

    # print(os.path.basename('/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证标注结果汇总/idcard'))
