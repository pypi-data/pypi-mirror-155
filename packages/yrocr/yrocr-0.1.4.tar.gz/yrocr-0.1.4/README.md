# 开源OCR组件

自研OCR组件，包含：纯文本提取、表格提取、固定格式文件识别三大功能

## 1. 用法
### 安装

```shell

# 安装paddlepaddle依赖（请根据实际情况自行选择cpu版本，gpu版本,更多版本选择可参考：https://www.paddlepaddle.org.cn/install/quick）

# cpu版本
python -m pip install paddlepaddle>2.2.0 -i https://mirror.baidu.com/pypi/simple
# gpu版本(可选)
# python -m pip install paddlepaddle-gpu==2.3.0 -i https://mirror.baidu.com/pypi/simple
# python -m pip install paddlepaddle-gpu==2.3.0.post112 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html


# 安装yrocr依赖
pip install yrocr==0.1.4 -i https://www.pypi.org/simple/

```

### 文本识别

```shell

from yrocr import ocr_text
result = ocr_text('1.jpg')
print(result)
```

### 表格识别

```shell

from yrocr import ocr_table
result = ocr_table('任务书.jpg')
print(result)
```

### 固定格式文件识别

**身份证识别**

```shell

from yrocr import ocr_fixed_format_file
result = ocr_fixed_format_file('身份证1.jpg','idcard')
print(result)
```

输出

```json

{
  "name": "胡冬梅",
  "birth": "1973年6月8日",
  "address": "湖北省广水市广水办事处九皇熊家山208号",
  "id_number": "420983197306089328",
  "sex": "女",
  "nation": "汉",
  "issue_org": "广水市公安局",
  "validate_date": "2007.09.24-2027.09.24"
}
```

**火车票识别**

```shell

from yrocr import ocr_fixed_format_file
result = ocr_fixed_format_file('火车票49.jpg','train_ticket')
print(result)
```

输出

```json

{
	"arrival_station": "苏州北站",
	"departure_station": "北京南站",
	"train_number": "G113",
	"seat_number": "",
	"departure_date": "2020年10月27日08:50",
	"class": "",
	"price": "￥523.5元",
	"ticket_id": "30530301981031E096560",
	"check": "",
	"passenger_id": "3621331979****0618",
	"passenger_name": "曾亮"
}

```


## 2. 源码开发&调试

clone源码 ，并下载预训练模型
```shell
# clone 代码
git clone ssh://git@192.168.54.162:12022/chenjianghai/yrocr.git
# 下载预训练模型
cd yrocr/yrocr/resources
wget http://192.168.54.162:28080/yrocr_pretrain_v1_2.tar.gz
tar -xzvf yrocr_pretrain_v1_2.tar.gz && rm -rf yrocr_pretrain_v1_2.tar.gz

```

测试ocr识别，并展示识别结果
```python
# 测试基础功能- 识别并展示文本识别结果
from yrocr import ocr_text
from yrocr.ocr_base import show_ocr_result
img_path = 'data/text.jpg'
result = ocr_text(img_path)
show_ocr_result(img_path, result, f'data/show_text_result.jpg')
```


备注：yrocr_pretrain_v1_2.tar.gz中包含了：前置方向分类器模型、文件检测模型、文件分类模型、以及电子证照识别中的身份证、火车票等自行训练等


## 3. 目录说明
相关主要源码如下
```
|--README.md----------------# 简介
|--yrocr/ocr_base.py------------------# OCR识别核心文件
|--yrocr/ocr_text.py -------------------# 文本识别功能核心代码
|--yrocr/ocr_table.py ----------------# 表格抽取核心代码   
|--yrocr/ocr_fixed_format_file.py ----------------# 电子证照识别代码   
|--yrocr/post_process.py ----------------# 后处理模块  
|--yrocr/template.py ----------------# 电子证照识别模版  
|--yrocr/resources ----------------# 资源目录，存放预训练模型、分类模型、检测模型等
|--yrocr/util ----------------# 工具类
|--encryption.py ----------------# 源码加密为so文件功能  
|--encryption_package.py ----------------# 打包加密后文件
```


## 4. 遗留问题
### 问题1: 图片变形矫正
问题描述：对于变形的图像，识别率较低，应尝试进行矫正。
思路：
使用特殊的锚点，来确定图片是否扭曲，参考：https://www.pythonf.cn/read/140815（找矩形）
根据关键点定位网络模型对包含不规则文本的图像进行处理，确定多个关键点的坐标信息，并进一步构建B样条曲线；根据B样条曲线和矫正直线确定差值变换矩阵，并利用该差值变换矩阵对图像进行变化处理得到矫正后图像；根据文本识别网络模型对矫正后图像进行文本识别，确定文本识别结果信息。
本发明提供的方法先定位关键点，再构建描述文本走向的B样条曲线，然后确定B样条曲线与矫正直线之间的差值变换矩阵，并利用该差值变换矩阵对图像进行矫正，同时实现了对图像中不规则文本的矫正，
提高了最终利用文本识别网络模型进行文本识别处理的准确率。

### 问题2: 部分数字识别置信度低
对数字的抽取效果较差或虽可以识别出来，但置信度分数很低
解决方法：收集素材加入训练

### 问题3:  偶发单元格内容切割错误
文字跟表格框线靠太近，有时候会导致两个单元格被识别合并一起列
解决方法：把所有单元格的像素合并为一张图，直接识别图。留下足够间距（已验证，可以）

## 5.版本更新记录
### 2021-09-12

- 升级底层paddleocr版本到2.0.3,升级基础预测模型到V2版本
### 2021-08-30

- 优化OCR过程，改为全程不落盘，提升性能。
### 2021-08-20

- 增加火车票识别
- 调整架构，去除正则模块，融入后处理模块
- 增加各个固定文件的自定义角度判断功能，可覆盖全局图像角度判断
- 增加身份证识别（仅限中文），增加对图像对局部特征切割再合并。

### 2021-07-08

- 支持源码加密功能
- docker部署，同时支持cpu版本/gpu版本
- 纯文本识别兼容合合

### 2021-06-25

- 优化表格框架提取
- 在经费决算/预算业务单元中测试
- 解决带倾斜角度的图片的识别问题（角度小于30）
- 解决复杂表格抽取出错的bug

### 2021-06-17

- 支持跨行跨列表格的提取
- 支持单页面多个表格的提取
- 修复大量bug、优化大量细节

### 2021-06-11

- 更改表格结构提取方式
- 延长竖线长度，避免交点丢失
- 支持简单点的跨列表格提取

### 2021-06-03

- 初始可用版本
- 支持简单表格提取
