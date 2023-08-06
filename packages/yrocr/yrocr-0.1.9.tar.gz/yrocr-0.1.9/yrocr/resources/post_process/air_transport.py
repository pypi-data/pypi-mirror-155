#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 飞机行程单后处理脚本&正则处理脚本
from paddleocr.ppocr.utils.logging import get_logger
import re
from yrocr.resources.post_process.util import juege_angle, treat_by_reg

logger = get_logger(name='air_transport')

province_map = {
    '河北省': ['石家庄', '保定', '秦皇岛', '唐山', '邯郸', '邢台', '沧州', '承德', '廊坊', '衡水', '张家口'],
    '山西省': ['太原', '大同', '阳泉', '长治', '临汾', '晋中', '运城', '晋城', '忻州', '朔州', '吕梁'],
    '内蒙古': ['呼和浩特', '呼伦贝尔', '包头', '赤峰', '乌海', '通辽', '鄂尔多斯', '乌兰察布', '巴彦淖尔'],
    '辽宁省': ['盘锦', '鞍山', '抚顺', '本溪', '铁岭', '锦州', '丹东', '辽阳', '葫芦岛', '阜新', '朝阳', '营口'],
    '吉林省': ['吉林', '通化', '白城', '四平', '辽源', '松原', '白山'],
    '黑龙江省': ['伊春', '牡丹江', '大庆', '鸡西', '鹤岗', '绥化', '双鸭山', '七台河', '佳木斯', '黑河', '齐齐哈尔'],
    '江苏省': ['无锡', '常州', '扬州', '徐州', '苏州', '连云港', '盐城', '淮安', '宿迁', '镇江', '南通', '泰州'],
    '浙江省': ['绍兴', '温州', '湖州', '嘉兴', '台州', '金华', '舟山', '衢州', '丽水'],
    '安徽省': ['合肥', '芜湖', '亳州', '马鞍山', '池州', '淮南', '淮北', '蚌埠', '巢湖', '安庆', '宿州', '宣城', '滁州', '黄山', '六安', '阜阳', '铜陵'],
    '福建省': ['福州', '厦门', '泉州', '漳州', '南平', '三明', '龙岩', '莆田', '宁德'],
    '江西省': ['南昌', '赣州', '景德镇', '九江', '萍乡', '新余', '抚州', '宜春', '上饶', '鹰潭', '吉安'],
    '山东省': ['潍坊', '淄博', '威海', '枣庄', '泰安', '临沂', '东营', '济宁', '烟台', '菏泽', '日照', '德州', '聊城', '滨州', '莱芜'],
    '河南省': ['郑州', '洛阳', '焦作', '商丘', '信阳', '新乡', '安阳', '开封', '漯河', '南阳', '鹤壁', '平顶山', '濮阳', '许昌', '周口', '三门峡', '驻马店'],
    '湖北省': ['荆门', '咸宁', '襄樊', '荆州', '黄石', '宜昌', '随州', '鄂州', '孝感', '黄冈', '十堰'],
    '湖南省': ['长沙', '郴州', '娄底', '衡阳', '株洲', '湘潭', '岳阳', '常德', '邵阳', '益阳', '永州', '张家界', '怀化'],
    '广东省': ['江门', '佛山', '汕头', '湛江', '韶关', '中山', '珠海', '茂名', '肇庆', '阳江', '惠州', '潮州', '揭阳', '清远', '河源', '东莞', '汕尾', '云浮'],
    '广西省': ['南宁', '贺州', '柳州', '桂林', '梧州', '北海', '玉林', '钦州', '百色', '防城港', '贵港', '河池', '崇左', '来宾'],
    '海南省': ['海口', '三亚'],
    '四川省': ['成都', '乐山', '雅安', '广安', '南充', '自贡', '泸州', '内江', '宜宾', '广元', '达州', '资阳', '绵阳', '眉山', '巴中', '攀枝花', '遂宁', '德阳'],
    '贵州省': ['贵阳', '安顺', '遵义', '六盘水'],
    '云南省': ['昆明', '玉溪', '大理', '曲靖', '昭通', '保山', '丽江', '临沧'],
    '西藏': ['拉萨', '阿里'],
    '陕西省': ['咸阳', '榆林', '宝鸡', '铜川', '渭南', '汉中', '安康', '商洛', '延安'],
    '甘肃省': ['兰州', '白银', '武威', '金昌', '平凉', '张掖', '嘉峪关', '酒泉', '庆阳', '定西', '陇南', '天水'],
    '青海省': ['西宁'],
    '宁夏': ['银川', '固原', '青铜峡', '石嘴山', '中卫'],
    '新疆': ['乌鲁木齐', '克拉玛依']
}


def get_rotate_angle(txt_result):
    """
    个性化的判断图像旋转角度判断方法
    :param txt_result:
    :return:
    """
    logger.info("执行【飞机行程单】角度判断方法")
    judge_txts = ['航空运输电子客票行程单']
    return juege_angle(judge_txts, txt_result)


