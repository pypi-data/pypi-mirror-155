#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 【增值税专用发票/普通发票/电子普通发票】通用后处理
from yrocr.resources.post_process.util import split_left_right_by_arrs, treat_by_reg
from yrocr.util.ocr_util import remove_special_char
from paddleocr.ppocr.utils.logging import get_logger

logger = get_logger(name='vat_base')


def treat_vat_invoice_number(text, txt_result):
    """
    处理发票号码(右上方的8位数字)
    :param text:
    :param full_text:
    :param txt_result:
    :return:
    """
    reg = '[0-9]{8}'
    text = treat_float_num(text, reg)
    if len(text) == 0:
        # 从后边搜索
        left_text, right_text = split_left_right_by_arrs(txt_result, ['密码区', '密码', '密', '码', '区'], split_text="。")
        reg = '。([0-9]{8})。'
        text = treat_float_num(right_text, reg, 1)
    return text


def treat_total_cover_tax_upper(text, lower_price, full_text):
    """
    处理价税合计大写
    备注：大写经常容易识别出错，可考虑从小写转换过来
    :param text:
    :param lower_price:小写金额
    :param full_text:
    :return:
    """
    reg = '[壹贰叁肆伍陆柒捌玖拾佰仟万亿圆整零角分]{2,30}'
    text = treat_by_reg(text, reg)
    if len(text) == 0:
        if len(lower_price) > 0:
            logger.info("采用小写金额")
            return digital_to_chinese(lower_price)
        else:
            text = treat_by_reg(full_text, reg)
    # 如果大小写不一致，采用小写的
    if len(lower_price) > 0:
        new_uppder_price = digital_to_chinese(lower_price)
        if new_uppder_price != text:
            return new_uppder_price

    return text


def digital_to_chinese(digital):
    """
    数字小写转大写
    :param digital:
    :return:
    """
    str_digital = str(digital)
    chinese = {'1': '壹', '2': '贰', '3': '叁', '4': '肆', '5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖', '0': '零'}
    chinese2 = ['拾', '佰', '仟', '万', '分', '角']
    jiao = ''
    bs = str_digital.split('.')
    yuan = bs[0]
    if len(bs) > 1:
        jiao = bs[1]
        if len(jiao) > 2:
            jiao = jiao[:2]
        if jiao == '00' or jiao == '0':
            jiao = ''

    r_yuan = [i for i in reversed(yuan)]
    count = 0
    for i in range(len(yuan)):
        if i == 0:
            r_yuan[i] += '圆'
            continue
        r_yuan[i] += chinese2[count]
        count += 1
        if count == 4:
            count = 0
            chinese2[3] = '亿'

    s_jiao = [i for i in jiao][:2]  # 去掉小于分之后的

    j_count = -1
    for i in range(len(s_jiao)):
        s_jiao[i] += chinese2[j_count]
        j_count -= 1
    last = [i for i in reversed(r_yuan)] + s_jiao

    last_str = ''.join(last)
    last_str = last_str.replace('0百', '0').replace('0十', '0').replace('000', '0').replace('00', '0').replace('0圆', '圆')
    for i in range(len(last_str)):
        digital = last_str[i]
        if digital in chinese:
            last_str = last_str.replace(digital, chinese[digital])
    # 整数的，加上整
    if last_str.endswith("圆"):
        last_str = last_str + "整"
    # 整数的，加上整: 4600.05 应该为：肆仟陆佰零拾圆零伍分
    # '拾', '佰', '仟', '万', '分', '角'
    last_str = last_str.replace('零仟', '零')
    last_str = last_str.replace('零佰', '零')
    last_str = last_str.replace('零拾', '零')
    last_str = last_str.replace('零角', '零')
    last_str = last_str.replace('零零', '零')
    return last_str


def treat_total_cover_tax_lower(text, txt_result):
    """
    处理价税合计小写
    无匹配时可尝试："税率"或'税额'这个块左右0.58的下方位置搜索数字，最大的即为总金额
    :param text:
    :param txt_result:
    :return:
    """
    reg = '[0-9]{1,10}\\.[0-9]{2}'
    text = treat_float_num(text, reg)
    if len(text) == 0:
        find_key_point = False
        left = 0
        right = 0
        top = 0
        for item in txt_result:
            if item['text'] == '税率':
                find_key_point = True
                left = item['position'][0][0]
                right = item['position'][1][0]
                top = item['position'][0][1]
                left = left - (right - left) * 2
                right = right + (right - left) * 5
                break
            if item['text'] == '税额':
                find_key_point = True
                left = item['position'][0][0]
                right = item['position'][1][0]
                top = item['position'][0][1]
                left = left - (right - left) * 2
                right = right + (right - left) * 2
                break

        money_arr = []
        if find_key_point:
            logger.info("尝试从相对位置中匹配['价税合计小写']")
            for item in txt_result:
                cur_center = (item['position'][0][0] + item['position'][1][0]) / 2
                cur_top = item['position'][0][1]
                if left < cur_center < right and cur_top > top:
                    price = treat_float_num(item['text'], reg)
                    if len(price) > 0:
                        money_arr.append(float(price))
        if len(money_arr) > 0:
            price = max(money_arr)
            return str(price)
    return text


