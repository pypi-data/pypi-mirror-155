#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 后处理脚本&正则处理脚本

from paddleocr.ppocr.utils.logging import get_logger

from yrocr.resources.post_process.util import juege_angle, treat_by_reg

logger = get_logger(name='idcart_reverse')


def get_rotate_angle(txt_result):
    """
    个性化的判断图像旋转角度判断方法
    :param img_path:
    :param txt_result:
    :return:
    """
    logger.info("执行【身份证_背面】角度判断方法")
    judge_txts = ['中华人民共和国', '居民身份证']
    return juege_angle(judge_txts, txt_result)


def post_process(image, result, txt_result, use_show_name):
    # 特殊处理1【有效期限】 2018.11.06-2028.1106
    txts = [item['text'] for item in txt_result]
    full_text = "".join(txts)
    logger.info(f"全文:{full_text}")
    result['签发机关'] = treat_issue_org(str(result['签发机关']), full_text)
    result['有效期限'] = treat_peroid(str(result['有效期限']), full_text)
    return result


def treat_issue_org(text, full_text):
    """
    处理签发机关
    :param text:
    :param full_text:
    :return:
    """
    # 不包含公安，或字数太少的，为错误的
    if len(text) < 5 or not text.__contains__('公安'):
        # 从全文中检索
        regs = [
            '签发机关([\u4E00-\u9FA5]{5,30})有效期限',
            '签机关([\u4E00-\u9FA5]{5,30})有效期限',
            '机关([\u4E00-\u9FA5]{5,30})有效期限',
        ]
        for reg in regs:
            result = treat_by_reg(full_text, reg, 1)
            if len(result) > 0:
                return result
    else:
        # 如果是以签发机关开头的，则要截取
        if text.__contains__('机关'):
            index = text.index('机关')
            return text[index + 2:]
    return text


def treat_peroid(text, full_text):
    """
    处理有限期限
    :param text:
    :param full_text:
    :return:
    """
    if len(text) >= 10:
        import re
        remove_chars = '[\.\-:：\,]+'
        text = re.sub(remove_chars, '', text)
        regs = [
            '20[0-9]{2}[0-9]{4}20[0-9]{2}[0-9]{4}',
            '20[0-9]{2}[0-9]{2}[0-9]{2}长期'
        ]
        for reg in regs:
            result = treat_by_reg(text, reg)
            if len(result) > 0:
                return format_period(result)

    regs = [
        '20[0-9]{2}\.[0-9]{2}\.[0-9]{2}\-20[0-9]{2}\.[0-9]{2}\.[0-9]{2}',
        '20[0-9]{2}\.[0-9]{2}\.[0-9]{2}\-长期'
    ]
    for reg in regs:
        result = treat_by_reg(full_text, reg)
        if len(result) > 0:
            return result

    # 特殊处理1：到这里了，极大概率是异常的情况（去除掉.号，先保留横杠尝试抽取） 2009.1119-20191119
    remove_chars = '[\.:：\,]+'
    import re
    new_full_text = re.sub(remove_chars, '', full_text)
    regs = [
        '20[0-9]{2}[0-9]{4}\-20[0-9]{2}[0-9]{4}',
        '20[0-9]{2}[0-9]{2}[0-9]{2}\-长期'
    ]
    for reg in regs:
        result = treat_by_reg(new_full_text, reg)
        if len(result) > 0:
            return format_period(result)

    # 特殊处理2：横杠也没有,直接取数字
    remove_chars = '[\.\-:：\,]+'
    new_full_text = re.sub(remove_chars, '', full_text)
    regs = [
        '20[0-9]{2}[0-9]{4}20[0-9]{2}[0-9]{4}',
        '20[0-9]{2}[0-9]{2}[0-9]{2}长期'
    ]
    for reg in regs:
        result = treat_by_reg(new_full_text, reg)
        if len(result) > 0:
            return format_period(result)

    # 特殊处理3，到这里了，可以尝试抽取2005.11.11-2025 这种的挣扎下。结束日期的月日可以补全。
    reg = '20[0-9]{2}\.[0-9]{2}\.[0-9]{2}\-20[0-9]{2}'
    result = treat_by_reg(full_text, reg)
    if len(result) > 0:
        result = result + '.' + result[5:7] + '.' + result[8:10]
        return result

    # TODO 做到这边623.jpg特殊处理4：有效期限2006.1221-长
    remove_chars = '[\.\-:：\,]+'
    new_full_text = re.sub(remove_chars, '', full_text)
    reg = '20[0-9]{2}\.[0-9]{2}\.[0-9]{2}\-20[0-9]{2}'
    result = treat_by_reg(full_text, reg)
    if len(result) > 0:
        result = result + '.' + result[5:7] + '.' + result[8:10]
        return result

    return ''


def format_period(text):
    """
    格式化有效期
    :param text:
    :return:
    """
    import re
    remove_chars = '[\.\-:：\,]+'
    text = re.sub(remove_chars, '', text)
    if text.__contains__('长期'):
        return text[0:4] + '.' + text[4:6] + '.' + text[6:8] + '-长期'
    return text[0:4] + '.' + text[4:6] + '.' + text[6:8] + '-' + text[8:12] + '.' + text[12:14] + '.' + text[14:16]


if __name__ == '__main__':
    result = {
        "出生": "",
        "住址": "",
        "公民身份号码": "",
        "姓名": "",
        "性别": "",
        "民族": "",
        "签发机关": "",
        "有效期限": "",
        'sex_nation': ''
    }
    # ocr结果只返回全文
    txt_result = [
        {
            'text': '姓名省新性别男民族汉出生1987年1月25日住址湖北省枣阳市王城镇李桥村一组公民身份号码420683198701254037中华人民共和国居民身份证签发机关枣阳市公安局有效期限2016.10.17-2036.10.17'
        }
    ]
    final_result = post_process('', result, txt_result, False)
    import json

    #
    print(json.dumps(final_result, indent=4, ensure_ascii=False))
    import pandas  as pd

    # 验证全部
    df = pd.read_excel('../../test/身份证_1026.xlsx')
    print(df)
    datas = []
    for index, row in df.iterrows():
        file_name = row['file_name']
        result = {
            "出生": "",
            "住址": "",
            "公民身份号码": "",
            "姓名": "",
            "性别": "",
            "民族": "",
            "签发机关": row['issue_org'],
            "有效期限": row['validate_date'],
            'sex_nation': ''
        }
        txt_result = [
            {
                'text': str(row['全文']) + ''
            }
        ]
        final_result = post_process('', result, txt_result, False)
        final_result['file_name'] = row['file_name']
        new_data = {
            "签发机关": final_result['签发机关'],
            "有效期限": final_result['有效期限'],
            "全文": str(row['全文']),
            "文件名": file_name,
        }
        datas.append(new_data)
    print("解析完毕")
    new_df = pd.DataFrame(datas)
    new_df.to_excel('身份证_背面正则.xlsx', index=False)
    print('finish')
