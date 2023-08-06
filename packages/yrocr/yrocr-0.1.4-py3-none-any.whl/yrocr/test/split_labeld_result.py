#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: [DET]切分已标注的数据，分为训练集，验证集

import os
import random
import json
import shutil
import pandas as pd


def get_label_map(file):
    label_map = {}
    for line in open(file):
        arr = line.split("\t")
        # 此处的file_name由两部分组织，文件夹名称+ 文件名。
        file_name = arr[0]
        index = file_name.index("/")
        file_name = file_name[index + 1:]
        # value = arr[1].replace("'", "\"")
        items = json.loads(arr[1])
        value = json.dumps(items, ensure_ascii=False)
        label_map[file_name] = value
    return label_map


def parse_file_status_file(file):
    datas = []
    for line in open(file):
        arr = line.split("\t")
        arr = arr[0].split("/")
        datas.append({
            'file_name': arr[len(arr) - 1],
            'value': '1'
        })
    return datas


def parse_rec_gt_file(file):
    datas = []
    for line in open(file):
        arr = line.split("\t")
        file_name_arr = arr[0].split("/")
        datas.append({
            'file_name': file_name_arr[len(file_name_arr) - 1],
            'value': arr[1]
        })
    return datas


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def split_for_det(type='air_transport'):
    """
    切割【文字检测】训练/测试数据
    :return:
    """
    if type == 'idcard':
        # 标注数据文件夹
        labeld_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证标注结果汇总/idcard'
        # 目标文件夹
        target_folder = '../model/data/det_idcrad'
    elif type == 'air_transport':
        # 标注数据文件夹
        labeld_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/飞机行程单标结果汇总/air_transport'
        # 目标文件夹
        target_folder = '../model/data/det_air_transport'
    elif type == 'biz_license_three_in_one':
        # 标注数据文件夹
        labeld_folder = '/Users/chenjianghai/job/YR/2021/OCR/data/biz_license_labled_all'
        # 目标文件夹
        target_folder = '../model/data/det_biz_license'
    elif type == 'vat_special_invoice':
        # 标注数据文件夹
        labeld_folder = '/Users/chenjianghai/job/YR/2021/OCR/data/vat_special_invoice_labeld/vat_special_invoice'
        # 目标文件夹
        target_folder = '../model/data/det_vat_special_invoice'


    mkdir(target_folder)
    mkdir(os.path.join(target_folder, 'train_image'))
    mkdir(os.path.join(target_folder, 'test_image'))

    # 得到所有已确认的文件，随机打乱拆分
    fileStateDatas = parse_file_status_file(os.path.join(labeld_folder, 'fileState.txt'))
    files = [
        item['file_name'] for item in fileStateDatas
    ]
    # 随机打乱，8/2切割
    random.shuffle(files)
    train_nums = len(files) * 0.7

    # 所有标注的文字记录
    label_map = get_label_map(os.path.join(labeld_folder, 'Label.txt'))

    # 复制文件、复制label.txt记录
    train_data = []
    test_data = []

    for index, file in enumerate(files):
        if index < train_nums:
            target_file = os.path.join(target_folder, 'train_image', file)
            train_data.append({
                'file_name': file,
                'value': label_map[file]
            })
        else:
            target_file = os.path.join(target_folder, 'test_image', file)
            test_data.append({
                'file_name': file,
                'value': label_map[file]
            })
        # 复制图片
        shutil.copy(os.path.join(labeld_folder, file), target_file)

    # train_df = pd.DataFrame(data=train_data)
    # train_df.to_csv(os.path.join(target_folder, 'train.txt'), index=False, sep="\t", header=False)
    with open(os.path.join(target_folder, 'train.txt'), 'w') as f:
        for data in train_data:
            f.write(data['file_name'] + '\t' + data['value'] + '\n')

    # test_df = pd.DataFrame(data=test_data)
    # test_df.to_csv(os.path.join(target_folder, 'test.txt'), index=False, sep="\t", header=False)
    with open(os.path.join(target_folder, 'test.txt'), 'w') as f:
        for data in test_data:
            f.write(data['file_name'] + '\t' + data['value'] + '\n')
    print(f"训练数据{len(train_data)}.验证数据{len(test_data)}")