def treat_total_money(text, txt_result):
    """
    处理不含税总金额
    无匹配时可尝试："金额"这个块左右0.58的下方位置搜索数字，最大的即为总金额
    :param text:
    :param txt_result:
    :return:
    """
    reg = '[0-9]{1,10}\\.[0-9]{2}'
    text = treat_float_num(text, reg)
    if len(text) == 0:
        find_key_point = False
        left = 0
        right = 0
        top = 0
        for item in txt_result:
            if item['text'] == '金额':
                find_key_point = True
                left = item['position'][0][0]
                right = item['position'][1][0]
                top = item['position'][0][1]
                break

        # 查找中心点，在'税额'周边的。再进行正则匹配，得到最大的数字即为'总税额'
        money_arr = []
        if find_key_point:
            logger.info("尝试从相对位置中匹配['不含税总金额']")
            left = left - (right - left) * 0.5
            right = right + (right - left) * 0.5
            for item in txt_result:
                cur_center = (item['position'][0][0] + item['position'][1][0]) / 2
                cur_top = item['position'][0][1]
                if left < cur_center < right and cur_top > top:
                    price = treat_float_num(item['text'], reg)
                    if len(price) > 0:
                        money_arr.append(float(price))
        if len(money_arr) > 0:
            price = max(money_arr)
            return str(price)
    return text


def treat_total_total_tax(text, txt_result):
    """
    处理总税额
    无匹配时可尝试："税额"这个块左右0.58的下方位置搜索数字，最大的即为税额
    :param text:
    :param full_text:
    :param txt_result:
    :return:
    """
    reg = '[0-9]{1,10}\\.[0-9]{2}'
    text = treat_float_num(text, reg)
    if len(text) == 0:
        find_key_point = False
        left = 0
        right = 0
        top = 0
        for item in txt_result:
            if item['text'] == '税额':
                find_key_point = True
                left = item['position'][0][0]
                right = item['position'][1][0]
                top = item['position'][0][1]
                break

        # 查找中心点，在'税额'周边的。再进行正则匹配，得到最大的数字即为'总税额'
        money_arr = []
        if find_key_point:
            logger.info("尝试从相对位置中匹配['总税额']")
            left = left - (right - left) * 0.5
            right = right + (right - left) * 0.5
            for item in txt_result:
                cur_center = (item['position'][0][0] + item['position'][1][0]) / 2
                cur_top = item['position'][0][1]
                if left < cur_center < right and cur_top > top:
                    price = treat_float_num(item['text'], reg)
                    if len(price) > 0:
                        money_arr.append(float(price))
        if len(money_arr) > 0:
            price = max(money_arr)
            return str(price)
    return text


def treat_cipher(text, full_text, right_text):
    """
    处理密码
    :param text:
    :param full_text:
    :param right_text:
    :return:
    """
    reg = '[0-9\/\*\<\-\>\+\-a-zA-Z]{90,100}'
    text = treat_by_reg(text, reg)
    if len(text) == 0:
        text = treat_by_reg(full_text, reg)
        if len(text) == 0:
            right_text = right_text.replace('密', '')
            right_text = right_text.replace('码', '')
            right_text = right_text.replace('区', '')
            text = treat_by_reg(right_text, reg)
            text = right_text.replace('。', '')
    return text


def treat_issue_date(text, full_text):
    """
    处理开票日期
    :param text:
    :param full_text:
    :return:
    """
    reg = '[0-9]{4}年[0-9]{2}月[0-9]{2}日'
    text = treat_by_reg(text, reg)
    if len(text) == 0:
        text = treat_by_reg(full_text, reg)
    return text


def treat_money(text):
    """
    处理多行金额
    :param text:
    :return:
    """
    text = text.replace(' ', '')
    arr = text.split('\r')
    new_arr = []
    reg = '[0-9]{1,10}\\.[0-9]{2}'
    if len(arr) > 0:
        for money in arr:
            money = treat_float_num(money, reg)
            new_arr.append(money)
    return new_arr


