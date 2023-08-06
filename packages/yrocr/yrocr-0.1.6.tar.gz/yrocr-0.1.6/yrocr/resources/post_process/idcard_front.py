#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 后处理脚本&正则处理脚本

from paddleocr.ppocr.utils.logging import get_logger
from yrocr.resources.post_process.util import juege_angle, treat_by_reg, extract_from_range_features

logger = get_logger(name='idcart_front')
nations = [
    '汉', '蒙古', '回', '藏', '维吾尔', '苗', '彝', '壮', '布依', '朝鲜', '满', '侗', '瑶', '白', '土家', '哈尼', '哈萨克',
    '傣', '黎', '僳僳', '佤', '畲', '高山', '拉祜', '水', '东乡', '纳西', '景颇', '柯尔克孜', '土', '达斡尔', '仫佬', '羌',
    '布朗', '撒拉', '毛南', '仡佬', '锡伯', '阿昌', '普米', '塔吉克', '怒', '乌孜别克', '俄罗斯', '鄂温克', '德昂', '保安', '裕固',
    '京', '塔塔尔', '独龙', '鄂伦春', '赫哲', '门巴', '珞巴', '基诺'
]


def get_rotate_angle(txt_result):
    """
    个性化的判断图像旋转角度判断方法
    :param img_path:
    :param txt_result:
    :return:
    """
    logger.info("执行【身份证_正面】角度判断方法")
    judge_txts = ['公民身份号码', '住址', '姓名', '性别', '民族']
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
    # 调试用
    #result['全文'] = full_text

    result['姓名'] = treat_name(result['姓名'], full_text)
    result['住址'] = treat_addr(result['住址'], full_text)
    result['公民身份号码'] = treat_id_number(str(result['公民身份号码']), full_text)
    result['出生'] = treat_birth(result['出生'], full_text)
    sex_nation = result['sex_nation']
    sex = treat_sex(sex_nation, full_text)
    nation = treat_nation(sex_nation, full_text)
    if use_show_name:
        result['sex'] = sex
        result['nation'] = nation
    else:
        result['性别'] = sex
        result['民族'] = nation

    del result['sex_nation']
    return result


def treat_birth(birth, full_text):
    birth = treat_by_reg(birth, '[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日')
    if len(birth) == 0:
        return treat_by_reg(full_text, '[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日')
    return birth


def treat_sex(sex_nation, full_text):
    if sex_nation.__contains__('男'):
        return '男'
    elif sex_nation.__contains__('女'):
        return '女'
    else:
        return '女' if full_text.__contains__("女") else '男'


def treat_nation(sex_nation, full_text):
    """
    处理民族：必须校验最终返回的民族在1～4位
    :param sex_nation:
    :param full_text:
    :return:
    """
    if sex_nation.__contains__('民族'):
        index = sex_nation.index('民族')
        result = sex_nation[index + 2:]
        if 4 >= len(result) >= 1:
            return result
    # 从全文中查询
    features = [
        {'start': '民族', 'end': '出生'},
    ]
    result = extract_from_range_features(full_text, features)
    if 4 >= len(result) >= 1:
        return result

    # 包含五十六个民族（民族+ val，或民+val）
    for nation in nations:
        if full_text.__contains__('民族' + nation) or full_text.__contains__('民' + nation):
            return nation
    return ''


def treat_id_number(id_number, full_text):
    """
    身份证：【公民身份号码】35052119880720203×
    :param id_number:
    :return:
    """
    import re
    biz_reg = '[1-9]\d{5}(18|19|20)\d{9}[0-9Xx]'
    id_number = treat_by_reg(id_number, biz_reg)
    if len(id_number) == 0:
        id_number = treat_by_reg(full_text, biz_reg)
        id_number = re.sub('[×x]+', 'X', id_number)
        return id_number

    id_number = re.sub('[×x]+', 'X', id_number)
    return id_number


