#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: OCR表格
# @remark: 存在问题：只能识别单个表格。

import os

import cv2
import numpy as np
from paddleocr.ppocr.utils.logging import get_logger

from yrocr.ocr_base import invoke_ocr, draw_text, get_ocr_point_rect
from yrocr.util.cvutil import rotate
from yrocr.util.ocr_util import get_rotate_angle, fix_box_rotate_position
from yrocr.util.table_util import get_table_rows, auto_adjust_table_structure, cut_table_area, show_debug_image, lines_detect, \
    erase_image_bound_padding

# 需调整的角度阀值
MAX_ANGLE = 0.3
logger = get_logger(name='ocr_table')
DEBUG_FOLDER = 'debug'
if not os.path.exists(DEBUG_FOLDER):
    os.mkdir(DEBUG_FOLDER)


def ocr_table(img_path, drop_score=0.1, erase_bound_padding=30, verbose_log=False):
    """
    OCR表格识别(暂时支持90/190/270度旋转)
    :param img_path: 图片路径
    :param drop_score: 丢弃的置信度
    :param erase_bound_padding: 擦除的边界宽度
    :param verbose_log: 是否显示详细日志
    :return:
    """
    image = cv2.imread(img_path).copy()
    img_hei, img_width, deep = image.shape
    txt_result = invoke_ocr(image, drop_score)
    angle = get_rotate_angle(txt_result, False)
    if abs(angle) >= MAX_ANGLE:
        fix_box_rotate_position(img_width, img_hei, txt_result, angle)
        image = rotate(image, angle)
    else:
        logger.info(f"图片角度:{angle}无需校正")
    tables = extract_tables(image, erase_bound_padding, angle, verbose_log)
    adapt_table_cell_value(tables, txt_result, verbose_log)
    if verbose_log:
        show_ocr_table_result(image, txt_result, tables)
    return compose_table_and_txt_result(tables, txt_result)


