import os

from setuptools import setup, find_packages

this_folder = os.path.abspath(os.path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os.path.join(this_folder, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


# 发布外网，信息保密，不宜展示
# gitlab_url = "http://192.168.54.162:12000/chenjianghai/yrocr"
gitlab_url = "https://pypi.org/project/yrocr"

setup(
    name="yrocr",
    version="0.1.8",
    author="ocr team",
    author_email="ocr@qq.com",
    description="OCR",
    long_description='基于开源paddleOcr的OCR小工具',
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    keywords="yrocr",
    url=gitlab_url,
    packages=find_packages(exclude=["test.py"]),
    include_package_data=True,
    install_requires=[
        "pdf2image",
        "paddlex==1.3.7",
        "paddleocr==2.0.1",
        "opencv-python==4.2.0.32",
        "opencv-contrib-python-headless==4.2.0.32",
        "click"
    ],
    classifiers=[
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points="""
        [console_scripts]
        ocr=yrocr.cli:ocr_cli
    """
)
