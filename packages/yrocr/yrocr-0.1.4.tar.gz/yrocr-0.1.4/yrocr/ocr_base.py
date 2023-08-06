#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc: OCR抽取基础
# 指定可见的GPU
import os

# 这种指定方式无效。paddleocr只支持在启动时直接指定CUDA_VISIBLE_DEVICES。
# 如：nvidia-docker run --env MAX_SHAPE=3000 --env CUDA_VISIBLE_DEVICES=2  --name yrocr-gpu_11_2_v1.2 -dit -p 28888:28888 yrocr-gpu_11_2:1.2
cuda_device = os.environ.get('cuda_device')
if cuda_device:
    os.environ['CUDA_VISIBLE_DEVICES'] = cuda_device

import json
from pathlib import Path
import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont
from paddleocr import PaddleOCR
from paddleocr.ppocr.utils.logging import get_logger
from yrocr.config import get_ocr_txt_server_url
from yrocr.util.util import resize

logger = get_logger(name='ocr_format_file')
base_path = os.path.dirname(__file__)
DEBUG_FOLDER = 'debug'
if not os.path.exists(DEBUG_FOLDER):
    os.mkdir(DEBUG_FOLDER)

base_path = os.path.dirname(__file__)
home_path = os.path.join(Path.home(), '.yrocr')
# 兼容docker中的变量设置、兼容pypi安装包的方式
OCR_CLS_PATH = os.environ.get('OCR_CLS_PATH')
if not OCR_CLS_PATH:
    OCR_CLS_PATH = os.path.join(base_path, 'resources/pretrain/mobile/cls')
    if not os.path.exists(OCR_CLS_PATH):
        OCR_CLS_PATH = os.path.join(home_path, 'pretrain/cls')
OCR_DET_PATH = os.environ.get('OCR_DET_PATH')
if not OCR_DET_PATH:
    OCR_DET_PATH = os.path.join(base_path, 'resources/pretrain/mobile/det')
    if not os.path.exists(OCR_DET_PATH):
        OCR_DET_PATH = os.path.join(home_path, 'pretrain/det')
OCR_REC_PATH = os.environ.get('OCR_REC_PATH')
if not OCR_REC_PATH:
    OCR_REC_PATH = os.path.join(base_path, 'resources/pretrain/mobile/rec')
    if not os.path.exists(OCR_REC_PATH):
        OCR_REC_PATH = os.path.join(home_path, 'pretrain/rec')

# os.environ.setdefault('USE_GPU', 'true')
USE_GPU = os.environ.get('USE_GPU')
if USE_GPU and USE_GPU == 'true':
    USE_GPU = True
else:
    USE_GPU = False

FONTS_PATH = os.path.join(base_path, 'resources/fonts/simfang.ttf')
# 16G内存/显存存，建议设置为4000，默认为4000，8G的话，设置为3000，低配置的话可设置为2000，默认先设置为3000
MAX_SHAPE = os.environ.get('MAX_SHAPE')
if not MAX_SHAPE:
    MAX_SHAPE = 2000
else:
    MAX_SHAPE = int(MAX_SHAPE)
MAX_WIDTH = MAX_SHAPE
MAX_HEIGHT = MAX_SHAPE
DEBUG_FOLDER = 'debug'
if not os.path.exists(DEBUG_FOLDER):
    os.mkdir(DEBUG_FOLDER)


def invoke_ocr(image, drop_score=0.1, use_angle_cls=True, det_model='', rec_model=''):
    """
    调用底层OCR
    说明：
    use_angle_cls 用于会对所有的文字行进行旋转角度判断，及其影响效率（且不会对竖排文字的识别造成影响），一般情况下先关闭
    :param image: 图像数据
    :param drop_score: 丢弃的分数
    :param det_model: 自定义检测模型路径
    :param rec_model: 自定义识别模型路径
    :return:

    """
    # 如果强制使用商业版本，则直接调用
    # if is_use_commercial_ocr():
    #     return invoke_commercial_ocr(img_path)
    parpare_pretrain(OCR_CLS_PATH)
    has_resize, rate, new_image = resize_img(image)
    ocr = PaddleOCR(use_angle_cls=use_angle_cls, cls=use_angle_cls, lang="ch", drop_score=drop_score,
                    det_model_dir=det_model if len(det_model) > 0 else OCR_DET_PATH,
                    rec_model_dir=rec_model if len(rec_model) > 0 else OCR_REC_PATH,
                    cls_model_dir=OCR_CLS_PATH,
                    det_db_box_thresh=0.5,
                    det_db_unclip_ratio=1.5,
                    use_gpu=USE_GPU)
    if has_resize:
        result = ocr.ocr(new_image, cls=True)
    else:
        result = ocr.ocr(image, cls=True)
    """ 原始格式如下
    [   
          [
            [[189.0, 271.0], [622.0, 269.0], [623.0, 361.0], [190.0, 363.0]],
            ('营业执照', 0.9948882)
          ],
          [
            [[351.0, 371.0], [463.0, 371.0], [463.0, 411.0], [351.0, 411.0]],
            ('（副本）', 0.9627871)
          ]
        ]
    四个点位分别为：左上、右上、右下、左下
    """
    result = [
        {
            'block_id': str(index + 1),
            'score': str(line[1][1]),
            'text': str(line[1][0]),
            'position': get_points(line[0])
        }

        for index, line in enumerate(result)
    ]
    if has_resize:
        resume_origal_position(rate, result)
    return result