def extract_tables(image, erase_bound_padding, angle, verbose_log=False):
    """
    抽取表格
    :param image: 图片路径
    :param erase_bound_padding: 擦除的边界
    :param verbose_log: 是否输出详细日志
    :return: 抽取到的表格列表
    """
    raw = image.copy()
    gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    # block_size 要分成的区域大小，奇数
    # C 每个区域计算出的阈值的基础上在减去这个常数作为这个区域的最终阈值
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -2)
    show_debug_image(f"{DEBUG_FOLDER}/1.二值化.jpg", binary, verbose_log)
    rows, cols = binary.shape
    if verbose_log:
        logger.info(f"图片宽度：{cols},高度{rows}")
    has_rotate = angle > MAX_ANGLE
    erase_image_bound_padding(binary, angle, has_rotate, erase_bound_padding)
    show_debug_image(f"{DEBUG_FOLDER}/2.二值化_边界修复.jpg", binary, verbose_log)

    # 重新再识别一下
    horizontal_lines, h_line_y_arr, h_line_x_arr, vertical_lines, v_line_y_arr, v_line_x_arr = lines_detect(binary, line_len=50, is_extend=True,
                                                                                                            extend_len=5)
    if len(horizontal_lines) == 0 or len(vertical_lines) == 0:
        return []
    show_debug_image(f"{DEBUG_FOLDER}/3.横线.jpg", horizontal_lines, verbose_log)
    show_debug_image(f"{DEBUG_FOLDER}/4.竖线.jpg", vertical_lines, verbose_log)
    # 标识表格
    table_skeleton = cv2.add(horizontal_lines, vertical_lines)
    show_debug_image(f"{DEBUG_FOLDER}/5.表格框架.jpg", table_skeleton, verbose_log)
    # 交点
    bitwise_and = cv2.bitwise_and(horizontal_lines, vertical_lines)
    show_debug_image(f"{DEBUG_FOLDER}/6.表格初步交点.jpg", bitwise_and, verbose_log)
    # 两张图片进行减法运算，去掉表格框线
    not_skeleton = cv2.subtract(binary, table_skeleton)
    show_debug_image(f"{DEBUG_FOLDER}/7.去掉表格框线.jpg", not_skeleton)

    src_tables = cut_table_area(cols, rows, h_line_x_arr, h_line_y_arr, v_line_x_arr, v_line_y_arr)
    if verbose_log:
        show_table_area(raw, src_tables, '8.原始表格区域.jpg')
    final_tables = []

    intersection_y_arr, intersection_x_arr = np.where(bitwise_and > 0)
    intersection_points = [
        (int(x), int(y)) for x, y in zip(intersection_x_arr, intersection_y_arr)
    ]
    h_points = [
        (int(x), int(y)) for x, y in zip(h_line_x_arr, h_line_y_arr)
    ]
    v_points = [
        (int(x), int(y)) for x, y in zip(v_line_x_arr, v_line_y_arr)
    ]

    # 表格框架点(方便调试)
    table_skeleton_image = np.zeros((rows, cols, 3), np.uint8)
    table_skeleton_image.fill(255)

    for index, table in enumerate(src_tables):
        logger.info(f"################################表格{index + 1}")
        # 过滤交点
        xmin = table['xmin'] - 5
        xmax = table['xmax'] + 5
        ymin = table['ymin'] - 5
        ymax = table['ymax'] + 5
        points = list(filter(lambda p: xmax > p[0] >= xmin and ymax > p[1] >= ymin, intersection_points))
        if len(points) == 0:
            continue
        rows, skeleton_points = get_table_rows(points, h_points, v_points, verbose_log)
        if len(rows) < 2:
            logger.warning("表格行数小于2行，废弃")
            continue
        final_table = {'position': {
            'xmin': table['xmin'],
            'xmax': table['xmax'],
            'ymin': table['ymin'],
            'ymax': table['ymax'],
        }, 'is_table': True, 'rows': rows}
        final_table = auto_adjust_table_structure(final_table)

        # 从表格的交点中，反向重新精确定位表格的位置，避免表格外的文字信息丢失
        xmins = []
        xmaxs = []
        ymins = []
        ymaxs = []
        for row in rows:
            for cell in row:
                points = cell['points']
                xmin = min(points[0][0], points[1][0], points[2][0], points[3][0])
                xmax = max(points[0][0], points[1][0], points[2][0], points[3][0])
                ymin = min(points[0][1], points[1][1], points[2][1], points[3][1])
                ymax = max(points[0][1], points[1][1], points[2][1], points[3][1])
                xmins.append(xmin)
                xmaxs.append(xmax)
                ymins.append(ymin)
                ymaxs.append(ymax)

        if len(xmins) > 0 and len(xmaxs) > 0 and len(ymins) > 0 and len(ymaxs) > 0:
            print(f"未修改前xmin：{table['xmin']};xmax：{table['xmax']};ymin：{table['ymin']};ymax：{table['ymax']}")
            final_table['position']['xmin'] = min(xmins)
            final_table['position']['xmax'] = max(xmaxs)
            final_table['position']['ymin'] = min(ymins)
            final_table['position']['ymax'] = max(ymaxs)
            print(
                f"修改后xmin：{final_table['position']['xmin']};xmax：{final_table['position']['xmax']};ymin：{final_table['position']['ymin']};ymax：{final_table['position']['ymax']}")
        final_tables.append(final_table)
        # 合并到新框架图中
        for point in skeleton_points:
            table_skeleton_image[point[1]][point[0]] = (0, 0, 255)
    show_debug_image(f"{DEBUG_FOLDER}/10.表格实际交点.jpg", table_skeleton_image, verbose_log)
    if verbose_log:
        show_table_area(raw, final_tables, '11.最终表格区域.jpg')
    return final_tables


def show_table_area(image, tables, debug_file_name):
    """
    显示表格区域
    :param image:
    :param tables:
    :return:
    """
    import numpy as np
    for index, table in enumerate(tables):
        xmin = table['xmin'] if 'xmin' in table else table['position']['xmin']
        xmax = table['xmax'] if 'xmax' in table else table['position']['xmax']
        ymin = table['ymin'] if 'ymin' in table else table['position']['ymin']
        ymax = table['ymax'] if 'ymax' in table else table['position']['ymax']
        box = [
            [xmin, ymin],
            [xmax, ymin],
            [xmax, ymax],
            [xmin, ymax]
        ]
        box = np.reshape(np.array(box), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True, (255, 0, 255), 1)
        image = draw_text(image, f"表格{index + 1}", xmin, ymin)
    cv2.imwrite(f"{DEBUG_FOLDER}/{debug_file_name}", image)


