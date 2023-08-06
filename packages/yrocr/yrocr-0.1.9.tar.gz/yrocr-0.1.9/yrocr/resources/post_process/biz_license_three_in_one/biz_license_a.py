#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 三证合一营业执照【A】版后处理
"""
新版营业执照维持原版执照的8种格式不变，
以保证法定记载事项清晰明确，保持营业执照的稳定性和一贯性。
即：
A格式：适用公司法人。
说明：最常见的就是这种的，本后处理脚本也是这种类型
字段：（8个字段）
左侧：名称、类型、法定代表人、经营范围、
右侧：注册资本、成立日期、营业期限、住所


B格式：适用非公司法人
C格式：适用合伙企业
D格式：适用农民专业合作社法人
E格式：适用个人独资企业
F格式：适用个体工商户

G格式：适用内资非法人企业、内资非公司企业分支机构、内资分公司、外商投资企业分支机构、合伙企业分支机构、个人独资企业分支机构、外国（地区）企业在中国境内从事生产经营活动。
说明：分公司用的是这种的
字段：（7个字段）
名称、类型、负责人、经营范围、成立日期、营业期限、营业场所
"""

import re

from paddleocr.ppocr.utils.logging import get_logger

from yrocr.resources.post_process.biz_license_three_in_one.base_biz_license import treat_unified_social_credit_code, treat_money
from yrocr.resources.post_process.util import juege_angle, treat_by_reg, find_pre_full_text_by_key, find_suffix_full_text_by_key, split_left_right, \
    get_text_between_start_end_key

logger = get_logger(name='biz_license')

# 类型
type_arr = [
    '一人有限责任公司',
    '有限责任公司',
    '有限责任公司(自然人独资)',
    '有限责任公司(法人独资)',
    '有限责任公司(自然人投资或控股)',
    '有限责任公司(自然人投资或控股的法人独资)',
    '有限责任公司(非自然人投资或控股的法人独资)',
    '有限责任公司分公司',
    '有限责任公司分公司(非自然人投资或控股的法人独资)',
    '其他有限责任公司',
    '全民所有制分支机构(非法人)',
    '股份有限公司(非上市、自然人投资或控股)',
    '股份有限公司(上市)',
    '股份有限公司'
]

# 营业期限
period_arr = [
    '长期'
]


def get_rotate_angle(txt_result):
    """
    个性化的判断图像旋转角度判断方法
    :param img_path:
    :param txt_result:
    :return:
    """
    logger.info("执行【营业执照_三证合一_副本】角度判断方法")
    judge_txts = ['营业执照', '经营范围', '统一社会信用代码', '国家市场监督管理总局']
    return juege_angle(judge_txts, txt_result)


def post_process(image, result, txt_result, use_show_name):
    """
    后处理
    :param img_path:
    :param result:
    :param txt_result:
    :param use_show_name:
    :return:
    """
    txts = [item['text'] for item in txt_result]
    full_text = "".join(txts)
    logger.info(f"全文:{full_text}")
    left_text, right_text = split_left_right(txt_result, '营业执照')
    logger.info(f"左侧全文:{left_text}")
    logger.info(f"右侧全文:{right_text}")

    # result['全文'] = full_text
    # result['左侧全文'] = left_text
    # result['右侧全文'] = right_text
    # 左侧字段：统一社会信用代码、名称、类型、法定代表人、经营范围
    result['统一社会信用代码'] = treat_unified_social_credit_code(result['统一社会信用代码'], full_text)
    result['名称'] = treat_company_name(result['名称'], left_text)
    result['类型'] = treat_type(result['类型'], full_text)
    result['法定代表人'] = treat_lawer(result['法定代表人'], left_text)
    result['经营范围'] = treat_business_scope(result['经营范围'], left_text)

    # 右侧字段：注册资本、成立日期、营业期限、住所、发证日期
    result['注册资本'] = treat_money(result['注册资本'], full_text)
    result['成立日期'] = treat_found_date(result['成立日期'], right_text)
    result['营业期限'] = treat_period(result['营业期限'], full_text, right_text)
    result['住所'] = treat_addr(result['住所'], full_text)
    issue_date = treat_issue_date(result['发证日期_LEFT_RIGHT'], right_text, txt_result)
    if use_show_name:
        result['issue_date'] = issue_date
    else:
        result['发证日期'] = issue_date
    del result['发证日期_LEFT_RIGHT']
    return result


def treat_company_name(text, left_text):
    """
    处理公司名称
    :param text:
    :param left_text:
    :return:
    """
    # 5个字以内认为识别错误
    min_size = 5
    reg = '[\u4e00-\u9fa5]{6,30}'
    company_name = treat_by_reg(text, reg)

    # 抽取的值有误
    if len(text) < min_size or len(company_name) == 0:
        # 情况1
        reg = '称([\u4e00-\u9fa5]{6,30})名'
        company_name = treat_by_reg(left_text, reg, 1)
        if len(company_name) > 0:
            return company_name

        # 情况2： 名称xxxxx类型
        if left_text.__contains__('名称') and left_text.__contains__('类型'):
            company_name = get_text_between_start_end_key(left_text, '名称', '类型')
            return company_name
        # TODO 是否有其他情况，待观察数据
        return ''
    else:
        # 抽取值正确，但可能存在其他信息，需再处理下
        company_name = text.replace('名称', '')
        if text.startswith('称'):
            company_name = text[1:]
        if text.endswith('名'):
            company_name = text[:len(text) - 1]
        return company_name


