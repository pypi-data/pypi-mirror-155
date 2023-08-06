from yrocr.resources.post_process.util import treat_by_reg, get_text_between_start_end_key


def treat_unified_social_credit_code(text, full_text):
    """
    统一社会信用代码
    :param text:
    :param full_text:
    :return:
    """
    reg = '[0-9a-zA-Z]{18}'
    code = treat_by_reg(text, reg)
    if len(code) == 0:
        code = treat_by_reg(full_text, reg)
    return code


def treat_money(text, full_text):
    """
    注册资金
    :param text:
    :param full_text:
    :return:
    """
    # 容易错误识别的文字
    text = text.replace('什', '仟')
    full_text = full_text.replace('什', '仟')

    reg = '[壹贰叁肆伍陆柒捌玖拾佰仟万亿圆元整零角分]{2,30}|[0-9\.]{3,30}[万元整]{2,3}'
    money = treat_by_reg(text, reg)
    if len(money) == 0:
        money = treat_by_reg(full_text, reg)
    return money
