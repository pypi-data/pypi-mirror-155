#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 审计三期CV部分功能测试
import os
from yrocr.ocr_fixed_format_file import ocr_fixed_format_file
import json


def test_safety_production_license():
    """
    测试安全生产许可证
    :return:
    """
    folder = '/Users/chenjianghai/job/YR/2021/审计三期/数据/安全生产许可证'
    code = 'audit/safety_production_license'
    for img_file in os.listdir(folder):
        if img_file.endswith('DS_Store'):
            continue
        print(f"====正在识别:{img_file}")
        result = ocr_fixed_format_file(os.path.join(folder, img_file), code, verbose_log=True)
        print(f"###################结果区域 {img_file}###################")
        print(json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False))
        print("###################最终结果 end ###################")


def test_safety_production_license_single(img_file):
    """
    测试安全生产许可证
    :return:
    """
    # folder = '/Users/chenjianghai/job/YR/2021/审计三期/数据/安全生产许可证_全国_FINISH'
    folder = '/Users/chenjianghai/Downloads/模型问题(1)/20-安全生产许可证'
    code = 'audit/safety_production_license'
    img_path = os.path.join(folder, img_file)
    result = ocr_fixed_format_file(img_path, code, verbose_log=False, use_show_name=False)
    print(f"###################结果区域 {img_path}###################")
    print(json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False))
    print("###################最终结果 end ###################")


def test_ele_facilities_install_license():
    """
    测试承装电力设施许可证
    :return:
    """
    folder = '/Users/chenjianghai/job/YR/2021/审计三期/数据/承装电力设施许可证_全国'
    code = 'audit/ele_facilities_install_license'
    for img_file in os.listdir(folder):
        if img_file.endswith('DS_Store'):
            continue
        print(f"====正在识别:{img_file}")
        result = ocr_fixed_format_file(os.path.join(folder, img_file), code, verbose_log=True)
        print(f"###################结果区域 {img_file}###################")
        print(json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False))
        print("###################最终结果 end ###################")


def test_ele_facilities_install_license_single():
    """
    测试承装电力设施许可证
    :return:
    """
    folder = '/Users/chenjianghai/job/YR/2021/审计三期/数据/承装电力设施许可证_全国_FINISH'
    img_file = '7.JPEG'
    code = 'audit/ele_facilities_install_license'
    result = ocr_fixed_format_file(os.path.join(folder, img_file), code, verbose_log=True)
    print(f"###################结果区域 {img_file}###################")
    print(json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False))
    print("###################最终结果 end ###################")


def test_construction_project_reg_cert_shandong():
    """
    测试山东省建设项目登记备案证明
    :return:
    """
    import pandas as pd
    folder = '/Users/chenjianghai/job/YR/2021/审计三期/数据/登记备案证明_山东'
    code = 'audit/construction_project_reg_cert_shandong'
    data = []
    for img_file in os.listdir(folder):
        if img_file.endswith('DS_Store'):
            continue
        print(f"====正在识别:{img_file}")
        result = ocr_fixed_format_file(os.path.join(folder, img_file), code, verbose_log=False, use_show_name=False)
        print(f"###################结果区域 {img_file}###################")
        print(json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False))
        print("###################最终结果 end ###################")
        result['file_name'] = img_file
        data.append(result)
    df = pd.DataFrame(data)
    df.to_excel('登记备案证明_山东_新.xlsx', index=False)
    print("finish")


def test_construction_project_reg_cert_single(img_file):
    """
    测试承装电力设施许可证
    :return:
    """
    folder = '/Users/chenjianghai/job/YR/2021/审计三期/数据/登记备案证明_山东'
    code = 'audit/construction_project_reg_cert_shandong'
    img_path = os.path.join(folder, img_file)
    result = ocr_fixed_format_file(img_path, code, verbose_log=True)
    print(f"###################结果区域 {img_file}###################")
    print(json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False))
    print("###################最终结果 end ###################")


def construction_works_license_zhejiang():
    """
    测试【浙江】【建筑工程施工许可证】
    :return:
    """
    folder = '/Users/chenjianghai/job/YR/2021/审计三期/数据/建筑工程施工许可证_浙江'
    code = 'audit/construction_works_license_zhejiang'
    for img_file in os.listdir(folder):
        if img_file.endswith('DS_Store'):
            continue
        print(f"====正在识别:{img_file}")
        result = ocr_fixed_format_file(os.path.join(folder, img_file), code, verbose_log=True)
        print(f"###################结果区域 {img_file}###################")
        print(json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False))
        print("###################最终结果 end ###################")


def construction_works_license_zhejiang_single(img_file):
    """
    单个测试【浙江】【建筑工程施工许可证】
    :return:
    """
    folder = '/Users/chenjianghai/job/YR/2021/审计三期/数据/建筑工程施工许可证_浙江'
    img_path = os.path.join(folder, img_file)
    code = 'audit/construction_works_license_zhejiang'
    result = ocr_fixed_format_file(img_path, code, verbose_log=False, use_show_name=False)
    print(f"###################结果区域 {img_file}###################")
    print(json.dumps(result, sort_keys=True, indent=4, ensure_ascii=False))
    print("###################最终结果 end ###################")


if __name__ == '__main__':
    # 登记备案证明_山东
    # test_construction_project_reg_cert_shandong()
    # test_construction_project_reg_cert_single('88.JPEG')
    # 安全生产许可证
    # test_safety_production_license_single('290.安全生产许可证.jpg')

    # 建筑工程施工许可证_浙江
    construction_works_license_zhejiang_single('2.JPEG')

    # construction_works_license_zhejiang()
    # test_safety_production_license_single()
    # test_ele_facilities_install_license_single()
    # test_construction_project_reg_cert_single()
    # test_safety_production_license()
    # test_ele_facilities_install_license()

    # test_construction_project_reg_cert()
    # test_construction_project_reg_cert()
