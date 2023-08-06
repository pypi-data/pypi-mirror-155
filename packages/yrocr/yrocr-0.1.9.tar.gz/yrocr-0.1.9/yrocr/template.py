#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: 模版标注
import json
import cv2
import numpy as np


def print_ocr():
    """
    OCR图片，并打印定制模版需要的信息
    :return:
    """
    img_path = 'data/test/template/bizlicense1.jpg'
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    result = ocr.ocr(img_path, cls=True)
    for line in result:
        points = line[0]
        text = line[1][0]
        # 变成矩形
        xmin = min(points[0][0], points[1][0], points[2][0], points[3][0])
        xmax = max(points[0][0], points[1][0], points[2][0], points[3][0])
        ymin = min(points[0][1], points[1][1], points[2][1], points[3][1])
        ymax = max(points[0][1], points[1][1], points[2][1], points[3][1])
        width = int(xmax) - int(xmin)
        height = int(ymax) - int(ymin)
        anchor = {
            "text": text,
            "left": int(xmin),
            "top": int(ymin),
            "width": width,
            "height": height
        }
        print("text: " + text, "anchor:", anchor)


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json_data(file_path, json_data):
    with open(file_path, "w") as fp:
        fp.write(json.dumps(json_data, ensure_ascii=False, indent=4))


def labelme_to_template(json_file, template_name='模版'):
    """
    将labelme标注的数据，转为模版数据
    :param json_file:
    :return:
    """
    label = read_json(json_file)

    anchors = []
    recognition_areas = []
    shapes = label['shapes']
    for shape in shapes:
        points = shape['points']
        left = int(points[0][0])
        top = int(points[0][1])
        width = int(points[1][0]) - left
        height = int(points[1][1]) - top
        text = shape['label']
        if str.startswith(text, '锚点'):
            text = str.replace(text, '锚点_', '')
            anchors.append({
                "text": text,
                "left": left,
                "top": top,
                "width": width,
                "height": height,
                # 默认不支持锚点的前缀匹配
                "prefix_match": "no"
            })
        else:
            # 待识别区域
            recognition_areas.append({
                "field_name": text,
                "left": left,
                "top": top,
                "width": width,
                "height": height
            })
    template = {
        "name": template_name,
        "imageHeight": label['imageHeight'],
        "imageWidth": label['imageWidth'],
        "anchors": anchors,
        "recognition_areas": recognition_areas
    }
    return template


def show_template_labeld_info(img_path, template_path):
    """
    显示标注信息
    :param img_path:
    :param template_path:
    :return:
    """
    template = read_json(template_path)
    # 加载图片，并安装标注信息，绘制矩形，并展示
    from PIL import Image
    image = Image.open(img_path).convert('RGB')
    for area in template['anchors']:
        xmin = round(area['left'])
        ymin = round(area['top'])
        xmax = round(xmin + area['width'])
        ymax = round(ymin + area['height'])
        box = [
            [xmin, ymin],
            [xmax, ymin],
            [xmax, ymax],
            [xmin, ymax]
        ]
        box = np.reshape(np.array(box), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True, (255, 0, 255), 4)
    for area in template['recognition_areas']:
        xmin = round(area['left'])
        ymin = round(area['top'])
        xmax = round(xmin + area['width'])
        ymax = round(ymin + area['height'])
        box = [
            [xmin, ymin],
            [xmax, ymin],
            [xmax, ymax],
            [xmin, ymax]
        ]
        box = np.reshape(np.array(box), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True, (255, 0, 0), 2)
    cv_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # cv2.imwrite('result_cv.jpg', cv_img)
    cv2.imshow("final", cv_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def update_template_position(template_file, lableme_json_file):
    """
    根据label_me的标注结果，更新template_file（只更新锚点/待抽取区域的位置,保留所有手工编辑的内容）
    :param template_file:
    :param lableme_json_file:
    :return:
    """
    new_template = labelme_to_template(lableme_json_file)
    old_template = read_json(template_file)
    # 更新锚点
    old_anchors_dict = {}
    for anchor in old_template['anchors']:
        old_anchors_dict[anchor['text']] = anchor

    anchors = []
    for anchor in new_template['anchors']:
        if anchor['text'] in old_anchors_dict:
            print("保留锚点:" + anchor['text'])
            combine_anchor = old_anchors_dict[anchor['text']]
            combine_anchor['left'] = anchor['left']
            combine_anchor['top'] = anchor['top']
            combine_anchor['width'] = anchor['width']
            combine_anchor['height'] = anchor['height']
            anchors.append(combine_anchor)
        else:
            print("####新增锚点:" + anchor['text'])
            anchors.append(anchor)
    old_template['anchors'] = anchors
    # 更新标注区域
    recognition_areas_dict = {}
    areas = []
    for area in old_template['recognition_areas']:
        recognition_areas_dict[area['field_name']] = area

    for area in new_template['recognition_areas']:
        if area['field_name'] in recognition_areas_dict:
            # 只更新抽取区域的坐标，其他的，全是旧的配置信息
            print("保留待抽取区域:" + area['field_name'])
            combine_area = recognition_areas_dict[area['field_name']]
            combine_area['left'] = area['left']
            combine_area['top'] = area['top']
            combine_area['width'] = area['width']
            combine_area['height'] = area['height']
            areas.append(combine_area)
        else:
            print("####新增待选区域:" + area['field_name'])
            areas.append(area)
    old_template['recognition_areas'] = areas
    old_template['imageHeight'] = new_template['imageHeight']
    old_template['imageWidth'] = new_template['imageWidth']
    write_json_data(template_file, old_template)


if __name__ == '__main__':
    # for index in range(2, 12):
    #     labelme_file = 'data/ningxiang/images/' + str(index) + '.json'
    #     img_file = 'data/ningxiang/images/' + str(index) + '.JPG'
    #     template_file = 'data/ningxiang/templates/template_' + str(index) + '.json'
    #     labelme_to_template(labelme_file, template_file)

    index = 1
    # labelme_file = 'data/images/biz_license_erected_{}.json'.format(index)
    # img_file = 'data/images/biz_license_erected_{}.JPG'.format(index)
    # template_file = 'data/templates/template_biz_lic_erected_{}.json'.format(index)
    config = {
        'name': '增值税发票',
        'namespace': '',
        'en_name': 'vat_special_invoice',
        'img_suffix': 'jpg'
    }
    name = config['name']
    key = config['en_name']
    img_suffix = config['img_suffix']
    namespace = config['namespace']
    labelme_file = f'resources/sample/{key}.json'
    img_file = f'resources/sample/{key}.{img_suffix}'
    template_file = f'resources/templates/tpl_{key}.json'
    if len(namespace) > 0:
        labelme_file = f'resources/sample/{namespace}/{key}.json'
        img_file = f'resources/sample/{namespace}/{key}.{img_suffix}'
        template_file = f'resources/templates/{namespace}/tpl_{key}.json'
    # 转模版s
    template = labelme_to_template(labelme_file, name)
    # write_json_data(template_file, template)
    # update_template_position(template_file, labelme_file)
    show_template_labeld_info(img_file, template_file)