def treat_addr(addr, full_text):
    """
    住址:经常容易出现 住址被识别为【往】址。
    :param addr:
    :return:
    """
    if addr.__contains__("住址"):
        # 错乱的情况：日OR日9964用住址武汉市汉阳区知音面村130号
        index = addr.index('住址')
        return addr[index + 2:]
    elif addr.__contains__("任址"):
        index = addr.index('任址')
        return addr[index + 2:]
    elif addr.__contains__("性址"):
        index = addr.index('性址')
        return addr[index + 2:]
    elif addr.startswith("往") or addr.startswith("任") or addr.startswith("性"):
        addr = addr[1:]
        return addr

    # 还为空，则从全文中截取位于【特征开始字符】、【特征结束字符】之间的字符。如：【性址】湖北省孝感市孝南区车站街153号【民身份号码】
    features = [
        {'start': '姓址', 'end': '公民身份'},
        {'start': '住址', 'end': '公民身份'},
        {'start': '性址', 'end': '公民身份'},
        {'start': '任址', 'end': '公民身份'},

        {'start': '姓址', 'end': '公民身务'},
        {'start': '住址', 'end': '公民身务'},
        {'start': '性址', 'end': '公民身务'},
        {'start': '任址', 'end': '公民身务'},

        {'start': '姓址', 'end': '公身份号'},
        {'start': '住址', 'end': '公身份号'},
        {'start': '性址', 'end': '公身份号'},
        {'start': '任址', 'end': '公身份号'},

        {'start': '姓址', 'end': '公份号'},
        {'start': '住址', 'end': '公份号'},
        {'start': '性址', 'end': '公份号'},
        {'start': '任址', 'end': '公份号'},

        {'start': '姓址', 'end': '民身份号'},
        {'start': '住址', 'end': '民身份号'},
        {'start': '性址', 'end': '民身份号'},
        {'start': '任址', 'end': '民身份号'},
    ]
    result = extract_from_range_features(full_text, features)
    if len(result) > 0:
        if result.__contains__("签发机关"):
            index = result.index('签发机关')
            return result[0:index]
        return result
    return addr


def treat_name(name, full_text):
    """
    处理姓名
    场景1：姓名后包含了性别，说明识别错乱了，如：姓名朱文博性别男民族汉
    肠镜2：未匹配到，但全文中有
    :param result:
    :param full_text:
    :return:
    """

    if name.__contains__('性别'):
        index = name.index('性别')
        return name[0:index]
    # 字数太长或包含不应包含的文字时，则认为抽取错误。如：彭世峰姓别男民族汉
    elif len(name) == 0 or len(name) > 10 or name.__contains__('民族'):
        # 没识别到的，从全文中特征查询(改为正则更合适
        regs = [
            '姓名([\u4E00-\u9FA5]{2,4})性别',
            '姓名([\u4E00-\u9FA5]{2,4})姓别',
            '姓名([\u4E00-\u9FA5]{2,4})姓姓',
            '姓名([\u4E00-\u9FA5]{2,4})性姓',
            '姓名([\u4E00-\u9FA5]{2,4})姓性',
            '姓名([\u4E00-\u9FA5]{2,4})性性',
            '姓名([\u4E00-\u9FA5]{2,4})姓男',
            '名([\u4E00-\u9FA5]{2,4})性别',
            '名([\u4E00-\u9FA5]{2,4})姓别',
            '名([\u4E00-\u9FA5]{2,4})姓姓',
            '名([\u4E00-\u9FA5]{2,4})性姓',
            '名([\u4E00-\u9FA5]{2,4})姓性',
            '名([\u4E00-\u9FA5]{2,4})性性',
        ]
        for reg in regs:
            result = treat_by_reg(full_text, reg, 1)
            if len(result) > 0:
                return result

    # 极端情况下，只识别到如："李胜华男汉1972214湖北省孝" 之类的内容
    pre_text_features = [
        '男汉', '男民族', '女汉', '女民族'
    ]
    for pre_text in pre_text_features:
        if full_text.__contains__(pre_text):
            index = full_text.index(pre_text)
            # 在前面三个字以内
            if index <= 3:
                return full_text[0:index]

    return name


if __name__ == '__main__':
    # 电子证照识别结果设置为空
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
            'text': '姓名赵永华姓别男民族汉出生1968年11月4日性址武汉市区南区纱帽街分苑路135-5-1号公民身份号码42010119651104街幼月2中华人民共和国居民身份证签发机关武汉市公安局汉市分局有效期限200612.06-202612.06'
        }
    ]
    final_result = post_process('', result, txt_result, False)
    import json

    print(json.dumps(final_result, indent=4, ensure_ascii=False))
