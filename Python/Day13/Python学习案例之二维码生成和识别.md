## 前言

在 JavaWeb 开发中，一般使用 Zxing 来生成和识别二维码，但是，Zxing 的识别有点差强人意，不少相对模糊的二维码识别率很低。不过就最新版本的测试来说，识别率有了现显著提高。

## 对比

在没接触 Python 之前，曾使用 Zbar 的客户端进行识别，测了大概几百张相对模糊的图片，Zbar的识别速度要快很多，识别率也比 Zxing 稍微准确那边一丢丢，但是，稍微模糊一点就无法识别。相比之下，微信和支付宝的识别效果就逆天了。

## 代码案例

```python
# -*- coding:utf-8 -*-
import os
import qrcode
import time
from PIL import Image
from pyzbar import pyzbar

"""
# 升级 pip 并安装第三方库
pip install -U pip
pip install Pillow
pip install pyzbar
pip install qrcode
"""


def make_qr_code_easy(content, save_path=None):
    """
    Generate QR Code by default
    :param content: The content encoded in QR Codeparams
    :param save_path: The path where the generated QR Code image will be saved in.
                      If the path is not given the image will be opened by default.
    """
    img = qrcode.make(data=content)
    if save_path:
        img.save(save_path)
    else:
        img.show()


def make_qr_code(content, save_path=None):
    """
    Generate QR Code by given params
    :param content: The content encoded in QR Code
    :param save_path: The path where the generated QR Code image will be saved in.
                      If the path is not given the image will be opened by default.
    """
    qr_code_maker = qrcode.QRCode(version=2,
                                  error_correction=qrcode.constants.ERROR_CORRECT_M,
                                  box_size=8,
                                  border=1,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    img = qr_code_maker.make_image(fill_color="black", back_color="white")
    if save_path:
        img.save(save_path)
    else:
        img.show()


def make_qr_code_with_icon(content, icon_path, save_path=None):
    """
    Generate QR Code with an icon in the center
    :param content: The content encoded in QR Code
    :param icon_path: The path of icon image
    :param save_path: The path where the generated QR Code image will be saved in.
                      If the path is not given the image will be opened by default.
    :exception FileExistsError: If the given icon_path is not exist.
                                This error will be raised.
    :return:
    """
    if not os.path.exists(icon_path):
        raise FileExistsError(icon_path)

    # First, generate an usual QR Code image
    qr_code_maker = qrcode.QRCode(version=4,
                                  error_correction=qrcode.constants.ERROR_CORRECT_H,
                                  box_size=8,
                                  border=1,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    qr_code_img = qr_code_maker.make_image(fill_color="black", back_color="white").convert('RGBA')

    # Second, load icon image and resize it
    icon_img = Image.open(icon_path)
    code_width, code_height = qr_code_img.size
    icon_img = icon_img.resize((code_width // 4, code_height // 4), Image.ANTIALIAS)

    # Last, add the icon to original QR Code
    qr_code_img.paste(icon_img, (code_width * 3 // 8, code_width * 3 // 8))

    if save_path:
        qr_code_img.save(save_path)
    else:
        qr_code_img.show()


def decode_qr_code(code_img_path):
    """
    Decode the given QR Code image, and return the content
    :param code_img_path: The path of QR Code image.
    :exception FileExistsError: If the given code_img_path is not exist.
                                This error will be raised.
    :return: The list of decoded objects
    """
    if not os.path.exists(code_img_path):
        raise FileExistsError(code_img_path)

    # Here, set only recognize QR Code and ignore other type of code
    return pyzbar.decode(Image.open(code_img_path), symbols=[pyzbar.ZBarSymbol.QRCODE], scan_locations=True)


if __name__ == "__main__":

    # # 简易版
    # make_qr_code_easy("make_qr_code_easy", "make_qr_code_easy.png")
    # results = decode_qr_code("make_qr_code_easy.png")
    # if len(results):
    #     print(results[0].data.decode("utf-8"))
    # else:
    #     print("Can not recognize.")
    #
    # # 参数版
    # make_qr_code("make_qr_code", "make_qr_code.png")
    # results = decode_qr_code("make_qr_code.png")
    # if len(results):
    #     print(results[0].data.decode("utf-8"))
    # else:
    #     print("Can not recognize.")
    #
    # 带中间 logo 的
    # make_qr_code_with_icon("https://blog.52itstyle.vip", "icon.jpg", "make_qr_code_with_icon.png")
    # results = decode_qr_code("make_qr_code_with_icon.png")
    # if len(results):
    #     print(results[0].data.decode("utf-8"))
    # else:
    #     print("Can not recognize.")

    # 识别答题卡二维码 16 识别失败
    t1 = time.time()
    count = 0
    for i in range(1, 33):
        results = decode_qr_code(os.getcwd()+"\\img\\"+str(i)+".png")
        if len(results):
            print(results[0].data.decode("utf-8"))
        else:
            print("Can not recognize.")
            count += 1
    t2 = time.time()
    print("识别失败数量:" + str(count))
    print("测试时间:" + str(int(round(t2 * 1000))-int(round(t1 * 1000))))

```

测试了32张精挑细选模糊二维码：
```
识别失败数量:1
测试时间:130
```
使用最新版的 Zxing 识别失败了三张。
