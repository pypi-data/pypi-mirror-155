import json
import cv2
import math
import base64


def write_json_data(file_path, json_data):
    with open(file_path, "w") as fp:
        fp.write(json.dumps(json_data, ensure_ascii=False, indent=4))


def pdf_2_images(pdf_file, img_path, append_real_name=True):
    """
    pdf批量转图片
    实际测试，19页pdf的情况下，300dpi，耗时10秒；200dpi:耗时4秒；100dpi耗时 2.7秒
    :param pdf_file:
    :param img_path:
    :param append_real_name: 生成的图片是否加上真实名
    :return:
    """
    from PIL import ImageFile,Image
    # 下面这两行代码是解决图片太大时，转换爆出exceeds limit of 178956970 pixel的异常。
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    Image.MAX_IMAGE_PIXELS = None
    from pdf2image import convert_from_path
    arr = pdf_file.split("/")
    real_name = arr[len(arr) - 1].replace(".pdf", "").replace(".PDF", "")
    print("real_name:" + real_name)
    pages = convert_from_path(pdf_file, 300)
    img_files = []
    for (index, page) in enumerate(pages):
        img_file = f'{img_path}/{real_name}_{index}.jpg' if append_real_name else f'{img_path}/{index}.jpg'
        page.save(img_file, 'jpeg')
        img_files.append(img_file)
    return img_files


def resize(image, target_width=0, target_height=0, dest_path=None):
    """
    将图片缩放到指定的宽度，高度自适应
    :param image: cv2 image
    :param target_width: 目标宽度，为0则为根据高度自适应
    :param target_height: 目标高度，为0则为根据宽度自适应
    :return:
    """
    hei, width = image.shape[0:2]
    if target_width == 0:
        target_width = int(target_height / hei * width)
    elif target_height == 0:
        target_height = int(target_width / width * hei)
    standard_img = cv2.resize(image, (target_width, target_height))
    if dest_path:
        cv2.imwrite(dest_path, standard_img)
    return standard_img


def corp_image(image, xmin, xmax, ymin, ymax, save_path=None):
    """
    裁剪图片
    :param image: cv2 image
    :param xmin:
    :param xmax:
    :param ymin:
    :param ymax:
    :return:
    """
    img_range = image[ymin:ymax, xmin:xmax]
    if save_path:
        cv2.imwrite(save_path, img_range)
    return img_range


def point_distance(x1, y1, x2, y2):
    """
    计算两个点之间的距离
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
    x = x1 - x2
    y = y1 - y2
    return math.sqrt((x ** 2) + (y ** 2))


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def img2base64(img_file_path):
    """
    图片转base64
    :param img_file_path:
    :return:
    """
    with open(img_file_path, "rb") as fb:
        img = fb.read()
        base64_bytes = base64.b64encode(img)
        base64_str = base64_bytes.decode("utf-8")
    return base64_str


if __name__ == '__main__':
    # src = '/Users/chenjianghai/PycharmProjects/yrocr/yrocr/data/table/img/audit/6-拆除设备评估鉴定表/评估鉴定表.pdf'
    target = './debug'
    src = '/Users/chenjianghai/Downloads/华久营业执照扫描件.pdf'
    pdf_2_images(src,target)
