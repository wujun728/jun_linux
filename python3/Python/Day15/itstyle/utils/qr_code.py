# -*- coding:utf-8 -*-
import os
from PIL import Image
from pyzbar import pyzbar


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

