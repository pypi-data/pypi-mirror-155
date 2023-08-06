#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 表格辅助工具
import cv2
import numpy as np
from paddleocr.ppocr.utils.logging import get_logger

from yrocr.util.cvutil import get_position_after_rotate

logger = get_logger(name='ocr_table')

X_DISTANCE = 10
Y_DISTANCE = 10
DISTANCE = X_DISTANCE * Y_DISTANCE


def erase_image_bound_padding(binary, angle, has_rotate, padding=30):
    """
    擦除二进制图片边界（印刷体的边界经常有黑边，毛边）
    :param binary: 二值化图片
    :param padding: 空白
    :return:
    """
    if padding == 0:
        return
    points = []
    rows, cols = binary.shape
    for col_index in range(cols):
        for row_index in range(padding):
            # 上面N行
            # binary[row_index][col_index] = 0
            # 下面N行
            # binary[rows - 1 - row_index][col_index] = 0

            points.append([row_index, col_index])
            points.append([rows - 1 - row_index, col_index])

    for row_index in range(rows):
        for col_index in range(padding):
            # 左边10行
            # binary[row_index][col_index] = 0
            # 右边10行
            # binary[row_index][cols - 1 - col_index] = 0

            points.append([row_index, col_index])
            points.append([row_index, cols - 1 - col_index])

    # 旋转的点，需得到旋转后的坐标
    if has_rotate:
        for index, point in enumerate(points):
            new_point = get_position_after_rotate(point[0], point[1], cols / 2, rows / 2, angle)
            points[index] = new_point
    for point in points:
        if 0 <= point[0] < rows and 0 <= point[1] < col_index:
            binary[point[0]][point[1]] = 0


def lines_detect(binary_img, line_len=22, is_extend=True, extend_len=3):
    """
    横线/竖线推断
    :param binary_img: 二值化图片
    :param line_len: 线条长度
    :param is_extend: 是否延伸线条
    :param extend_len: 延伸长度
    :return: 横线/竖线 X/Y数组
    """
    horizontal_lines = discover_line_obj(binary_img, min_line_len=line_len, type='horizontal_lines')
    h_line_y_arr, h_line_x_arr = np.where(horizontal_lines > 0)
    if len(h_line_y_arr) == 0 or len(h_line_x_arr) == 0:
        return [], [], [], [], [], []

    rows, cols = binary_img.shape
    if is_extend:
        ex_points = extend_horizontal_lines(h_line_x_arr, h_line_y_arr, extend_len)
        for point in ex_points:
            if point[1] < rows and point[0] < cols:
                horizontal_lines[point[1]][point[0]] = 255
    vertical_lines = discover_line_obj(binary_img, min_line_len=line_len, type='vertical_lines')
    v_line_y_arr, v_line_x_arr = np.where(vertical_lines > 0)
    if len(v_line_y_arr) == 0 or len(v_line_x_arr) == 0:
        return [], [], [], [], [], []
    if is_extend:
        ex_points = extend_vertical_lines(v_line_x_arr, v_line_y_arr, extend_len)
        for point in ex_points:
            if point[1] < rows and point[0] < cols:
                vertical_lines[point[1]][point[0]] = 255
    return horizontal_lines, h_line_y_arr, h_line_x_arr, vertical_lines, v_line_y_arr, v_line_x_arr


def discover_line_obj(img, width=1, min_line_len=22, type='horizontal_lines'):
    """
    从图片中检测线条装物体
    :param img: cv2图对象
    :param width: 线条粗，如1或3
    :param min_line_len: 最小长度
    :param type: 类型；水平线条 horizontal_lines/垂直线 vertical_lines
    :return:
    """
    kernel_struct = (min_line_len, width) if type == 'horizontal_lines' else (width, min_line_len)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_struct)
    eroded = cv2.erode(img, kernel, iterations=1)
    return cv2.dilate(eroded, kernel, iterations=1)


