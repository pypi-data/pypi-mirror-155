#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 后处理脚本&正则处理脚本
import re


def post_process(image, result, txt_result, use_show_name):
    """
    后处理脚本
    bad case:
    {
        "住所": "",
        "单位名称": "：上海冲佳电力工程安装有限住所：上海市崇明县中兴镇广福路100号公司",
        "发证日期": "2013年2月09日",
        "有效期限": "自2012年03月27日始至2018年03月20止",
        "法定代表人": "：俞冲",
        "许可类别和等级": "：承装类四级承修类四级承试类四级",
        "许可证编号": "：4-1-00033-2006"
    }
    :param image:
    :param result:
    :param txt_result:
    :return:
    """

    # 特殊后处理1：如果"单位名称"字段包含"住所"或包含"所："两个字，则证明是公司名称太长导致"单位名称"与"住所"两个字段混合一起
    # TODO 特殊后处理2： 单位名称单独过长，或者住所单独过长
    org_name = result['单位名称']
    if org_name.__contains__("住所") or org_name.__contains__("所："):
        split_index = org_name.index("住所") if org_name.__contains__("住所") else org_name.index("所：")
        result['单位名称'] = org_name[:split_index]
        result['住所'] = org_name[split_index + 2:]
        """
        最极端的情况下，【单位名称】与【住所】均过长，即：两个字段都占用两行。
        处理措施：取【单位名称】与【法定代表人】之间的块，区分左右。左边为【单位名称】后缀，右边为 【住所】后缀
        """
        src_org_name = ''
        start_index = -1
        for index, item in enumerate(txt_result):
            if item['text'].startswith('单位名称'):
                src_org_name = item['text']
                start_index = index + 1
                break
        blocks = []
        for index in range(start_index, len(txt_result)):
            block = txt_result[index]
            if block['text'].startswith('法定代表人'):
                break
            blocks.append(block)
        if len(blocks) == 0:
            return result

        # 如果【单位名称】与【法定代表人】有一个多行的，则需要从原始识别结果中识别
        index = src_org_name.index("住所") if src_org_name.__contains__("住所") else src_org_name.index("所：")
        org_name = src_org_name[:index]
        address = src_org_name[index + 2:]

        # 如果有值，证明【单位名称】或 【住所】过长，需作为后缀添加
        left_suffix = ''
        right_suffix = ''
        hei, width = image.shape[0:2]
        for block in blocks:
            x = block['position'][0][0] * 2
            if x < width:
                left_suffix = left_suffix + block['text']
            else:
                right_suffix = right_suffix + block['text']

        org_name = re.sub(r'[：]', '', org_name + left_suffix)
        org_name = re.sub(r'单位名称', '', org_name)
        address = re.sub(r'[：]', '', address + right_suffix)
        result['单位名称'] = org_name
        result['住所'] = address

    return result


def exatrct_by_reg(txt_result):
    # 这里也需要直接调用后处理脚本
    return {'reg': 'not reg script'}
