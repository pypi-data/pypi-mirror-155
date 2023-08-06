#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 审计三期CV部分-数据转换（pdf=>images）
import shutil
from yrocr.util.util import pdf_2_images
import os


def trans_ele_facilities_install_license():
    """
    转换 承装电力设施许可证
    :return:
    """
    import os
    src = '/Users/chenjianghai/job/YR/2021/审计三期/数据/承装电力设施许可证_原始'
    target = '/Users/chenjianghai/job/YR/2021/审计三期/数据/承装电力设施许可证'
    suffix_arr = ['jpg', 'jpeg', 'JPEG']
    if not os.path.exists(target):
        os.mkdir(target)
    for file in os.listdir(src):
        is_image = False
        for suffix in suffix_arr:
            if file.endswith(suffix):
                is_image = True
        if is_image:
            shutil.copy(os.path.join(src, file), os.path.join(target, file))
        elif file.endswith('pdf') or file.endswith('PDF'):
            pdf_2_images(os.path.join(src, file), target)
        else:
            print(f'==不处理的文件:{file}')


def trans_construction_project_reg_cert():
    """
    转换 山东省份，建设项目登记备案证明
    Construction project registration record certificate
    :return:
    """
    import os
    src = '/Users/chenjianghai/job/YR/2021/审计三期/数据/登记备案证明_山东_原始'
    target = '/Users/chenjianghai/job/YR/2021/审计三期/数据/登记备案证明_山东'
    suffix_arr = ['jpg', 'jpeg', 'JPEG']
    if not os.path.exists(target):
        os.mkdir(target)
    index = 1
    for file in os.listdir(src):
        is_image = False
        my_suffix = ''
        for suffix in suffix_arr:
            if file.endswith(suffix):
                my_suffix = suffix
                is_image = True
        if is_image:
            shutil.copy(os.path.join(src, file), os.path.join(target, f'{index}.{my_suffix}'))
            index += 1
        elif file.endswith('pdf') or file.endswith('PDF'):
            pdf_2_images(os.path.join(src, file), target)
        else:
            print(f'==不处理的文件:{file}')


def trans_construction_permit():
    """
    转换 浙江 建筑工程施工许可证
    Construction project registration record certificate
    :return:
    """
    import os
    src = '/Users/chenjianghai/job/YR/2021/审计三期/数据/原始_建筑工程施工许可证_浙江'
    target = '/Users/chenjianghai/job/YR/2021/审计三期/数据/建筑工程施工许可证_浙江'
    suffix_arr = ['jpg', 'jpeg', 'JPEG']
    if not os.path.exists(target):
        os.mkdir(target)
    index = 1
    for file in os.listdir(src):
        is_image = False
        my_suffix = ''
        for suffix in suffix_arr:
            if file.endswith(suffix):
                my_suffix = suffix
                is_image = True
        if is_image:
            shutil.copy(os.path.join(src, file), os.path.join(target, f'{index}.{my_suffix}'))
            index += 1
        elif file.endswith('pdf') or file.endswith('PDF'):
            pdf_2_images(os.path.join(src, file), target)
        else:
            print(f'==不处理的文件:{file}')


if __name__ == '__main__':
    # 建筑项目备案登记证明
    trans_construction_project_reg_cert()