def cut_table_area(width, height, h_line_x_arr, h_line_y_arr, v_line_x_arr, v_line_y_arr):
    """
    切割表格区域
    得到Y轴上的阶段连续空间
    得到Y连续空间上的X轴阶段连续空间
    得到每个表格的精确区域
    :param width: 图片宽度
    :param height: 图片高度
    param h_line_x_arr: 横线X数组
    param h_line_y_arr: 横线Y数组
    :param v_line_x_arr: 竖线X数组
    :param v_line_y_arr: 竖线Y数组
    :return:
    """
    h_points = [
        (int(x), int(y)) for x, y in zip(h_line_x_arr, h_line_y_arr)
    ]
    v_points = [
        (int(x), int(y)) for x, y in zip(v_line_x_arr, v_line_y_arr)
    ]

    # Y轴空间
    full_page_y_dict = {}
    for index in range(height):
        value = 1 if index in v_line_y_arr else 0
        full_page_y_dict[index] = value

    tables = []
    is_table_start = False
    start_pos = 0
    # 得到有竖线的连续空间，每个连续空间，即为表格的Y轴上下限
    for index in range(height):
        if is_table_start:
            # 线条有可能一直持续到最后一个像素点
            if full_page_y_dict[index] == 0 or index == height - 1:
                # print(f"Y轴结束,结束高度：{index}")
                tables.append({
                    # 横线点
                    'h_points': list(filter(lambda point: index > point[1] >= start_pos, h_points)),
                    'ymin': start_pos,
                    'ymax': index,
                    'height': index - start_pos,
                    # 竖线点
                    'v_points': list(filter(lambda point: index > point[1] >= start_pos, v_points))

                })
                start_pos = 0
                is_table_start = False
        else:
            if full_page_y_dict[index] == 1:
                # print(f"Y轴开始,起始高度：{index}")
                start_pos = index
                is_table_start = True

    # 最终表格
    final_tables = []
    # 每个表格区域，再按照X轴划分，得到表格的准确区域
    for table in tables:
        # 这个区域如果没有竖线，则X轴无需再切分
        if len(table['v_points']) == 0:
            continue
        full_page_x_dict = {}
        x_arr = [point[0] for point in table['h_points']]
        for index in range(width):
            value = 1 if index in x_arr else 0
            full_page_x_dict[index] = value
        # 得到有横线的连续空间，每个连续空间，即为表格的X轴上下限
        start_x = 0
        is_x_start = False
        for index in range(width):
            if is_x_start:
                # 线条有可能一直持续到最后一个像素点
                if full_page_x_dict[index] == 0 or index == width - 1:
                    # print(f"X轴结束,结束宽度：{index}")
                    # 宽度限制，避免图片质量太差引起的识别异常（横线竖线的点不连续的时候容易出现这个问题）。
                    if index - start_pos > DISTANCE:
                        # 表格最小要求
                        cur_h_points = list(filter(lambda point: index > point[0] >= start_x, table['h_points']))
                        cur_v_points = list(filter(lambda point: index > point[0] >= start_x, table['v_points']))
                        cur_width = index - start_x
                        if len(cur_h_points) >= 4 and len(cur_v_points) >= 4 and cur_width >= 40 and table[
                            'height'] >= 40:
                            final_tables.append({
                                'xmin': start_x,
                                'xmax': index,
                                'width': index - start_x,
                                'h_points': list(filter(lambda point: index > point[0] >= start_x, table['h_points'])),
                                'ymin': table['ymin'],
                                'ymax': table['ymax'],
                                'height': table['height'],
                                'v_points': list(filter(lambda point: index > point[0] >= start_x, table['v_points']))
                            })
                    start_x = 0
                    is_x_start = False


            else:
                if full_page_x_dict[index] == 1:
                    # print(f"X轴开始,起始宽度：{index}")
                    start_x = index
                    is_x_start = True


    return final_tables