def treat_multi_text(money, text):
    """
    处理多行文本（货物名称、规格型号、单位）
    :param money:
    :param text:
    :return:
    """
    if len(money) == 0:
        return []
    text = text.replace(' ', '')
    if len(text) > 0:
        return text.split('\r')
    else:
        return create_empty_result(len(money))


def treat_multi_float_num(money, text, reg):
    """
    处理多行浮点数（数量、单价、金额、税率、税额）
    :param money:
    :param text:
    :return:
    """
    if len(money) == 0:
        return []
    text = text.replace(' ', '')
    if len(text) > 0:
        units = text.split('\r')
        arr = []
        for unit in units:
            single = treat_float_num(unit, reg)
            if len(single) > 0:
                arr.append(treat_float_num(unit, reg))
        return arr
    else:
        return create_empty_result(len(money))


def treat_quantity(money, text):
    """
    数量
    :param money:
    :param text:
    :return:
    """
    if len(money) == 0:
        return []
    text = text.replace(' ', '')
    if len(text) > 0:
        units = text.split('\r')
        arr = []
        for unit in units:
            arr.append(treat_float_num(unit, '[1-9][0-9\\.]{1,30}'))
        return units
    else:
        return create_empty_result(len(money))


def create_empty_result(num):
    arr = []
    for index in range(num):
        arr.append('')
    return arr


def treat_float_num(text, reg, group_index=0):
    """
    处理浮点型的数字
    :param text:
    :return:
    """
    # 去除空格
    text = text.replace(' ', '')
    return treat_by_reg(text, reg, group_index)


def treat_buyer_name(payer_arr, top_ocr_results):
    """
    处理购买者姓名
    :param buyer_arr:
    :param full_text:
    :return:
    """
    text = payer_arr[0] if len(payer_arr) == 4 else ''
    if len(text) == 0:
        # 从原始坐标中匹配（跟名称Y坐标最接近，且距离最近，且在右边）
        for item in top_ocr_results:
            print("做到根据位置查询匹配的字段")

    # 常规后处理
    text = text.replace("：", ":")
    if text.__contains__(":"):
        index = text.find(":")
        if text.endswith('名'):
            text = text[:len(text) - 1]
        return text[index + 1:]

    text = text.replace('名称', '')
    if text.startswith('称'):
        text = text[1:]
    if text.endswith('名'):
        text = text[:len(text) - 1]
    return text


def match_right_horizontal_field(keyword_arr, src_ocr_result):
    """
    根据关键词，从ocr识别结果中找到与在关键词组右侧，且基本在同一个水平线上的文本
    匹配规则：Y轴最接近、且X坐标也最接近。
    :param keyword_arr:
    :param src_ocr_result:
    :return:
    """
    # TODO 做到这个方法


def treat_bank(text):
    # 购买者姓名
    text = text.replace("：", ":")
    if text.__contains__(":"):
        index = text.find(":")
        return text[index + 1:]
    return text


def treat_addr_tell(text):
    """
    地址电话
    :param text:
    :return:
    """
    import re
    text = re.sub('[：:、,，]+', '', text)
    text = text.replace('地址', '')
    text = text.replace('电话', '')
    return text


def treat_payee(text):
    text = remove_special_char(text)
    text = text.replace("：", "").replace('收款人', '').replace('款人', '')
    if text.startswith('人'):
        text = text[1:]
    return text


def treat_review(text):
    text = remove_special_char(text)
    text = text.replace("：", "").replace('复核', '')
    if text.startswith('核'):
        text = text[1:]
    return text


def treat_drawer(text):
    text = remove_special_char(text)
    text = text.replace("：", "").replace('开票人', '').replace('票人', '')
    if text.startswith('人'):
        text = text[1:]
    return text


def treat_tax_id_number(text):
    """
    处理纳税人识别号
    :param text:
    :return:
    """
    text = text.replace("：", ":")
    if text.__contains__(":"):
        index = text.find(":")
        return text[index + 1:]
    return text


def treat_validate_code(text):
    """
    处理校验码
    :param text:
    :return:
    """
    import re
    text = re.sub('[：:、,，]+', '', text)
    return text


if __name__ == '__main__':
    # print(digital_to_chinese(123456789.456))
    # print(digital_to_chinese(123.456))
    # print(digital_to_chinese(0.456))
    # print(digital_to_chinese(1.23))
    # print(digital_to_chinese(1.2))
    # print(digital_to_chinese(555))
    # print(digital_to_chinese(199999.22))
    print(digital_to_chinese(4600.05))
    print(digital_to_chinese('4600.00'))
    print(digital_to_chinese('4600.0'))
    print(digital_to_chinese('708.0'))
    print(digital_to_chinese('7008.0'))
    print(digital_to_chinese('9050.0'))