def adapt_table_cell_value(tables, ocr_result, verbose_log=False):
    """
    根据OCR文本识别结果匹配表格单元格的值
    设置表格单元格文本内容，并设置其匹配中所有块编号
    :param tables: 表格
    :param ocr_result: ocr识别结果
    :param verbose_log: 是否显示详细日志
    :return:
    """
    html = "<!DOCTYPE html> <html lang='en'> <head><meta charset='UTF-8'><title>抽取结果</title>  <style type='text/css'>\n" \
           "table{  " \
           "  padding: 5px; " \
           "  margin-top: 10px; }" \
           "table td{" \
           "    border: 1px solid #eee;" \
           "    padding: 20px;" \
           "}\n" \
           "</style></head ><body>"

    for index, table in enumerate(tables):
        row_index = 1
        match_block_ids = []
        table_text = "\n<table cellpadding='0' cellspacing='0'>\n"
        for row in table['rows']:
            # logger.info(f"####正在匹配第【{row_index}】行单元格=======")
            table_text += ' <tr>\n'
            for cell in row:
                colspan = cell['colspan']
                rowspan = cell['rowspan']
                vmerge = cell['vmerge']
                if vmerge:
                    continue
                cell['text'], sub_block_ids = find_cell_text(cell['position'], ocr_result)
                match_block_ids = match_block_ids + sub_block_ids
                cell_text = cell['text'] if len(cell['text']) > 0 else 'null'
                table_text += f"    <td colspan='{colspan}' rowspan='{rowspan}' vmerge={vmerge}>{cell_text}</td>\n"
                cell['block_ids'] = sub_block_ids
            table_text += ' </tr>\n'
            row_index += 1
        table_text += '</table>\n'
        # 设置该表格关联的块ID
        table['block_ids'] = match_block_ids
        if verbose_log:
            # logger.info(f"################打印表格:[{index + 1}]识别结果########################")
            # logger.info(table_text)
            html += f"\n\n\n表格{index + 1}\n\n\n"
            html += table_text
            # logger.info(f"################打印结束########################")

    html += '</body> </html>'
    if verbose_log:
        with open(f'{DEBUG_FOLDER}/result.html', "w") as fp:
            fp.write(html)


def compose_table_and_txt_result(tables, ocr_result):
    """
    根据表格及OCR纯文本识别结果，组装最终结果
    :param tables: 表格列表
    :param ocr_result: 文本识别结果
    :return:
    """
    if len(tables) == 0:
        return [
            {
                'is_table': False,
                'blocks': ocr_result
            }
        ]

    table_blocks_ids = []
    for table in tables:
        table_blocks_ids = table_blocks_ids + table['block_ids']
    # 游离的块
    free_blocks = list(filter(lambda item: item['block_id'] not in table_blocks_ids, ocr_result))
    # 所有表格最前面的块
    first_free_blocks = find_blocks_before_table(free_blocks, tables[0])
    # 所有表格最后面的块
    last_free_blocks = find_blocks_after_table(free_blocks, tables[len(tables) - 1])
    # 剩余的游离块
    free_blocks = filter_free_blocks(free_blocks, first_free_blocks, last_free_blocks)

    # 构建最终返回数据（每个表格都要有前后的块）
    final_result = [
        {
            'is_table': False,
            'blocks': first_free_blocks
        }
    ]

    for index, table in enumerate(tables):
        final_result.append(table)
        if index < len(tables) - 1:
            # 中间的表格才需处理：取当前表格的所有后面元素，以及下一个表格的前面元素的并集
            after_table_blocks = find_blocks_after_table(free_blocks, tables[index])
            before_table_blocks = find_blocks_before_table(free_blocks, tables[index + 1])
            blocks = union_blocks(after_table_blocks, before_table_blocks)
            final_result.append(
                {
                    'is_table': False,
                    'blocks': blocks
                }
            )

    final_result.append(
        {
            'is_table': False,
            'blocks': last_free_blocks
        })
    return final_result


def union_blocks(blocks1, blocks2):
    """
    取两个块集合的交集
    :param block1:
    :param block2:
    :return:
    """
    ids1 = [block['block_id'] for block in blocks1]
    ids2 = [block['block_id'] for block in blocks2]
    ids = list(set(ids1).intersection(set(ids2)))
    return [block for block in blocks1 if block['block_id'] in ids]