def split_for_rec(type='air_transport'):
    """
    切割【文字识别】训练/测试数据
    :return:
    """
    if type == 'idcard':
        # 标注数据文件夹
        labeld_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证标注结果汇总/idcard'
        # 目标文件夹
        target_folder = '../model/data/rec_idcrad'
    elif type == 'air_transport':
        # 标注数据文件夹
        labeld_folder = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/飞机行程单标结果汇总/air_transport'
        # 目标文件夹
        target_folder = '../model/data/rec_air_transport'
    elif type == 'biz_license_three_in_one':
        # 标注数据文件夹
        labeld_folder = '/Users/chenjianghai/job/YR/2021/OCR/data/biz_license_labeld/biz_license_three_in_one'
        # 目标文件夹
        target_folder = '../model/data/rec_biz_license'
    elif type == 'vat_special_invoice':
        # 标注数据文件夹
        labeld_folder = '/Users/chenjianghai/job/YR/2021/OCR/data/vat_special_invoice_labeld/vat_special_invoice'
        # 目标文件夹
        target_folder = '../model/data/rec_vat_special_invoice'

    mkdir(target_folder)
    mkdir(os.path.join(target_folder, 'train_image'))
    mkdir(os.path.join(target_folder, 'test_image'))

    # 得到gt文件
    rec_flle_arr = parse_rec_gt_file(os.path.join(labeld_folder, 'rec_gt.txt'))
    files = [
        item['file_name'] for item in rec_flle_arr
    ]
    # 随机打乱，8/2切割
    random.shuffle(files)
    train_nums = len(files) * 0.8

    # 所有标注的文字记录
    label_map, word_dict = get_rec_label_map(os.path.join(labeld_folder, 'rec_gt.txt'))

    # 复制文件、复制label.txt记录
    train_data = []
    test_data = []

    for index, file in enumerate(files):
        if index < train_nums:
            target_file = os.path.join(target_folder, 'train_image', file)

            train_data.append({
                'file_name': 'train_image/' + file,
                'value': label_map[file]
            })
        else:
            target_file = os.path.join(target_folder, 'test_image', file)
            test_data.append({
                'file_name': 'test_image/' + file,
                'value': label_map[file]
            })
        # 复制图片
        shutil.copy(os.path.join(labeld_folder, 'crop_img', file), target_file)

    with open(os.path.join(target_folder, 'word_dict.txt'), 'w') as f:
        for key in word_dict:
            f.write(key + '\n')

    with open(os.path.join(target_folder, 'train_gt.txt'), 'w') as f:
        for data in train_data:
            f.write(data['file_name'] + '\t' + data['value'] + '\n')

    # test_df = pd.DataFrame(data=test_data)
    # test_df.to_csv(os.path.join(target_folder, 'test.txt'), index=False, sep="\t", header=False)
    with open(os.path.join(target_folder, 'test_gt.txt'), 'w') as f:
        for data in test_data:
            f.write(data['file_name'] + '\t' + data['value'] + '\n')
    print(f"训练数据{len(train_data)}.验证数据{len(test_data)}")


def get_rec_label_map(file):
    label_map = {}
    word_dict = {}
    for line in open(file):
        arr = line.split("\t")
        # 此处的file_name由两部分组织，文件夹名称+ 文件名。
        file_name = arr[0]
        index = file_name.index("/")
        file_name = file_name[index + 1:]
        text = arr[1].replace("\n", "")
        for char in text:
            word_dict[char] = char
        label_map[file_name] = text

    return label_map, word_dict


if __name__ == '__main__':
    split_for_det('biz_license_three_in_one')
