#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 增值税专用发票后处理

from yrocr.resources.post_process.invoice_base import *
from yrocr.resources.post_process.util import *

logger = get_logger(name='vat_special_invoice')


def get_rotate_angle(ocr_src_results):
    logger.info("执行【增值税专用发票/普通发票】角度判断方法")
    judge_txts = ['货物或应税劳务服务名称', '价税合计大写']
    return juege_angle(judge_txts, ocr_src_results)


def post_process(image, result, ocr_src_results, use_show_name):
    """
    需抽取的字段有：
    【开票日期、购买方地址、电话、购买方开户行及账号、销售方开户行及账号、销售方地址、
    电话、开票人、收款人、复核、货物或服务名称、单位、数量、单价、金额明细、税率、税额明细】

    额外新增：

    :param img_path:
    :param result:
    :param ocr_src_results: ocr原始结果
    :param use_show_name:
    :return:
    """
    txts = [item['text'] for item in ocr_src_results]
    full_text = "。".join(txts)
    logger.info(f"全文:{full_text}")

    # 从【密码区】区分开左右两边的数据
    left_text, right_text = split_left_right_by_arrs(ocr_src_results, ['密码区', '密码', '密', '码', '区'], split_text="。")
    # 从 货物名称、价税分为 上下两部分数据（上面的为购买方）
    top_ocr_results, bottom_ocr_result = split_top_bottom(ocr_src_results, ['货物', '应税劳务', '服务名称', '规格', '数量', '单价', '税率', '税额'])
    top_text = "。".join([item['text'] for item in top_ocr_results])
    bottom_text = "。".join([item['text'] for item in bottom_ocr_result])
    logger.info(f"左侧全文:{left_text}")
    logger.info(f"右侧全文:{right_text}")
    logger.info(f"上方全文:{top_text}")
    logger.info(f"下方全文:{bottom_text}")

    # 处理购买方
    key = '购买方_多行'
    payer_info = result[key]
    payer_arr = payer_info.split('\r')
    payer_name = treat_buyer_name(payer_arr, top_ocr_results)

    payer_id = payer_info[1] if len(payer_info) == 4 else ''
    payer_id = treat_tax_id_number(payer_id)
    payer_addr_tell = payer_info[2] if len(payer_info) == 4 else ''
    payer_addr_tell = treat_addr_tell(payer_addr_tell)

    payer_bank_account = payer_info[3] if len(payer_info) == 4 else ''
    payer_bank_account = treat_bank(payer_bank_account)
    if use_show_name:
        result['payer_name'] = payer_name
        result['payer_id'] = payer_id
        result['payer_addr_tell'] = payer_addr_tell
        result['payer_bank_account'] = payer_bank_account
    else:
        result['购买方名称'] = payer_name
        result['购买方纳税人识别号'] = payer_id
        result['购买方地址电话'] = payer_addr_tell
        result['购买方开户行及账号'] = payer_bank_account
    del result[key]

    # 处理销售方

    key = '销售方_多行'
    seller_info = result[key]
    seller_arr = seller_info.split('\r')
    seller_name = treat_buyer_name(seller_arr, top_ocr_results)
    seller_id = seller_arr[1] if len(seller_arr) == 4 else ''
    seller_id = treat_tax_id_number(seller_id)
    buyer_addr_tell = seller_arr[2] if len(seller_arr) == 4 else ''
    buyer_addr_tell = treat_addr_tell(buyer_addr_tell)

    buyer_bank_account = seller_arr[3] if len(seller_arr) == 4 else ''
    buyer_bank_account = treat_bank(buyer_bank_account)
    if use_show_name:
        result['seller_name'] = seller_name
        result['seller_id'] = seller_id
        result['seller_addr_tell'] = buyer_addr_tell
        result['seller_bank_account'] = buyer_bank_account
    else:
        result['销售方名称'] = seller_name
        result['销售方纳税人识别号'] = seller_id
        result['销售方地址电话'] = buyer_addr_tell
        result['销售方开户行及账号'] = buyer_bank_account
    del result[key]

    result['总金额'] = treat_total_money(result['总金额'], ocr_src_results)
    result['总税额'] = treat_total_total_tax(result['总税额'], ocr_src_results)
    result['价税合计小写'] = treat_total_cover_tax_lower(result['价税合计小写'], ocr_src_results)
    result['价税合计大写'] = treat_total_cover_tax_upper(result['价税合计大写'], result['价税合计小写'], full_text)

    result['发票代码'] = treat_by_reg(result['发票代码'], '[0-9]{10}')
    result['发票号码'] = treat_vat_invoice_number(result['发票号码'], ocr_src_results)
    result['开票日期'] = treat_issue_date(result['开票日期'], full_text)
    result['收款人'] = treat_payee(result['收款人'])
    result['复核'] = treat_review(result['复核'])
    result['开票人'] = treat_drawer(result['开票人'])
    result['密码'] = treat_cipher(result['密码'], full_text, right_text)

    # 列表项 [货物名称_多行、规格型号_多行、单位_多行、数量_多行、单价_多行、金额_多行、税率_多行、税额_多行]
    # 多行的例子 239.jpg ,288.jpg
    key = '金额_多行'
    money = treat_money(result[key])
    del result[key]
    # 货物名称（文本）
    key = '货物名称_多行'
    goods = treat_multi_text(money, result[key])
    del result[key]
    # 规则型号（文本）
    key = '规格型号_多行'
    plate_specific = treat_multi_text(money, result[key])
    del result[key]

    # 单位（文本）
    key = '单位_多行'
    unit = treat_multi_text(money, result[key])
    del result[key]

    # 数量 整数/浮点数/空值
    key = '数量_多行'
    quantity = treat_multi_float_num(money, result[key], '[1-9][0-9\\.]{0,30}')
    del result[key]

    key = '单价_多行'
    price = treat_multi_float_num(money, result[key], '[0-9\\.]{1,30}')
    del result[key]

    key = '税率_多行'
    tax_rate = treat_multi_float_num(money, result[key], '[1-9]{1,2}' + '%')
    del result[key]

    key = '税额_多行'
    tax = treat_multi_float_num(money, result[key], '[0-9]{1,10}\\.[0-9]{2}')
    del result[key]

    if use_show_name:
        result['goods'] = goods
        result['plate_specific'] = plate_specific
        result['unit'] = unit
        result['quantity'] = quantity
        result['price'] = price
        result['money'] = money
        result['tax_rate'] = tax_rate
        result['tax'] = tax
        # 无法判断是普通还是通用。先不判断，后面再来
        result['invoce_type'] = tax
    else:
        result['货物名称'] = goods
        result['规格型号'] = plate_specific
        result['单位'] = unit
        result['数量'] = quantity
        result['单价'] = price
        result['金额'] = money
        result['税率'] = tax_rate
        result['税额'] = tax

    return result


if __name__ == '__main__':
    result = {

    }
    result = post_process('', result, '', '')
    import json

    print(json.dumps(result, indent=4, ensure_ascii=False))
