#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : image
# @Time         : 2022/6/15 上午11:33
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 
from meutils.pipe import *


def image_read(filename):
    _bytes = b''
    if filename.startswith('http'):
        _bytes = requests.get(url).content

    elif Path(filename).exists():
        _bytes = Path(filename).read_bytes()

    if _bytes:
        import cv2
        np_arr = np.frombuffer(_bytes, dtype=np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return img

    # from PIL import Image
    # np.asarray((Image.open(bio)))


if __name__ == '__main__':
    url = "https://i1.mifile.cn/f/i/mioffice/img/slogan_5.png?1604383825042"

    print(image_read(url))
