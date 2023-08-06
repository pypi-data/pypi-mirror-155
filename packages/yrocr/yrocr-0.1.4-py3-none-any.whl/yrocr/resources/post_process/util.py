from paddleocr.ppocr.utils.logging import get_logger

logger = get_logger(name='post_process.util')
import math


def juege_angle(judge_txts, txt_result):
    """
    判断倾斜角度
    :param judge_txts:
    :param txt_result:
    :return:
    """
    if len(txt_result) == 0:
        return 0
    avg_angle = 0
    angles = []
    num = 0
    for txt in judge_txts:
        for item in txt_result:
            cur_text = remove_special_char(item['text'])
            if cur_text.__contains__(txt):
                position = item['position']
                # 左上 - 右上
                ydis1 = position[1][1] - position[0][1]
                xdis1 = abs(position[1][0] - position[0][0])
                # 左下 - 右下
                ydis2 = position[2][1] - position[3][1]
                xdis2 = abs(position[3][0] - position[2][0])
                t1 = float(ydis1 / xdis1) if xdis1 > 0 else 0
                t2 = float(ydis2 / xdis2) if xdis2 > 0 else 0
                t = (t1 + t2) / 2
                rotate_angle = math.degrees(math.atan(t))
                logger.info(f"{item['text']}文字角度:{rotate_angle}")
                if rotate_angle == 0:
                    logger.info(f"{item['text']}零度角，直接返回")
                    return 0
                angles.append(rotate_angle)
                if abs(rotate_angle) < 30:
                    avg_angle += rotate_angle
                    num += 1

    if num == 0 or avg_angle == 0:
        return 0
    avg_angle = avg_angle / num
    # 如果有叫角度跟平均值过大，则忽略
    for angle in angles:
        rate = angle / avg_angle
        if rate > 5 or rate < 0.3:
            logger.info(f"角度超过偏离值：{rate},不进行纠正。当前角度：{angle},均值：{avg_angle}")
            return 0
    return avg_angle


def remove_special_char(text):
    import re
    """
    去除特殊字符，包括：标点符号，ascii码小于19的
    :param text:
    :return:
    """
    text = re.sub('[\'!\"#$%&()*+,-./:;<=>?@，。?★、…【】《》？“”^！[\\]_\{\|\}（）：~\s]+', '', text)
    text = re.sub('[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+', '', text)
    return text


def treat_by_reg(text, reg, group_index=0):
    import re
    result = re.search(reg, text)
    if result:
        return result.group(group_index)
    return ''


def find_pre_full_text_by_key(full_text, key_arr):
    """
    通过一组关键词在全文中找到该组关键字前的部分全文内容
    如：营业执照中有两个日期。而【成立日期】在全文中的前半部分。其位于关键词【'法定代表人', '营业期限', '经营范围', '住所'】前面，
    需先截取出这些关键词前的部分全文，用于后续匹配正则
    :param full_text: 全文
    :param key_arr:   关键词数组，ru
    :return:
    """
    for key in key_arr:
        if full_text.__contains__(key):
            index = full_text.index(key)
            return full_text[0:index]
    return ''


def find_suffix_full_text_by_key(full_text, key_arr):
    for key in key_arr:
        if full_text.__contains__(key):
            index = full_text.index(key)
            return full_text[index:]
    return ''


def split_left_right_by_arrs(txt_results, anchor_texts, judge_type='center', split_text=''):
    """
    切割为左右
    :param txt_results:
    :param anchor_texts:
    :param judge_type:
    :param split_text:
    :return:
    """
    for anchor_text in anchor_texts:
        left_text, right_text = split_left_right(txt_results, anchor_text, judge_type, split_text)
        if len(left_text) > 0 and len(right_text) > 0:
            return left_text, right_text
    return '', ''


