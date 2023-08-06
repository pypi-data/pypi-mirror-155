#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 营业执照_三证合一副本测试。目前仅支持A版本/G版本
import json
import os
import shutil

from yrocr.ocr_fixed_format_file import ocr_fixed_format_file

CODE = 'biz_license_three_in_one'
NAME = "营业执照_三证合一副本"
TEST_FILE_FOLDER = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/营业执照_三证合一副本'
from pathlib import Path


def test_pdf_2_images():
    """
    从1开始编号
    :return:
    """
    target = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/4类票据数据/营业执照三证合一PNG_第二次'
    src_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/4类票据数据/营业执照三证合一PDF_第二次'
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
    src_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/4类票据数据/营业执照_三证合一副本'
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
    TEST_FILE_FOLDER = '/Users/chenjianghai/job/YR/2021/OCR自研/模型问题数据/营业执照/数据'
    for file in os.listdir(TEST_FILE_FOLDER):
        if file.endswith("jpg") or file.endswith("JPG") or file.endswith("png") or file.endswith("jpeg"):
            img_file = os.path.join(TEST_FILE_FOLDER, file)
            print(f"###################################################正在识别{img_file}")
            result = ocr_fixed_format_file(os.path.join(TEST_FILE_FOLDER, file), CODE, verbose_log=False)
            print(json.dumps(result, indent=4, ensure_ascii=False))
            print(f"###################################################识别结果{img_file} finish.")
            result['file_name'] = file
            data.append(result)
            if len(data) % 10 == 0:
                df = pd.DataFrame(data)
                df.to_excel(f'{NAME}_{len(data)}.xlsx', index=False)

    df = pd.DataFrame(data)
    df.to_excel(f'{NAME}.xlsx', index=False)
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
    show_ocr_result(img_path, result, f'debug/{CODE}.jpg')


if __name__ == '__main__':
    # test_pdf_2_images()
    # rename()
    # single_test('../resources/sample/biz_license/biz_license_a.jpg')
    # single_test('../resources/sample/biz_license_three_in_one/biz_license_g.jpg')
    # single_test(f'/Users/chenjianghai/job/YR/2021/OCR自研/模型问题数据/营业执照/数据/76.jpg')
    # batch_test()
    # show_ocr_text_result()
    single_test('/Users/chenjianghai/job/YR/2021/OCR/data/biz_license_labled_all/13.jpg')

    # print(os.path.basename('/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证标注结果汇总/idcard'))
