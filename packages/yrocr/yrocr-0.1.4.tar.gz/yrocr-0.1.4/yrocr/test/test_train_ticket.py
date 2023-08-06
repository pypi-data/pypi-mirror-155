#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 火车票OCR识别测试用例
import json
import os
from yrocr.ocr_fixed_format_file import ocr_fixed_format_file
import shutil

CODE = 'train_ticket'
TEST_FILE_FOLDER = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/火车票'


def rename():
    """
    从1开始编号
    :return:
    """
    src_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/4类票据数据/火车票499_原始'
    index = 1
    for file in os.listdir(src_folder):
        from pathlib import Path
        suffix = Path(file).suffix
        shutil.copy(os.path.join(src_folder, file), os.path.join(TEST_FILE_FOLDER, f'{index}{suffix}'))
        index += 1


def test_single_train_ticket(img_path):
    result = ocr_fixed_format_file(img_path, CODE, verbose_log=True, use_show_name=False)
    print(json.dumps(result, indent=4, ensure_ascii=False))


def test_rotate_90():
    img_path = '/Users/chenjianghai/个人资料/身份证测试数据/陈江海_测试旋转90.jpeg'
    from yrocr import ocr_text
    from yrocr.ocr_base import show_ocr_result
    result = ocr_text(img_path)
    show_ocr_result(img_path, result, f'debug/idcard_debug.jpg')
    # 结论：90度情况下，识别条件不一定好


def batch_test():
    import pandas as pd
    data = []
    TEST_FILE_FOLDER = '/Users/chenjianghai/job/YR/2021/OCR自研/模型问题数据/火车票/全部'
    for file in os.listdir(TEST_FILE_FOLDER):
        img_file = os.path.join(TEST_FILE_FOLDER, file)
        print(f"###################################################正在识别{img_file}")
        result = ocr_fixed_format_file(os.path.join(TEST_FILE_FOLDER, file), CODE, verbose_log=False)
        print(json.dumps(result, indent=4, ensure_ascii=False))
        print(f"###################################################识别结果{img_file} finish.")
        result['file_name'] = file
        data.append(result)
        # if len(data) % 50 == 0:
        #     df = pd.DataFrame(data)
        #     df.to_excel(f'火车票_{len(data)}.xlsx', index=False)

    df = pd.DataFrame(data)
    df.to_excel('火车票.xlsx', index=False)
    print("finish")


if __name__ == '__main__':
    rename()
    # 校验模版
    # test_single_train_ticket('../resources/sample/train_ticket.png')
    # 校验已有的每一张图片
    test_single_train_ticket('/Users/chenjianghai/job/YR/2021/OCR自研/模型问题数据/火车票/全部/车票 (5).jpg')
    # batch_test()
    # test_rotate_90()