def split_left_right(txt_results, anchor_text, judge_type='center', split_text=''):
    """
    将ocr文本识别结果切割为左右两部分
    :param txt_results: 文本识别结果数组
    :param anchor_text: 用于判断的锚点文本值
    :param judge_type:  判断类型。center:取锚点中心点为判断；left:取锚点left为判断点
    :param split_text:  切割符号，一般为空格或者句号
    :return:
    """

    find = False
    for item in txt_results:
        if item['text'] == anchor_text:
            anchor_position = item['position']
            find = True
            break
    if not find:
        return '', ''

    left = (anchor_position[0][0] + anchor_position[1][0]) / 2
    if judge_type == 'left':
        left = anchor_position[0][0]

    left_text = ''
    right_text = ''
    for item in txt_results:
        postion = item['position']
        cur_left = postion[0][0]
        if cur_left < left:
            left_text += item['text'] + split_text
        else:
            right_text += item['text'] + split_text

    return left_text, right_text


def split_top_bottom(txt_results, anchors):
    """
    根据高度，将OCR识别的原始结果切割为，上下两个部分。返回原始的txt_result数组
    :param txt_results: 文本识别结果数组
    :param anchors: 用于判断的锚点文本值数组
    :param split_text:  切割符号，一般为空格或者句号
    :return:
    """

    find_anchor = False
    for item in txt_results:
        if is_in_anchor_arr(anchors, item['text']):
            anchor_position = item['position']
            find_anchor = True
    if not find_anchor:
        return [], []

    split_top = anchor_position[0][1]

    top_results = []
    bottom_result = []
    for item in txt_results:
        postion = item['position']
        cur_top = postion[0][1]
        if cur_top < split_top:
            top_results.append(item)
        else:
            bottom_result.append(item)
    return top_results, bottom_result


def split_top_middle_bottom(txt_results, first_anchors, second_anchors, split_text=''):
    """
    根据高度，将OCR识别的原始结果切割为，上中下三个部分
    :param txt_results: 文本识别结果数组
    :param anchor_text: 用于判断的锚点文本值
    :param split_text:  切割符号，一般为空格或者句号
    :return:
    """

    find_first = False
    find_secend = False
    for item in txt_results:
        if is_in_anchor_arr(first_anchors, item['text']):
            first_anchor_position = item['position']
            find_first = True
        if is_in_anchor_arr(second_anchors, item['text']):
            second_anchor_position = item['position']
            find_secend = True

    if not find_first or not find_secend:
        return '', '', ''

    first_top = first_anchor_position[0][1]
    second_top = second_anchor_position[0][1]

    top_text = ''
    middle_text = ''
    bottom_text = ''
    for item in txt_results:
        postion = item['position']
        cur_top = postion[0][1]
        if cur_top < first_top:
            top_text += item['text'] + split_text
        elif cur_top < second_top:
            middle_text += item['text'] + split_text
        else:
            bottom_text += item['text'] + split_text
    return top_text, middle_text, bottom_text


def is_in_anchor_arr(anchors, text):
    """
    判断文本是否匹配 指定锚点中的关键词
    :param anchors: 锚点数组
    :param text: 文本
    :return:
    """
    for anchor in anchors:
        if text.__contains__(anchor):
            return True
    return False


def get_text_between_start_end_key(text, start_key, end_key):
    """
    取两个关键词中间的文本，如
    :param text:
    :param start_key:
    :param end_key:
    :return:
    """
    start = text.index(start_key)
    end = text.index(end_key)
    return text[start + len(start_key):end]


def extract_from_range_features(full_text, features):
    """
    根据特征从全文中搜索特征数组中start & end 之间的字符串
    :param full_text: 全文
    :param features: 特征数组，如[ {'start': '姓名', 'end': '性别'}]
    :return:
    """
    for feature in features:
        if full_text.__contains__(feature['start']) and full_text.__contains__(feature['end']):
            start_index = full_text.index(feature['start'])
            end_index = full_text.index(feature['end'])
            return full_text[start_index + len(feature['start']):end_index]

    return ''