def invoke_commercial_ocr(img_path, detect_direction=True):
    """
    调用商业版本OCR（即：合合）
    :param img_path: 图片地址
    :return:
    """

    from yrocr.util.util import img2base64
    base64_data = img2base64(img_path)
    data = {'task_data': base64_data}
    if detect_direction:
        data['detect_direction'] = 1
    headers = {"Content-type": "application/json"}
    r = requests.post(url=get_ocr_txt_server_url(), headers=headers, data=json.dumps(data))
    print(r.status_code)
    if r.status_code != 200:
        raise Exception(f'invoke ocr http error:{r.status_code}')
    resp = r.json()
    if resp['code'] != 200:
        raise Exception(f"invoke ocr error:{resp['message']}")

    blocks = resp['data'][0]['recognize_data_detail']
    result = [
        {
            'block_id': str(index + 1),
            'score': '1.0',
            'text': str(block['data']),
            'position': get_commercial_block_points(block['position'])
        }

        for index, block in enumerate(blocks)
    ]
    return result


def get_commercial_block_points(position):
    """
    获取商业版本ocr的块中的点
    :param position:
    :return:
    """
    # "372,63,700,62,700,78,372,80"
    # 四个点位分别为：左上、右上、右下、左下
    points = position.split(",")
    return [
        [int(points[0]), int(points[1])],
        [int(points[2]), int(points[3])],
        [int(points[4]), int(points[5])],
        [int(points[6]), int(points[7])]
    ]


def get_points(points):
    return [
        [round(points[0][0]), round(points[0][1])],
        [round(points[1][0]), round(points[1][1])],
        [round(points[2][0]), round(points[2][1])],
        [round(points[3][0]), round(points[3][1])]
    ]


def resize_img(img):
    """
    缩放图片
    :param img: image
    :return: 是否缩放、缩放比例、缩放后图像内容
    """
    hei, width = img.shape[0:2]
    logger.info(f"最大宽度{MAX_WIDTH},{MAX_HEIGHT}。图片宽度{hei},{width}")
    if width > hei and width > MAX_WIDTH:
        rate = width / MAX_WIDTH
        new_image = resize(img, MAX_WIDTH, 0)
        return True, rate, new_image
    elif hei > width and hei > MAX_HEIGHT:
        rate = hei / MAX_HEIGHT
        new_image = resize(img, 0, MAX_HEIGHT)
        return True, rate, new_image
    return False, 1.0, None


def _get_tmp_file(img_path):
    import uuid
    uid = str(uuid.uuid4())
    tmp_id = ''.join(uid.split('-'))
    from pathlib import Path
    suffix = Path(img_path).suffix
    if not os.path.exists(DEBUG_FOLDER):
        os.makedirs(DEBUG_FOLDER)
    return os.path.join(DEBUG_FOLDER, tmp_id + suffix)


def resume_origal_position(rate, result):
    """
    还原图片原始位置
    :param rate:
    :param result:
    :return:
    """
    for item in result:
        position = item['position']
        new_position = [
            [round(point[0] * rate), round(point[1] * rate)]
            for point in position
        ]
        item['position'] = new_position


def draw_text(img, text, left, top, text_color=(255, 0, 255), text_size=14):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(FONTS_PATH, text_size, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, text_color, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def get_ocr_point_rect(points):
    """
    将OCR识别结果的四个点坐标转为矩形
    :param points:
    :return:
    """
    xmin = min(points[0][0], points[1][0], points[2][0], points[3][0])
    xmax = max(points[0][0], points[1][0], points[2][0], points[3][0])
    ymin = min(points[0][1], points[1][1], points[2][1], points[3][1])
    ymax = max(points[0][1], points[1][1], points[2][1], points[3][1])
    width = xmax - xmin
    hei = ymax - ymin
    # return [xmin, xmax, ymin, ymax, width, hei]
    return {
        "left": xmin,
        "top": ymin,
        "width": width,
        "height": hei
    }


def show_ocr_result(img_path, result, output):
    """
    可视化识别结果
    :param img_path: 图片路径
    :param result: 识别结果
    :param output: 输出路径
    :return:
    """
    image = cv2.imread(img_path)
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
    cv2.imwrite(output, image)


def parpare_pretrain(cls_model_path):
    if os.path.exists(cls_model_path):
        logger.debug("pretrain exists.not need to download ：" + cls_model_path)
        return
    from pathlib import Path
    target = os.path.join(Path.home(), '.yrocr')
    if not os.path.exists(target):
        os.mkdir(target)
    if os.path.exists(os.path.join(target, 'pretrain')):
        logger.debug("pretrain exists:" + os.path.join(target, 'pretrain'))
        return
    from paddleocr.paddleocr import download_with_progressbar
    url = 'http://192.168.54.162:28080/yrocr_pretrain_v1_2.tar.gz'
    # url = "http://localhost:8080/biz_models/yrocr_pretrain_v1_2.tar.gz"
    tmp_path = os.path.join(target, url.split('/')[-1])
    logger.info(f"download pretrain file [{url}] to:{tmp_path}")
    download_with_progressbar(url, tmp_path)
    import tarfile
    with tarfile.open(tmp_path, mode="r:gz") as tarObj:
        tarObj.extractall(path=target)
    os.remove(tmp_path)
    logger.info("finish pretrain.")


if __name__ == '__main__':
    img_path = "/Users/chenjianghai/job/YR/OCR/公司内部测试数据/1.文本识别/3.四川大学项目审计报告_0.jpg"
    result = invoke_ocr(cv2.imread(img_path))
    print(result)
