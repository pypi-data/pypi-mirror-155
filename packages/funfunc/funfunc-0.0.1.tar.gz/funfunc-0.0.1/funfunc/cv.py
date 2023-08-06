# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 16:32
# FILE    : cv
# PROJECT : funfunc
# IDE     : PyCharm
from io import BytesIO
from typing import Literal
import base64

import cv2

_ImageFormat = Literal['jpg', 'png', 'jpeg', 'bmp', 'gif']


def pil_image_to_base64_string(pil_image,
                               image_format: _ImageFormat) -> str:
    temp_buffer = BytesIO()
    try:
        pil_image.save(temp_buffer, format=image_format)
    except Exception as e:
        raise NotImplementedError(f'pil_image has not method save(), is this a PIL.Image? {e}')
    byte_data = temp_buffer.getvalue()
    base64_string = base64.b64encode(byte_data).decode('utf-8')
    return base64_string


def base64_string_to_pil_image(image_base64_string: str):
    from PIL import Image

    img_b64decode = base64.b64decode(image_base64_string)
    image_bytes = BytesIO(img_b64decode)
    pil_image = Image.open(image_bytes)
    return pil_image


def pil_image_to_cv_image(pil_image):
    import cv2
    import numpy as np

    cv_image = cv2.cvtColor(np.asarray(pil_image), cv2.COLOR_RGB2BGR)
    return cv_image


def cv_image_to_pil_image(cv_image):
    import cv2
    from PIL import Image

    pil_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    return pil_image


def cv_image_to_base64_string(cv_image, image_format: _ImageFormat) -> str:
    temp_string = cv2.imencode(image_format, cv_image)[1].tostring()
    base64_string = base64.b64encode(temp_string).decode('utf-8')
    return base64_string


def base64_string_to_cv_image(base64_string: str):
    import cv2
    import numpy as np

    base64_decode = base64.b64decode(base64_string)
    cv_image = cv2.imdecode(np.frombuffer(base64_decode, np.uint8), cv2.COLOR_BGR2RGB)
    return cv_image