def get_table_rows(points, h_points, v_points, verbose_log=False):
    """
    从横线/竖线相交的点集合中，推断出当前表格的结构，并返回行列表，及使用到的表格交点
    目前已支持列合并的情况，暂不支持行合并的情况
    行列合并的情况说明：
    正常情况：一个单元格应满足：存在point1、point2、point3、point4四个点；且point2与point4要连续；与point4要连续
    列合并情况：point3、point4存在，但是point2/point4不连续（即：单元格右侧没闭合）
    行合并情况：1： point3不存在（行合并发在最左侧的情况） 2： point4不存在（行合并发在最右侧的情况）
    2：point3、point4存在，但是两个点之间不连续（行合并发生在中间）；
    存在问题:
    :param points: 该表格交点
    :param h_points: 整个页面横线点集合
    :param v_points: 整个页面竖线点集合
    :param verbose_log: 详细日志
    :return:
    """
    # 框架点
    skeleton_points = get_alone_points(points)
    # useful_x_arr = get_alone_num([point[0] for point in points])
    useful_y_arr = get_alone_num([point[1] for point in skeleton_points])
    # 将点按行分开
    point_y_dict = {}
    for point in skeleton_points:
        y = judge_num_belongs(useful_y_arr, point[1])
        y_list = point_y_dict[y] if y in point_y_dict else []
        y_list.append(point)
        point_y_dict[y] = y_list
    # 得到最终从上到下，从左到右的点集合
    row_point_objs = []
    for y in point_y_dict:
        row_point_objs.append([y, sort_points_by_x_asc(point_y_dict[y])])
    row_point_objs = sort_row_point_objs(row_point_objs)
    # 绘制单元格
    rows = []
    for row_index in range(len(row_point_objs) - 1):
        row = [
        ]
        y, points = row_point_objs[row_index]
        # 因为列合并而跳过的单元格索引
        skip_colspan_cell_dict = {}
        for cell_index in range(len(points) - 1):
            if cell_index in skip_colspan_cell_dict:
                continue

            point1 = points[cell_index]
            point2 = points[cell_index + 1]
            next_y, next_points = row_point_objs[row_index + 1]
            point3, continuous_13 = match_next_point_by_position(point1[0], point1[1], next_points, v_points)
            point4, continuous_24 = match_next_point_by_position(point2[0], point2[1], next_points, v_points)
            continuous_12 = is_continuous_horizontal_lines(point1, point2, h_points)
            continuous_34 = is_continuous_horizontal_lines(point3, point4, h_points) if point3 and point4 else False
            # 正常情况，存在点，且各个点之间有连续的连线
            # 行合并跟列合并的情况有时候难以区分
            # if row_index == 1 and cell_index == 1:
            #     print("进去调试")
            if point3 and point4 and continuous_13 and continuous_24 and continuous_12 and continuous_34:
                if verbose_log:
                    logger.info(f"正常单元格,位置:{row_index}:{cell_index}.坐标{point1}{point2}")
                cell_obj = get_cell_obj(point1, point2, point3, point4)
                row.append(cell_obj)
            elif not continuous_12:
                # point1 跟point2 无连线，则证明该单元格是是被列合并的单元格，无需处理，往下走接口
                if verbose_log:
                    logger.info(f"行合并被跳过的单元格,位置:{row_index}:{cell_index}")
                continue
            elif point3 and point4 and not continuous_24:
                colspan = add_colspan_cell(row, point1, cell_index, points, next_points, v_points, skip_colspan_cell_dict)
                if verbose_log:
                    logger.info(f"列合并单元格,位置:{row_index}:{cell_index}.colspan:{colspan}")
            elif not point3 or (point3 and point4 and not continuous_34):
                # 行合并
                rowspan = add_rowspan_cell(row, point1, point2, row_index, row_point_objs, h_points, v_points)
                if verbose_log:
                    logger.info(f"行合并单元格,位置:{row_index}:{cell_index}.rowspan:{rowspan}")

            elif not point4:
                # point4没有的情况，大概率是行合并；但也有复杂情况下是列合并（列合并的下一行也是列合并，造成原本应该存在的point4不存在）
                if verbose_log:
                    logger.info(f"point4不存在,判断是行合并还是列合并,位置:{row_index}:{cell_index}")
                # 采用point3的X坐标，point2的Y坐标
                # 此处 point3也有可能不存在（极小概率：当本行又出现复杂当行合并列合并时，则直接把本单元格当成普通的单元格）
                fake_point4 = (point2[0], point3[1])
                # 判断p3 p4之间是否有连线，如果有则为列合并，否则为行合并
                continuous_34 = is_continuous_horizontal_lines(point3, fake_point4, h_points)
                if continuous_34:
                    colspan = add_colspan_cell(row, point1, cell_index, points, next_points, v_points, skip_colspan_cell_dict)
                    if verbose_log:
                        logger.info(f"该单元格为列合并单元格.colspan:{colspan}")
                else:
                    rowspan = add_rowspan_cell(row, point1, point2, row_index, row_point_objs, h_points, v_points)
                    if verbose_log:
                        logger.info(f"该单元格为行合并单元格.rowspan:{rowspan}")

            elif not continuous_12:
                # point1 跟point2 无连线，则证明该单元格是是被列合并的单元格，无需处理，往下走接口
                if verbose_log:
                    logger.info(f"行合并被跳过的单元格,位置:{row_index}:{cell_index}")
                continue

            else:
                summary = f'未知情况,位置:{row_index}:{cell_index}'
                if point3:
                    summary += f'point3 exits;'
                if point4:
                    summary += f'point4 exits;'
                logger.info(
                    f"{summary};continuous_12:{continuous_12};continuous_13:{continuous_13};continuous_24:{continuous_24};continuous_34:{continuous_34}")

        rows.append(row)
    return rows, skeleton_points