def filter_free_blocks(free_blocks, first_free_blocks, last_free_blocks):
    """
    过滤掉已经被使用的游离块
    :param free_blocks:
    :param first_free_blocks:
    :param last_free_blocks:
    :return:
    """
    first_ids = [item['block_id'] for item in first_free_blocks]
    last_ids = [item['block_id'] for item in last_free_blocks]
    use_ids = first_ids + last_ids
    free_blocks = filter(lambda block: block['block_id'] not in use_ids, free_blocks)
    return list(free_blocks)


def find_blocks_before_table(blocks, table):
    """
    查找在指定表格之前的块
    此处有两种情况
    情况1：表格占了整行的情况，块的ymax坐标比表格的ymin小即可。
    情况2：表格只占了部分行。块的ymax坐标小于表格ymax，且块的xmax比表格的xmin小
    :param blocks:
    :param table:
    :return:
    """
    table_xmin = table['position']['xmin']
    table_ymin = table['position']['ymin']
    table_ymax = table['position']['ymax']
    ret_blocks = []
    for block in blocks:
        rect = get_ocr_point_rect(block['position'])
        xmax = rect['left'] + rect['width']
        ymax = rect['top'] + rect['height']
        if ymax < table_ymin:
            ret_blocks.append(block)
        elif ymax < table_ymax and xmax < table_xmin:
            ret_blocks.append(block)
    return ret_blocks


def find_blocks_after_table(blocks, table):
    """
    查找在表格之后的块
    此处有两种情况
    情况1：表格占了整行的情况，块的ymin大于表格ymax即可
    情况2：表格只占了部分行，块的ymin大于表格ymin，且块的xmin大于表格的xmax
    :param blocks:
    :param table:
    :return:
    """
    table_xmax = table['position']['xmax']
    table_ymin = table['position']['ymin']
    table_ymax = table['position']['ymax']
    ret_blocks = []
    for block in blocks:
        rect = get_ocr_point_rect(block['position'])
        xmin = rect['left']
        ymin = rect['top']
        if ymin > table_ymax:
            ret_blocks.append(block)
        elif ymin > table_ymin and xmin > table_xmax:
            ret_blocks.append(block)
    return ret_blocks


def find_cell_text(cell_rect, result):
    cell_text = ''
    block_ids = []
    for item in result:
        fonts_rect = get_ocr_point_rect(item['position'])
        is_match = judge_cell_match_fonts(cell_rect, fonts_rect, item['text'])
        if is_match:
            cell_text += item['text']
            block_ids.append(item['block_id'])
    return cell_text, block_ids


def judge_cell_match_fonts(cell_rect, fonts_rect, text, min_cover_rate=0.5):
    """
    判断单元格是否覆盖指定的文字，原则上，单元格会完整包含整个OCR识别的文字区域
    :param cell_rect:  单元格区域矩形{
        "left": xmin,
        "top": ymin,
        "width": width,
        "height": hei
    }
    :param fonts_rect: 抽取的字体矩形{
        "left": xmin,
        "top": ymin,
        "width": width,
        "height": hei
    }
    :param min_cover_rate: 最小覆盖度
    :return:
    """
    p1_x = cell_rect['left']
    p1_y = cell_rect['top']
    p2_x = p1_x + cell_rect['width']
    p2_y = p1_y + cell_rect['height']
    p3_x = fonts_rect['left']
    p3_y = fonts_rect['top']
    p4_x = p3_x + fonts_rect['width']
    p4_y = p3_y + fonts_rect['height']

    if p1_x > p4_x or p2_x < p3_x or p1_y > p4_y or p2_y < p3_y:
        return False
    width = min(p2_x, p4_x) - max(p1_x, p3_x)
    height = min(p2_y, p4_y) - max(p1_y, p3_y)
    cover_area = width * height
    fonts_area = fonts_rect['width'] * fonts_rect['height']
    score = cover_area / fonts_area
    if score > 0:
        logger.info(f'####单元格覆盖字体【{text}】比例:{score}')
    return score >= min_cover_rate


