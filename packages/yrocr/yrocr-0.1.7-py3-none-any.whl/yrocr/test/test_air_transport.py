#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 验证飞机行程单
import json
import os
import shutil

from yrocr.ocr_fixed_format_file import ocr_fixed_format_file

CODE = 'air_transport'
TEST_FILE_FOLDER = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/飞机行程单'
from pathlib import Path


def rename():
    """
    从1开始编号
    :return:
    """
    src_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/4类票据数据/行程单352_原始'
    index = 1
    for file in os.listdir(src_folder):
        if file.endswith("jpg") or file.endswith("JPG") or file.endswith("png") or file.endswith("jpeg"):
            suffix = Path(file).suffix
            shutil.copy(os.path.join(src_folder, file), os.path.join(TEST_FILE_FOLDER, f'{index}{suffix}'))
            index += 1


def single_test(img_path):
    result = ocr_fixed_format_file(img_path, CODE, verbose_log=True, drop_score=0.01)
    print(json.dumps(result, indent=4, ensure_ascii=False))


def batch_test():
    import pandas as pd
    data = []
    for file in os.listdir(TEST_FILE_FOLDER):
        img_file = os.path.join(TEST_FILE_FOLDER, file)
        print(f"###################################################正在识别{img_file}")
        result = ocr_fixed_format_file(os.path.join(TEST_FILE_FOLDER, file), CODE, verbose_log=True)
        print(json.dumps(result, indent=4, ensure_ascii=False))
        print(f"###################################################识别结果{img_file} finish.")
        result['file_name'] = file
        data.append(result)
        if len(data) % 10 == 0:
            df = pd.DataFrame(data)
            df.to_excel(f'idcard_{len(data)}.xlsx', index=False)

    df = pd.DataFrame(data)
    df.to_excel('身份证.xlsx', index=False)
    print("finish")


def show_ocr_text_result():
    """
    直接ocr纯文本识别，查看效果
    :return:
    """
    img_path = f'{TEST_FILE_FOLDER}/4.jpg'
    from yrocr import ocr_text
    from yrocr.ocr_base import show_ocr_result
    result = ocr_text(img_path, drop_score=0.01)
    print(result)
    show_ocr_result(img_path, result, f'debug/air_transport_old.jpg')


def roteta_img(img_path, output):
    """
    旋转原始图片
    :param img_path:
    :return:
    """
    import cv2
    from yrocr.resources.post_process.util import juege_angle
    judge_txts = ['航空运输电子客票行程单']
    from yrocr import ocr_text
    from yrocr.util.cvutil import rotate
    txt_result = ocr_text(img_path, drop_score=0.01)
    angle = juege_angle(judge_txts, txt_result)
    print(f"##############旋转角度：{angle}")
    image = cv2.imread(img_path)
    image = rotate(image, angle)
    cv2.imwrite(output, image)


def rotata_all():
    src_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/飞机行程单'
    dest_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/飞机行程单_正式'
    for file in os.listdir(src_folder):
        if file.endswith("jpg") or file.endswith("JPG") or file.endswith("png") or file.endswith("jpeg"):
            roteta_img(os.path.join(src_folder, file), os.path.join(dest_folder, file))


if __name__ == '__main__':
    # rename()
    single_test(f'{TEST_FILE_FOLDER}/4.jpg')
    # batch_test()
    # show_ocr_text_result()
    # rotata_all()
    # roteta_img('/Users/chenjianghai/job/YR/2021/OCR自研/数据/飞机行程单/1.jpg')