def add_colspan_cell(row, point1, cell_index, points, next_points, v_points, skip_colspan_cell_dict):
    """
    添加列合并单元格
    :param row: 行对象
    :param point1: point1
    :param cell_index: 当前单元格索引
    :param points: 当前行的所有点集合
    :param next_points: 下一行的点集合
    :param v_points: 当前页面所有竖点集合
    :param skip_colspan_cell_dict: 跳过的单元格dict
    :return:
    """
    skip_colspan_cell_dict[cell_index + 1] = cell_index + 1
    # 这边的colspan不一定准，因为如果上一行也是行合并的情况，本行的points数会减少，导致colspan会偏少
    colspan = 1
    # 列合并，这个时候point1不变，point2索引+1，继续找。找到后。下一个迭代的cell_index要直接跳到该截止的索引，否则会造成重复找
    for point2_index in range(cell_index + 2, len(points)):
        point2 = points[point2_index]
        point3, continuous_13 = match_next_point_by_position(point1[0], point1[1], next_points, v_points)
        point4, continuous_24 = match_next_point_by_position(point2[0], point2[1], next_points, v_points)
        colspan += 1
        if point3 and point4 and continuous_24:
            logger.info(f"单元格colspan:{colspan}")
            cell_obj = get_cell_obj(point1, point2, point3, point4, colspan=colspan)
            row.append(cell_obj)
            break
        else:
            skip_colspan_cell_dict[point2_index] = point2_index
    return colspan


def add_rowspan_cell(row, point1, point2, row_index, row_point_objs, h_points, v_points):
    """
    添加行合并单元格
    :param row: 行对象
    :param point1: point1
    :param point2: point2
    :param row_index: 行索引
    :param row_point_objs: 行点对象map
    :param h_points: 当前页面所有水平点集合
    :param v_points: 当前页面所有竖点集合
    :return:
    """
    rowspan = 2
    for start_row_index in range(row_index + 2, len(row_point_objs)):
        next_y, next_points = row_point_objs[start_row_index]
        point3, continuous_13 = match_next_point_by_position(point1[0], point1[1], next_points, v_points)
        point4, continuous_24 = match_next_point_by_position(point2[0], point2[1], next_points, v_points)
        continuous_34 = is_continuous_horizontal_lines(point3, point4, h_points) if point3 and point4 else False
        if point3 and point4 and continuous_34:
            cell_obj = get_cell_obj(point1, point2, point3, point4, colspan=1, rowspan=rowspan)
            row.append(cell_obj)
            break
        else:
            rowspan += 1
    return rowspan