def post_process(image, result, txt_result, use_show_name):
    txts = [item['text'] for item in txt_result]
    full_text = "。".join(txts)
    logger.info(f"全文:{full_text}")

    result['有效身份证件号码'] = treat_idnum(result['有效身份证件号码'], full_text)
    result['印刷序号'] = treat_print_no(result['印刷序号'], full_text)
    from_text, to_text = treat_from_to(result['from'], result['from'], full_text)
    result['from'] = from_text
    result['to'] = to_text
    # 有效截止日期、行李，如：。11JUN 20K。
    end_date, free_baggage = treat_end_date_baggage(result['有效截止日期_行李'], full_text)
    ticket_price, dev_found_price, total_price = treat_price_info(full_text)

    flight_number, site_level, date, ticket_level = treat_date_seat(result['航班号_座位_日期'], full_text)
    if use_show_name:
        result['flight_number'] = flight_number
        result['site_level'] = site_level
        result['departure_date'] = date
        result['ticket_level_reg'] = ticket_level
        result['end_date'] = end_date
        result['free_baggage'] = free_baggage

        result['ticket_price'] = ticket_price
        result['dev_found_price'] = dev_found_price
        result['total_price'] = total_price
    else:
        result['航班'] = flight_number
        result['座位等级'] = site_level
        result['出发日期'] = date
        result['客票级别'] = ticket_level
        result['有效截止日期'] = end_date
        result['免费行李'] = free_baggage
        result['ticket_price'] = ticket_price
        result['dev_found_price'] = dev_found_price
        result['total_price'] = total_price
    del result['航班号_座位_日期']
    del result['有效截止日期_行李']
    del result['价格信息']

    return result


def treat_price_info(full_text):
    """
    处理价格信息[票价、民航发展基金、总价]
    。500YQ。34330.00。1280.00CN。
    :param text:
    :param full_text:
    :return:
    """
    # 票价：1280.00CN
    ticket_price_reg = '([1-9][0-9]{2,4})\.00CN'
    dev_found_price_reg = '。([1-9][0-9]{1,2})\.00YQ。'
    total_price_reg = '。([1-9][0-9]{2,4})\.00。'

    ticket_price = treat_by_reg(full_text, ticket_price_reg, 1)
    dev_found_price = treat_by_reg(full_text, dev_found_price_reg, 1)
    total_price = treat_by_reg(full_text, total_price_reg, 1)
    return ticket_price, dev_found_price, total_price


def treat_end_date_baggage(text, full_text):
    """
    处理有效截止日期、行李。11JUN 20K。

    :param text:
    :param full_text:
    :return:
    """
    reg = '。([0-9]{1,2})(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) ([0-9]{1,3}K)。'
    result = re.search(reg, text)
    if result:
        end_date = result.group(1) + result.group(2)
        free_baggage = result.group(3)
        return end_date, free_baggage
    else:
        result = re.search(reg, full_text)
        if result:
            end_date = result.group(1) + result.group(2)
            free_baggage = result.group(3)
            return end_date, free_baggage
    return '', ''


def treat_from_to(from_text, to_text, full_text):
    """
    处理from、to。除了 福州-长乐这样的，还有可能是【银州】、【成都】这样的
    :param from_text:
    :param to_text:
    :param full_text:
    :return:
    """
    addr_reg = '[\u4e00-\u9fa5]{2,3}\-[\u4e00-\u9fa5]{2,3}'
    from_text = treat_by_reg(from_text, addr_reg)
    to_text = treat_by_reg(to_text, addr_reg)
    if from_text and to_text:
        return from_text, to_text

    result = re.finditer(addr_reg, full_text)
    addrs = []
    for item in result:
        addrs.append(item.group())
    if len(addrs) >= 2:
        return addrs[0], addrs[1]
    elif len(addrs) == 1:
        return addrs[0]
    return '', ''


def treat_date_seat(text, full_text):
    """
    处理：航班编号、座位等级、日期、客票类型
    航班编号： 厦航MF8235（两个中文+两个字母+四个数字）
    座位等级： 单个字母
    日期：2021-04-1010:15
    日期后的：客票级别 单个英文字母（V、Q）+ 四个数字
    :param text:
    :param full_text:
    :return:
    """
    text = text.replace(' ', '')
    full_text = full_text.replace(' ', '')
    flight_number_reg = '[\u4e00-\u9fa5]{2}[a-zA-Z]{2}[0-9]{4}'
    site_level_reg = '[A-Z]'
    date_reg = '20[0-9]{2}\-[0-9]{2}\-[0-9]{4}\:[0-9]{2}'
    ticket_level_reg = '[A-Z]|[A-Z][0-9]{4}'

    date_result = re.search(date_reg, text)
    if date_result:
        prefix_text = text[0:date_result.start()]
        suffix_text = text[date_result.end():]
        flight_number = treat_by_reg(prefix_text, flight_number_reg)
        site_level = treat_by_reg(prefix_text, site_level_reg)
        ticket_level = treat_by_reg(suffix_text, ticket_level_reg)
        date = format_departure_date(date_result.group())
        return flight_number, site_level, date, ticket_level
    else:
        date_result = re.search(date_reg, full_text)
        if date_result:
            prefix_text = full_text[0:date_result.start()]
            suffix_text = full_text[date_result.end():]
            flight_number = treat_by_reg(prefix_text, flight_number_reg)
            site_level = treat_by_reg(prefix_text, site_level_reg)
            ticket_level = treat_by_reg(suffix_text, ticket_level_reg)
            date = format_departure_date(date_result.group())
            return flight_number, site_level, date, ticket_level
        else:
            return '', '', '', ''


def format_departure_date(date):
    """
    格式化出发时间：2021-04-1010:15 ==> 2021-04-1010:15
    :param date:
    :return:
    """
    date = date[0:10] + ' ' + date[10:]
    return date


def treat_print_no(text, full_text):
    reg = '[0-9]{10} [0-9]'
    print_no = treat_by_reg(text, reg)
    if len(print_no) == 0:
        reg1 = '。([0-9]{10} [0-9])。'
        reg2 = '。([0-9]{10}[0-9])。'
        print_no = treat_by_reg(full_text, reg1, 1)
        if not print_no:
            return treat_by_reg(full_text, reg2, 1)
    return print_no


def treat_idnum(idnum, full_text):
    reg = '[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]'
    birth = treat_by_reg(idnum, reg)
    if len(birth) == 0:
        return treat_by_reg(full_text, reg)
    return birth
