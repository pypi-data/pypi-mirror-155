#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 合并多人的标注结果
import json
import os
import shutil

import pandas as pd


def merge(type='air_transport'):
    """
    合并多个人的标注结果数据（PaddleOcr）
    :return:
    """
    # 最终文件（用于检查所有人的标注结果）
    if type == 'idcard':
        final_foler = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证标注结果汇总/idcard'
        labled_folders = [
            '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证标注结果汇总/林子键',
            '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证标注结果汇总/林婕',
            '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证标注结果汇总/陈江毅',
            '/Users/chenjianghai/job/YR/2021/OCR自研/数据/身份证标注结果汇总/陈全毅'
        ]
    elif type == 'air_transport':
        base_foler = '/Users/chenjianghai/job/YR/2021/OCR自研/数据/飞机行程单标结果汇总'
        final_foler = base_foler + '/air_transport'
        labled_folders = [
            base_foler + '/林子健',
            base_foler + '/林婕',
            base_foler + '/陈江毅',
            base_foler + '/陈全毅'
        ]
    elif type == 'biz_license_three_in_one':
        base_foler = '/Users/chenjianghai/job/YR/2021/OCR/data/biz_license_labeld'
        final_foler = base_foler + '/biz_license_three_in_one'
        labled_folders = [
            base_foler + '/wdh',
            base_foler + '/cjy',
            base_foler + '/cqy',
            base_foler + '/lj',
            base_foler + '/lzj'
        ]
    # 第二批
    elif type == 'biz_license_three_in_one2':
        base_foler = '/Users/chenjianghai/job/YR/2021/OCR/data/biz_license_labeld2'
        final_foler = base_foler + '/biz_license_three_in_one_batch2'
        labled_folders = [
            base_foler + '/qy',
            base_foler + '/qy2',
            base_foler + '/jy',
            base_foler + '/jy2'
        ]
    # 合并全部 营业执照
    elif type == 'biz_license_three_in_one_all':
        final_foler = '/Users/chenjianghai/job/YR/2021/OCR/data/biz_license_labled_all'
        labled_folders = [
            '/Users/chenjianghai/job/YR/2021/OCR/data/biz_license_3',
            '/Users/chenjianghai/job/YR/2021/OCR/data/biz_license_labeld2/biz_license_three_in_one_batch2'
        ]

    # 增值税专用发票
    elif type == 'vat_special_invoice':
        base_foler = '/Users/chenjianghai/job/YR/2021/OCR/data/vat_special_invoice_labeld'
        final_foler = base_foler + '/vat_special_invoice'
        labled_folders = [
            base_foler + '/liuyonghui',
            base_foler + '/xiongzhenshan',
            base_foler + '/yhw',
            base_foler + '/zengzhishuifapiao1',
            base_foler + '/zengzhishuifapiao2',
            base_foler + '/zengzhishuifapaio3',
            base_foler + '/zengzhishuifapiao4',
            base_foler + '/zengshizhuifapiao5'
        ]

    # step1:解析Lable.txt

    labels_datas = []
    for f in labled_folders:
        sub_datas = parse_label_txt_result(os.path.join(f, 'Label.txt'))
        for item in sub_datas:
            # 拼凑上最终文件夹名称
            item['file_name'] = os.path.basename(final_foler) + "/" + item['file_name']
            labels_datas.append(item)
    # df = pd.DataFrame(data=labels_datas)
    # df.to_csv(os.path.join(final_foler, 'Label.txt'), index=False, sep="\t", header=False)
    with open(os.path.join(final_foler, 'Label.txt'), 'w') as f:
        for data in labels_datas:
            f.write(data['file_name'] + '\t' + data['value'] + '\n')
    print("parse label.txt finish")

    # step2 解析 rec_gt.txt
    rec_datas = []
    for f in labled_folders:
        print(f'处理：{f}')
        sub_datas = parse_rec_gt_file(os.path.join(f, 'rec_gt.txt'))
        for item in sub_datas:
            rec_datas.append(item)
    df = pd.DataFrame(data=rec_datas)
    df.to_csv(os.path.join(final_foler, 'rec_gt.txt'), index=False, sep="\t", header=False)
    print("parse rec_gt.txt finish")

    # step3: copy crop_img
    target_corp_img = os.path.join(final_foler, 'crop_img')
    if not os.path.exists(target_corp_img):
        os.mkdir(target_corp_img)
    for folder in labled_folders:
        for file in os.listdir(os.path.join(folder, 'crop_img')):
            shutil.copy(os.path.join(folder, 'crop_img', file), os.path.join(target_corp_img, file))
    print("copy crop_image finish")

    # step4: copy fileState.txt
    file_state_datas = []
    for file in labled_folders:
        sub_datas = parse_file_status_file(os.path.join(file, 'fileState.txt'))
        for item in sub_datas:
            # 拼凑上最终文件夹名称
            item['file_name'] = final_foler + "/" + item['file_name']
            file_state_datas.append(item)
    df = pd.DataFrame(data=file_state_datas)
    df.to_csv(os.path.join(final_foler, 'fileState.txt'), index=False, sep="\t", header=False)
    print("parse fileState.txt finish")


def parse_label_txt_result(file):
    datas = []
    for line in open(file):
        arr = line.split("\t")
        # 此处的file_name由两部分组织，文件夹名称+ 文件名。
        file_name = arr[0]
        index = file_name.index("/")
        file_name = file_name[index + 1:]
        items = json.loads(arr[1])
        value = json.dumps(items, ensure_ascii=False)
        datas.append({
            'file_name': file_name,
            'value': str(value)
        })
    return datas


def parse_rec_gt_file(file):
    datas = []
    line_num = 0
    for line in open(file):
        arr = line.split("\t")
        if len(arr) != 2:
            print(f'第{line_num}行GT文件值异常：{line}')
        line_num += 1
        datas.append({
            'file_name': arr[0],
            'value': arr[1].replace("\n", "")
        })
    return datas


def parse_file_status_file(file):
    datas = []
    for line in open(file):
        arr = line.split("\t")
        if arr[0].__contains__("/"):
            new_arr = arr[0].split("/")
        else:
            new_arr = arr[0].split("\\")
        datas.append({
            'file_name': new_arr[len(new_arr) - 1],
            'value': '1'
        })
    return datas


if __name__ == '__main__':
    merge('biz_license_three_in_one_all')