def get_cell_obj(point1, point2, point3, point4, colspan=1, rowspan=1, vmerge=False):
    return {
        'rowspan': rowspan,
        'colspan': colspan,
        'vmerge': vmerge,
        # position没办法处理角度倾斜的倾斜，目前position跟points都先返回
        'position': {
            "left": int(point1[0]),
            "top": int(point1[1]),
            "width": int(point2[0] - point1[0]),
            "height": int(point3[1] - point1[1]),
        },
        'points': [point1, point2, point3, point4]
    }


def auto_adjust_table_structure(table):
    """
    自动调整表格结构（原始rowspan是准的,colspan会因为前面有行合并的情况不准）
    :param table:
    :return:
    """
    # 判断列合并
    set_table_colspan(table)
    return table


def set_table_colspan(table):
    # 将被行合并的单元格还原出，并标记为vmerge（否则，列合并会失误）
    # 记录有行合并的单元格
    rowspan_cells = []
    for row_index, row in enumerate(table['rows']):
        for col_index, cell in enumerate(row):
            if cell['rowspan'] > 1:
                rowspan_cells.append({
                    'rowspan': cell['rowspan'],
                    'row_index': row_index,
                    'col_index': col_index,
                    'left': cell['position']['left'],
                    'right': cell['position']['left'] + cell['position']['width']
                })

    # 补齐因行合并带来的单元格缺失
    rows = table['rows']
    for cell in rowspan_cells:
        start = cell['row_index'] + 1
        end = cell['row_index'] + cell['rowspan']
        for index in range(start, end):
            row = rows[index]
            add_index = judage_vmerge_cell_index(row, cell['left'], cell['right'])
            cell_obj = get_cell_obj([0, 0], [0, 0], [0, 0], [0, 0], 1, 1, True)
            row.insert(add_index, cell_obj)

    for row_index, row in enumerate(table['rows']):
        # logger.info(f'##########计算第{row_index}列合并情况')
        # 当前单元格前面已有的单元格数量（colspan大于1的算多个单元格）
        pre_cells_num = 0
        for cell_index, cell in enumerate(row):
            if cell['vmerge']:
                pre_cells_num += 1
                continue
            colspan = caculate_colspan(table, cell, row_index, pre_cells_num)
            cell['colspan'] = colspan
            # logger.info(f'第{cell_index}列合并：{colspan}')
            pre_cells_num += colspan

    # TODO 重新移除vmerge的单元格（等都调试好了再来做）
    rows = []
    for row in table['rows']:
        row = list(filter(lambda cell: not cell['vmerge'], row))
        rows.append(row)
    table['rows'] = rows


def judage_vmerge_cell_index(row, left, right):
    """
    判断因行合并而额外添加的单元格应该添加的位置
    :param row: 行
    :param left: 坐标坐标
    :param right: 右边坐标
    :return:
    """
    for index, cell in enumerate(row):
        left_dis = abs(cell['position']['left'] - right)
        if left_dis < X_DISTANCE:
            return index
        cell_right = cell['position']['left'] + cell['position']['width']
        right_dis = abs(cell_right - left)
        if right_dis < X_DISTANCE:
            return index + 1
        if index == len(row) - 1 and cell_right < left:
            return len(row)
    return 0


