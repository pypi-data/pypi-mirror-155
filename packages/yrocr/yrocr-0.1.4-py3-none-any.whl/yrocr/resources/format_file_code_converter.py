#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 固定文件编码转化模块
from paddleocr.ppocr.utils.logging import get_logger

logger = get_logger(name='convert_file_code')


def convert_format_file_code(txt_result, format_file_code):
    """
    转化电子证照文件编码
    1. 情况1：自动区分。如发票，需自动区分是电子发票/纸质发票
    2. 情况2：一个证照需拆分为多个部分分别进行识别的，如：身份证需拆分为正面、反面
    3. 无需处理的情况
    :param format_file_code:  ['xxxx'] 或  ['xxxx','yyyy']
    :return:
    """
    if format_file_code == 'idcard':
        # 身份证
        return ['idcard_front', 'idcard_reverse']

    elif format_file_code == 'vat_invoice':
        # 增值税发票统一入口
        # 注：普通发票只有电子版的。
        logger.info("接收到【发票】识别请求")
        txts = [item['text'] for item in txt_result]
        text = "".join(txts)
        if text.__contains__("普通发票") or text.__contains__("发票号码") or text.__contains__("发票代码"):
            logger.info("该发票为【电子普通发票】")
            return ['vat_ele_normal_invoice']
        else:
            logger.info("该发票为纸质发票(专用发票)")
            return ['vat_special_invoice']
    elif format_file_code == 'biz_license_three_in_one':
        # 三证合一营业执照统一入口(营业执照有8种子类型)
        logger.info("接收到【三证合一营业执照】识别请求")
        # 目前只需判断 A版、G版本。默认为A版本
        txts = [item['text'] for item in txt_result]
        text = "".join(txts)
        if text.__contains__("负责人") or text.__contains__("营业场所"):
            logger.info("该营业执照为【G版】")
            return ['biz_license_three_in_one/biz_license_g']
        else:
            logger.info("该营业执照为【A版】")
            return ['biz_license_three_in_one/biz_license_a']


    else:
        return [format_file_code]