def treat_type(text, full_text):
    """
    处理类型
    :param text:
    :param full_text:
    :return:
    """
    match_type = ''
    for type in type_arr:
        if type.__contains__(text):
            match_type = type
            break
    if len(match_type) > 0:
        return match_type
    # 按照文字倒叙排
    import functools
    def compare(obj1, obj2):
        if len(obj2) < len(obj1):
            return -1
        elif len(obj1) < len(obj2):
            return 1
        else:
            return 0

    standard_type_arr = sorted(type_arr, key=functools.cmp_to_key(compare))
    remove_reg = '[\'!\"#$%&()*+,-./:;<=>?@，。?★、…【】《》？“”^！[\\]_\{\|\}（）：~\s]+'
    full_text = re.sub(remove_reg, '', full_text)
    for type in standard_type_arr:
        prue_type = re.sub(remove_reg, '', type)
        if full_text.__contains__(prue_type):
            return type
    return ''


def treat_lawer(text, left_text):
    max_size = 4
    field_name = '法定代表人'
    next_field = '经营范围'
    if len(text) == 0:
        if left_text.__contains__(field_name) and left_text.__contains__(next_field):
            return get_text_between_start_end_key(left_text, field_name, next_field)
    else:
        if text.__contains__(field_name):
            index = text.index(field_name)
            return text[index + len(field_name):]
        if len(text) > max_size and left_text.__contains__(field_name) and left_text.__contains__(next_field):
            return get_text_between_start_end_key(left_text, field_name, next_field)
        return text


def treat_business_scope(text, left_text):
    """
    处理经营范围
    :param text:
    :param full_text:
    :return:
    """
    field_name = '经营范围'
    if len(text) == 0 and left_text.__contains__(field_name):
        index = text.index(field_name)
        return text[index + len(field_name):]
    else:
        return text


def treat_found_date(text, right_text):
    """
    成立日期
    右侧顺序为：注册资本、成立日期、营业期限、住所、发证日期
    因此，可能存在两个日期，必须从 【营业期限、住所】两个进行切割
    :param text:
    :param right_text: 右侧文本
    :return:
    """
    reg = '[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}[日]{0,1}'
    found_date = treat_by_reg(text, reg)
    if len(found_date) == 0:
        # 得到前半段全文，并使用正则匹配
        part_full_text = find_pre_full_text_by_key(right_text, ['营业期限', '住所', '住', '所'])
        return treat_by_reg(part_full_text, reg)
    return found_date


def treat_addr(text, full_text):
    """
    处理住所
    :param text:
    :param full_text:
    :return:
    """
    if text.__contains__("住所"):
        index = text.index("住所")
        return text[index + 2:]
    return text


def treat_period(text, full_text, right_text):
    """
    处理营业期限
    有如下集中情况：
    永久、长期、空白、具体年月日 至 具体年月日、具体年月日 至 长期、具体年月日 至 永久、具体年月日 至 年月日（空白）、具体年月日 至******、
    :param text:
    :param full_text:
    :return:
    """
    # 合法的正则
    valid_period_reg_arr = [
        '[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日至[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日',
        '[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日至长期',
        '[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日至永久',
        '[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日至年月日',
        '[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日至年月',
        '永久',
        '长期'
    ]
    for reg in valid_period_reg_arr:
        peroid = treat_by_reg(text, reg)
        if len(peroid) > 0:
            return peroid

    for reg in valid_period_reg_arr:
        peroid = treat_by_reg(full_text, reg)
        if len(peroid) > 0:
            return peroid

    # 还没有的话 营业期限2015年12月12日至年月 住所
    if right_text.__contains__('营业期限') and right_text.__contains__('住'):
        peroid = get_text_between_start_end_key(right_text, '营业期限', '住')
        return peroid

    return ''


def treat_issue_date(text, full_text, txt_result):
    """
    发证日期
    :param text:
    :param full_text:
    :return:
    """
    remove_reg = '[\'!\"#$%&()*+,-./:;<=>?@，。?★、…【】《》？“”^！[\\]_\{\|\}（）：~\s]+'
    # text = re.sub(remove_reg, '', text)
    full_text = re.sub(remove_reg, '', full_text)
    reg = '[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}[日]{0,1}'
    issue_date = treat_by_reg(text, reg)
    if len(issue_date) == 0:
        # 得到前半段全文，并使用正则匹配
        suffix_full_text = find_suffix_full_text_by_key(full_text, ['住所', '住', '所'])
        return treat_by_reg(suffix_full_text, reg)
    return issue_date


if __name__ == '__main__':
    reg = '[壹贰叁肆伍陆柒捌玖拾佰仟万亿圆整零角分]{2,30}|[0-9\.]{3,30}[万元整]{2,3}'
    text = 'sss1111120514.5534万元整aa'
    result = treat_by_reg(text, reg)
    print(result)