def caculate_colspan(table, target_cell, target_row_index, pre_cells_num):
    """
    计算指定单元格的列合并数量
    :param table: 表格
    :param target_cell: 待计算的单元格
    :param target_row_index: 待计算的单元格的行索引
    :param pre_cells_num: 当前单元格前面已有的单元格数量（colspan大于1的算多个单元格）
    :return:
    """
    target_right = target_cell['position']['left'] + target_cell['position']['width']
    # 该表格中：与目标单元格右侧一样的其他单元格最大的列索引号
    max_col_index = 0
    for index, row in enumerate(table['rows']):
        if target_row_index == index:
            continue
        for cell_index, cell in enumerate(row):
            cell_right = cell['position']['left'] + cell['position']['width']
            if not almost_equals(cell_right, target_right):
                continue
            # 计算前面有多少单元格
            prefix_cell_size = caculate_prefix_cell_size(row, cell_index)
            if max_col_index < prefix_cell_size:
                max_col_index = prefix_cell_size
    max_col_index = max_col_index - pre_cells_num + 1
    if max_col_index <= 0:
        max_col_index = 1
    return max_col_index


def caculate_prefix_cell_size(row, stop_index):
    """
    判断某行中，指定索引序号的单元格前面实际有多少单元格（colspan计入）
    :param row:
    :param stop_index:
    :return:
    """
    total = 0
    for index in range(stop_index):
        cell = row[index]
        total += cell['colspan']
    return total


def almost_equals(num1, num2):
    return abs(num1 - num2) < X_DISTANCE


def match_next_point_by_position(x, y, next_points, v_points):
    """
    根据当前点的坐标匹配下一行中的点,及两点之间是否连续
    :param x: X值
    :param x: Y值
    :param next_points: 下一行点集合
    :param h_points: 整个页面横线点集合
    :param v_points: 整个页面竖线点集合
    :return:
    """
    match_point = next_points[0]
    distance = abs(x - next_points[0][0])
    for point in next_points:
        cur_dis = abs(point[0] - x)
        if cur_dis < distance:
            distance = cur_dis
            match_point = point
    if distance >= X_DISTANCE:
        return None, False
    # 判断两个点之间是否有连续的竖线
    line_points = list(filter(lambda p: abs(p[0] - x) < X_DISTANCE and y <= p[1] <= match_point[1], v_points))
    # 理论上一个像素一个点
    target_line_points = abs(match_point[1] - y) / 2
    # 至少要有一半的点，否则直接不连续
    if len(line_points) <= target_line_points:
        return match_point, False
    # 按照Y轴升序
    line_points = sort_points_by_y_asc(line_points)
    is_continuous = True
    for index in range(len(line_points) - 1):
        p1 = line_points[index]
        p2 = line_points[index + 1]
        if p2[1] - p1[1] > Y_DISTANCE:
            is_continuous = False
            break
    return match_point, is_continuous


def is_continuous_horizontal_lines(point1, point2, h_points):
    """
    判断两点之间是否是连续是连续的水平线（横线）
    :param point1:
    :param point2:
    :param h_points:
    :return:
    """
    y = point1[1]
    # Y轴一样，x轴在point1, point2之间
    line_points = list(filter(lambda p: abs(p[1] - y) < Y_DISTANCE and point1[0] <= p[0] <= point2[0], h_points))
    line_points = sort_points_by_x_asc(line_points)
    # 理论上一个像素一个点
    target_line_points = abs(point2[0] - point1[0]) / 2
    # 至少要有一半的点，否则直接不连续
    if len(line_points) <= target_line_points:
        return False
    is_continuous = True
    for index in range(len(line_points) - 1):
        p1 = line_points[index]
        p2 = line_points[index + 1]
        if p2[0] - p1[0] > X_DISTANCE:
            is_continuous = False
            break
    return is_continuous


def sort_row_point_objs(row_point_objs):
    """
    按照Y轴升序
    :param row_point_objs:
    :return:
    """
    import functools
    def compare(obj1, obj2):
        if obj2[0] < obj1[0]:
            return 1
        elif obj1[0] < obj2[0]:
            return -1
        else:
            return 0

    return sorted(row_point_objs, key=functools.cmp_to_key(compare))