def show_ocr_table_result(image, result, tables):
    """
    显示OCR、表格结构抽取的结果
    :param image: 图片路径
    :param result: 纯文本识别结果
    :param table: 表格
    :return:
    """
    import numpy as np
    for item in result:
        position = item['position']
        xmin = min(position[0][0], position[1][0], position[2][0], position[3][0])
        ymax = max(position[0][1], position[1][1], position[2][1], position[3][1])
        box = [
            [position[0][0], position[0][1]],
            [position[1][0], position[1][1]],
            [position[2][0], position[2][1]],
            [position[3][0], position[3][1]]
        ]
        box = np.reshape(np.array(box), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True, (255, 0, 255), 1)
        text = item['text'] + '(' + item['score'] + ')'
        image = draw_text(image, text, xmin, ymax)

    # 加上单元格识别结果
    for table in tables:
        for row in table['rows']:
            for cell in row:
                box = cell['position']
                xmin = round(box['left'])
                ymin = round(box['top'])
                xmax = round(xmin + box['width'])
                ymax = round(ymin + box['height'])
                box = [
                    [xmin, ymin],
                    [xmax, ymin],
                    [xmax, ymax],
                    [xmin, ymax]
                ]
                box = np.reshape(np.array(box), [-1, 1, 2]).astype(np.int64)
                image = cv2.polylines(np.array(image), [box], True, (255, 127, 127), 2)
    cv_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(f'{DEBUG_FOLDER}/ocr_table_result.jpg', cv_img)


def re_combile_table_cell(img_path, table):
    """
    重新将单元格拆分并打乱，并重新合成带padding的新图片，确保不会被纯文本组件识别错乱掉
    :param table:
    :return:
    """
    padding_width = 100
    padding_height = 10

    table_height = table['position']['ymax'] - table['position']['ymin']
    table_width = table['position']['xmax'] - table['position']['xmin']
    all_height = table_height + len(table['rows']) * padding_height + 20
    all_width = table_width + len(table['rows'][0]) * padding_width + 20
    final_matrix = np.zeros((all_height, all_width, 3), np.uint8)
    final_matrix.fill(255)
    start_row = 20
    start_col = 20

    src_img = cv2.imread(img_path).copy()
    gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -2)
    horizontal_lines, h_line_y_arr, h_line_x_arr, vertical_lines, v_line_y_arr, v_line_x_arr = lines_detect(binary,
                                                                                                            line_len=22,
                                                                                                            is_extend=True)
    h_points = [
        (int(x), int(y)) for x, y in zip(h_line_x_arr, h_line_y_arr)
    ]
    v_points = [
        (int(x), int(y)) for x, y in zip(v_line_x_arr, v_line_y_arr)
    ]
    # 设置这些点的颜色为255
    for point in h_points:
        src_img[point[1]][point[0]] = (255, 255, 255)
    for point in v_points:
        src_img[point[1]][point[0]] = (255, 255, 255)

    for row in table['rows']:
        print("##开始复制行")
        for cell in row:
            # 得到单元格的完整像素
            left = cell['position']['left']
            top = cell['position']['top']
            width = cell['position']['width']
            height = cell['position']['height']
            end_col = start_col + width
            end_row = start_row + height
            print(f'col:{start_col}-{end_col}.row:{start_row}-{end_row}')
            final_matrix[start_row:end_row, start_col:end_col] = src_img[top:top + height, left:left + width]
            start_col = end_col + padding_width
        start_row = end_row + padding_height
        start_col = 20

    cv2.imwrite(f'{DEBUG_FOLDER}/合成图.jpg', final_matrix)
    result = invoke_ocr(f'{DEBUG_FOLDER}/合成图.jpg', drop_score=0.2)
    print("#######打印结果")
    for block in result:
        print(block)


if __name__ == '__main__':
    # TODO 验证90度 倾斜ocr返回的规律，看下

    # TODO 做到，测试之前业务单元使用的数据
    # 文件1
    # img_path = "/Users/chenjianghai/job/YR/2021/OCR自研/公司内部测试数据/2.表格抽取/1.基础测试用例.jpg"
    # 文件2
    # img_path = '/Users/chenjianghai/job/YR/2021/OCR自研/公司内部测试数据/2.表格抽取/2.任务书.jpg'
    # 文件3
    # img_path = '/Users/chenjianghai/job/YR/2021/OCR自研/公司内部测试数据/2.表格抽取/3.项目支付计划.jpg'
    # 文件4
    # img_path = '/Users/chenjianghai/job/YR/2021/OCR自研/公司内部测试数据/2.表格抽取/4.计划任务书.jpg'
    img_path = '/Users/chenjianghai/job/YR/2021/OCR/公司内部测试数据/2.表格抽取/7.四川大学项目审计报告_4.jpg'
    result = ocr_table(img_path, verbose_log=True, erase_bound_padding=0, drop_score=0.1)
    print(result)
