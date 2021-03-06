# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/limcv/utils.py
# Compiled at: 2019-12-11 09:22:26
# Size of source mod 2**32: 2267 bytes
import cv2, numpy as np
from PIL import Image
from .error import TemplateInputError

def generate_result(middle_point, pypts, confi):
    """Format the result: 定义图像识别结果格式."""
    ret = dict(result=middle_point, rectangle=pypts,
      confidence=confi)
    return ret


def check_image_valid(im_source, im_search):
    """Check if the input images valid or not."""
    if im_source is not None:
        if im_source.any():
            if im_search is not None:
                if im_search.any():
                    return True
    return False


def check_source_larger_than_search(im_source, im_search):
    """检查图像识别的输入."""
    h_search, w_search = im_search.shape[:2]
    h_source, w_source = im_source.shape[:2]
    if h_search > h_source or w_search > w_source:
        raise TemplateInputError('error: in template match, found im_search bigger than im_source.')


def img_mat_rgb_2_gray(img_mat):
    """
    Turn img_mat into gray_scale, so that template match can figure the img data.
    "print(type(im_search[0][0])")  can check the pixel type.
    """
    assert isinstance(img_mat[0][0], np.ndarray), 'input must be instance of np.ndarray'
    return cv2.cvtColor(img_mat, cv2.COLOR_BGR2GRAY)


def img_2_string(img):
    _, png = cv2.imencode('.png', img)
    return png.tostring()


def string_2_img(pngstr):
    nparr = np.fromstring(pngstr, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def pil_2_cv2(pil_image):
    open_cv_image = np.array(pil_image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    return open_cv_image


def cv2_2_pil(cv2_image):
    cv2_im = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    pil_im = Image.fromarray(cv2_im)
    return pil_im


def compress_image(pil_img, path, w=300, h=300):
    """
        生成缩略图
    """
    pil_img.thumbnail((w, h))
    pil_img.save(path, quality=30)