def extend_horizontal_lines(horizontal_x_arr, horizontal_y_arr, extend_len=10):
    """
    延长横线，避免表格的交点丢失
    :param dilated_ys: X坐标
    :param dilated_xs: Y坐标
    :param extend_len: 延伸的长度
    :return:
    """

    points = [
        [int(x), int(y)] for x, y in zip(horizontal_x_arr, horizontal_y_arr)
    ]
    # 每个Y轴拥有的x坐标列表
    y_x_dict = {

    }
    # 按Y轴分组
    y_group_arr = np.sort(get_alone_num(horizontal_y_arr))
    for point in points:
        # 判断归属于哪个Y
        y = judge_num_belongs(y_group_arr, point[1])
        x_list = y_x_dict[y] if y in y_x_dict else []
        x_list.append(point[0])
        y_x_dict[y] = x_list

    extend_points = []
    for y in y_x_dict:
        x_list = np.sort(y_x_dict[y])
        lines = split_lines_from_nums(x_list)
        for line in lines:
            for index in range(extend_len):
                extend_points.append([line[0] - index, y])
                extend_points.append([line[0] + index, y])
                extend_points.append([line[len(line) - 1] - index, y])
                extend_points.append([line[len(line) - 1] + index, y])

    return extend_points


def extend_vertical_lines(vertical_x_arr, vertical_y_arr, extend_len=10):
    """
    延长竖线，避免表格的交点丢失
    :param dilated_ys: X坐标
    :param dilated_xs: Y坐标
    :param extend_len: 延伸的长度
    :return:
    """

    points = [
        [int(x), int(y)] for x, y in zip(vertical_x_arr, vertical_y_arr)
    ]
    # 每个x轴拥有的y坐标列表
    x_y_dict = {

    }
    # 按X轴分组
    x_group_arr = np.sort(get_alone_num(vertical_x_arr))
    for point in points:
        # 判断归属于哪个X
        x = judge_num_belongs(x_group_arr, point[0])
        y_list = x_y_dict[x] if x in x_y_dict else []
        y_list.append(point[1])
        x_y_dict[x] = y_list

    extend_points = []
    for x in x_y_dict:
        y_list = np.sort(x_y_dict[x])
        # 如果有上下两张表格中的竖线x值一样，则这些竖线会被识别为同一条竖线；这时，需要分辨出y值里到底有多少条线条，从而延长每一个线条
        lines = split_lines_from_nums(y_list)
        for line in lines:
            for index in range(extend_len):
                extend_points.append([x, line[0] - index])
                extend_points.append([x, line[0] + index])
                extend_points.append([x, line[len(line) - 1] - index])
                extend_points.append([x, line[len(line) - 1] + index])

    return extend_points


def split_lines_from_nums(nums):
    """
    从给定的一段数字中，识别并切割出连线的线条,并设置(间隔小于5的，则认为连续)
    如：1,2,3,4,6,7,9,22,23,24,44,45,46,47 则返回[[1,2,3,4],[22,23,24],[44,45,46,47] ]
    :param nums:
    :return:
    """
    lines = []
    line = []
    for index, num in enumerate(nums):
        if index == 0:
            line.append(num)
        else:
            if num - nums[index - 1] > X_DISTANCE:
                if len(line) >= 2:
                    lines.append(line)
                line = [num]
            else:
                line.append(num)
    if len(line) > 2:
        lines.append(line)
    return lines


def judge_num_belongs(num_group, num):
    """
    判断指定的数字于数组中归属（与哪个数字最接近）
    :param group_arr: 点数组
    :param num: 待判断的数据
    :return:
    """
    result = num_group[0]
    distance = abs(result - num)
    for x in num_group:
        cur_dis = abs(x - num)
        if cur_dis < distance:
            distance = cur_dis
            result = x
    return result


