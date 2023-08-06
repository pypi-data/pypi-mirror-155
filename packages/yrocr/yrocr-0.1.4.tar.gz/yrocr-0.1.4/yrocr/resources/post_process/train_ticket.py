#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 后处理脚本&正则处理脚本
from paddleocr.ppocr.utils.logging import get_logger

from yrocr.resources.post_process.util import juege_angle, split_left_right, treat_by_reg

logger = get_logger(name='idcart_front')


def get_rotate_angle(txt_result):
    """
    个性化的判断图像旋转角度判断方法
    :param txt_result:
    :return:
    """
    logger.info("执行【火车票】角度判断方法")
    judge_txts = ['中国铁路祝您旅途愉快', '仅供报销使用']
    return juege_angle(judge_txts, txt_result)


def post_process(image, result, txt_result, use_show_name):
    """
    后处理脚本
    所有字段：[、、、、、、、、、、、、、、]
    合合官方测试：https://ai.intsig.com/api/vision/train_ticket
    :param img_path:
    :param result:
    :param txt_result:
    :return:
    """

    txts = [item['text'] for item in txt_result]
    full_text = "。".join(txts)
    logger.info(f"全文:{full_text}")

    result['车次号'] = treat_train_num(result['车次号'], full_text)
    result['座位类别'] = treat_seat_level(result['座位类别'], full_text)
    result['座位号'] = treat_seat_number(result['座位号'], full_text)
    # 特殊处理3： 目的地可能跟 检票口混淆了。如：检票：9检票口上海虹桥站
    result['检票口'] = treat_check(result['检票口'], full_text)
    left_text, right_text = get_left_right_text(txt_result, result)
    logger.info(f"左侧全文:{left_text}")
    logger.info(f"右侧全文:{right_text}")

    from_site, to_site = treat_site_name(result, txt_result, left_text, right_text)
    result['出发地'] = from_site
    result['目的地'] = to_site

    # 特殊处理4：提取价格
    result['价格'] = treat_price(result['价格'], full_text)

    # 特殊处理5：拆分身份证跟姓名
    passenger_id, passenger_name = get_idcard_no_and_name(result['乘客身份证姓名'], full_text)
    if use_show_name:
        result['passenger_id'] = passenger_id
        result['passenger_name'] = passenger_name
    else:
        result['乘客身份证'] = passenger_id
        result['乘客名称'] = passenger_name

    del result['乘客身份证姓名']
    result['乘车时间'] = treat_departure_date(result['乘车时间'], full_text)
    result['火车票ID'] = treat_ticket_id(result['火车票ID'], full_text)
    return result


def treat_ticket_id(text, full_text):
    reg = '[0-9]{14}[A-Z][0-9]{6}'
    text = treat_by_reg(text, reg)
    if len(text) == 0:
        return treat_by_reg(full_text, reg)
    return text


def treat_seat_number(text, full_text):
    reg = '[0-9]{1,2}车[0-9]{1,2}[ABCDEFG]号'
    text = treat_by_reg(text, reg)
    if len(text) == 0:
        return treat_by_reg(full_text, reg)
    return text


def get_left_right_text(txt_result, result):
    """
    切割左右全文，先通过车次号、没有车次号的，通过"网"这个字
    再没有的通过具体的
    :param txt_result:
    :param result:
    :return:
    """
    left_text, right_text = split_left_right(txt_result, result['车次号'], split_text='。')
    if len(left_text) > 0 and len(right_text) > 0:
        return left_text, right_text
    left_text, right_text = split_left_right(txt_result, '密码区')
    if len(left_text) > 0 and len(right_text) > 0:
        return left_text, right_text
    return '', ''


def treat_train_num(text, full_text):
    """
    处理车次号
    特征： CDGZTK
    :param text:
    :param full_text:
    :return:
    """
    reg = '([CDGZTK][0-9]{2,4})。'
    text = treat_by_reg(text, reg, 1)
    if len(text) == 0:
        return treat_by_reg(full_text, reg, 1)
    return text


def treat_seat_level(text, full_text):
    """
    处理座位等级
    :param text:
    :param full_text:
    :return:
    """
    if len(text) == 0:
        text = full_text
    if text.__contains__("二"):
        return '二等座'
    elif text.__contains__("一"):
        return '一等座'
    elif text.__contains__("商"):
        return '商务座'
    return ''


