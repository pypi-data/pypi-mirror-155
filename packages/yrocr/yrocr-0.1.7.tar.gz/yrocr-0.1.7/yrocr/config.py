import os

use_commercial_ocr = False
ocr_txt_server_url = "http://192.168.55.199:30007/recognize/ocr/ocr_data"
ocr_table_server_url = "http://192.168.55.199:30004/icr/recognize_multi_table_raw"
if os.environ.get('use_commercial_ocr'):
    use_commercial_ocr = True if os.environ.get('use_commercial_ocr') == 'yes' else False
if os.environ.get('ocr_txt_server_url'):
    ocr_txt_server_url = os.environ.get('ocr_txt_server_url')
if os.environ.get('ocr_table_server_url'):
    ocr_table_server_url = os.environ.get('ocr_table_server_url')


def is_use_commercial_ocr():
    return use_commercial_ocr


def get_ocr_txt_server_url():
    return ocr_txt_server_url


def get_ocr_table_server_url():
    return ocr_table_server_url