def get_alone_num(nums):
    """
    从一堆点中，获取相对独立的点,more两个单元格直接应至少间隔10厘米（这个跟倾斜度有关，太倾斜的大表容易出问题）
    :param points:
    :return:
    """
    nums = np.sort(nums)
    alone_points = [nums[0]]
    last = nums[0]
    for current in nums:
        if abs(current - last) > X_DISTANCE:
            alone_points.append(current)
            last = current
    return np.sort(alone_points)


def get_alone_points(points):
    """
    切割散乱的点，留下有意义的坐标（有明显距离）
    :param points:
    :return:
    """
    alone_points = [points[0]]
    for current in points:
        if is_alone_point(alone_points, current):
            alone_points.append(current)

    return sort_points(alone_points)


def sort_points(points):
    """
    排序点，按照从左到右，从上到下排序（即：X轴升序，X轴一样，则按Y轴升序）
    :param points:
    :return:
    """
    import functools
    def compare(point1, point2):
        if abs(point1[0] - point2[0]) < 1:
            # X轴一样的，按照Y轴升序
            if point2[1] < point1[1]:
                return 1
            elif point1[1] < point2[1]:
                return -1
            else:
                return 0
        else:
            # X轴升序
            if point2[0] < point1[0]:
                return 1
            elif point1[0] < point2[0]:
                return -1
            else:
                return 0

    return sorted(points, key=functools.cmp_to_key(compare))


def sort_points_by_x_asc(points):
    """
    按照x轴生序
    :param points:
    :return:
    """
    import functools
    def compare(point1, point2):
        if point2[0] < point1[0]:
            return 1
        elif point1[0] < point2[0]:
            return -1
        else:
            return 0

    return sorted(points, key=functools.cmp_to_key(compare))


def sort_points_by_y_asc(points):
    """
    按照Y轴生序
    :param points:
    :return:
    """
    import functools
    def compare(point1, point2):
        if point2[1] < point1[1]:
            return 1
        elif point1[1] < point2[1]:
            return -1
        else:
            return 0

    return sorted(points, key=functools.cmp_to_key(compare))


def is_alone_point(alone_points, point):
    # 与任意已有点均存在合法距离，才留下
    for alone in alone_points:
        if abs(alone[0] - point[0]) <= X_DISTANCE and abs(alone[1] - point[1]) <= Y_DISTANCE and get_point_distance(
                alone, point) <= DISTANCE:
            return False
    return True


def get_point_distance(point1, point2):
    return abs(point1[0] - point2[0]) * abs(point1[0] - point2[0])


def show_debug_image(output, image, verbose_log=False):
    """
    显示调试图片
    :param output: 输出目录
    :param image:
    :param verbose_log:
    :return:
    """
    if not verbose_log:
        return
    cv2.imwrite(output, image)


if __name__ == '__main__':
    # 合法的应该有26个
    # x_point_arr = [133, 213, 337, 492, 608, 749]
    # y_point_arr = [133, 175, 220, 286, 352]
    xs = [749, 750, 133, 749, 750, 133, 608, 749, 750, 133, 213, 214, 337, 338, 608, 749, 750, 213, 214, 337, 338, 492,
          493, 608, 749, 750, 134, 213, 214, 337, 338, 750, 751, 337, 338, 492, 493, 608, 609, 750, 751, 134, 213, 214,
          337, 338, 608, 609, 750, 751, 214, 337, 338, 492, 493, 608, 609, 750, 751, 134, 214, 337, 338, 492, 493, 134]
    ys = [133, 133, 135, 175, 175, 176, 176, 176, 176, 177, 177, 177, 177, 177, 220, 220, 220, 221, 221, 221, 221, 221,
          221, 221, 221, 221, 222, 222, 222, 222, 222, 286, 286, 287, 287, 287, 287, 287, 287, 287, 287, 288, 288, 288,
          288, 288, 352, 352, 352, 352, 353, 353, 353, 353, 353, 353, 353, 353, 353, 354, 354, 354, 354, 354, 354, 355]

    arr = [1, 2, 3, 4, 5, 6]
    arr.insert(1, 99)
    print(arr)