def treat_departure_date(text, full_text):
    """
    处理乘车时间
    2019年08月19日09：52开
    :param date:
    :return:
    """
    reg = '2[0-9]{3}年[0-9]{2}月[0-9]{2}日[0-9]{2}\:[0-9]{2}'
    text = text.replace('：', ':')
    text = treat_by_reg(text, reg)
    if len(text) == 0:
        full_text = full_text.replace('：', ':')
        return treat_by_reg(full_text, reg)
    return text


def treat_price(text, full_text):
    reg = '￥([0-9]{1,5}\.[0-9])元'
    text = treat_by_reg(text, reg)
    if len(text) == 0:
        return treat_by_reg(full_text, reg)
    return text


def treat_check(text, full_text):
    """
    处理检票口
    检票口类型：
    检票：14
    检票：14A
    检票：3检票口
    候车：候车室5号检票口
    检票：候车室3号检票口

    :param text:
    :param full_text:
    :return:
    """
    regs = [
        ('(检票|候车)[：\:]([A-Z]{0,1}[0-9]{1,2}[A-Z]{0,1})', 2),
        ('(检票|候车)[：\:]候车室([A-Z]{0,1}[0-9]{1,2}[A-Z]{0,1})', 2)
    ]
    for reg, group_index in regs:
        text = treat_by_reg(text, reg, group_index)
        if len(text) > 0:
            return text

    for reg, group_index in regs:
        text = treat_by_reg(full_text, reg, group_index)
        if len(text) > 0:
            return text
    return ''


def treat_site_name(result, txt_result, left_text, right_text):
    """
    处理出发/终点站点名称(去除英文、数字)
    出发地/目的地中容易混淆站点代码，以及火车票红色代码。去除所有的数字跟字母
    :param name:
    :return:
    """
    import re
    remove_chars = '[0-9a-zA-Z’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~：]+'
    from_site = result['出发地']
    to_site = result['目的地']
    if len(from_site) > 0 and from_site.__contains__('站'):
        from_site = re.sub(remove_chars, '', from_site)
    else:
        # 先从左边文字里判断，如果左边文字没有，再从txt_result获取包含站，且在图像左边的
        if len(left_text) > 0:
            reg = '([\u4E00-\u9FA5]{2,6}站)。'
            from_site = treat_by_reg(left_text, reg, 1)
        else:
            from_site = ''
    if len(to_site) > 0 and to_site.__contains__('站'):
        to_site = re.sub(remove_chars, '', to_site)
    else:
        if len(right_text) > 0:
            reg = '([\u4E00-\u9FA5]{2,6}站)。'
            to_site = treat_by_reg(right_text, reg, 1)
        else:
            to_site = ''
    return from_site, to_site


def get_idcard_no_and_name(text, full_text):
    """
    得到身份证、姓名。350823991****1639张小华
    :param text:
    :return:
    """
    reg = '[0-9]{10}\*{4}[0-9]{3}[0-9X][\u4E00-\u9FA5]{2,4}'
    idcard_no_name = treat_by_reg(text, reg)
    if len(idcard_no_name) == 0:
        idcard_no_name = treat_by_reg(full_text, reg)
    if len(idcard_no_name) >= 0:
        idcard_no = text[0:18]
        name = text[18:]
        return idcard_no, name
    return '', ''


if __name__ == '__main__':
    result = {
        "出发地": "",
        "目的地": "",
        "车次号": "",
        "乘车时间": "",
        "座位号": "",
        "座位类别": "",
        "价格": "",
        "乘客身份证姓名": "",
        '检票口': '',
        '火车票ID': ''
    }
    full_text = '检票：4检票口。Y075585。北京南站。福州站。G28。Fuzhou。BeiJingnan。2019年08月19日09：52开。11车08A号。网。二等座。￥719.0元。王发。限乘当日当次车。3505241989****6037王志发。买票请到12306。发货请到95306。中国铁路祝您旅途愉快。34682310010820Y075585。5福州售'
    txt_result = [{'text': full_text}]
    final_result = post_process('', result, txt_result, False)
    import json

    print(json.dumps(final_result, indent=4, ensure_ascii=False))
