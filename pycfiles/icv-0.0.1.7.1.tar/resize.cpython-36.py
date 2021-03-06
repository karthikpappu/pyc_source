# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/image/transforms/resize.py
# Compiled at: 2019-07-26 11:53:55
# Size of source mod 2**32: 3437 bytes
from __future__ import division
import cv2
from ..io import imread

def _scale_size(size, scale):
    """Rescale a size by a ratio.

    Args:
        size (tuple): w, h.
        scale (float): Scaling factor.

    Returns:
        tuple[int]: scaled size.
    """
    w, h = size
    return (int(w * float(scale) + 0.5), int(h * float(scale) + 0.5))


interp_codes = {'nearest':cv2.INTER_NEAREST, 
 'bilinear':cv2.INTER_LINEAR, 
 'bicubic':cv2.INTER_CUBIC, 
 'area':cv2.INTER_AREA, 
 'lanczos':cv2.INTER_LANCZOS4}

def imresize(img, size, return_scale=False, interpolation='bilinear'):
    """Resize image to a given size.

    Args:
        img (ndarray): The input image.
        size (tuple): Target (w, h).
        return_scale (bool): Whether to return `w_scale` and `h_scale`.
        interpolation (str): Interpolation method, accepted values are
            "nearest", "bilinear", "bicubic", "area", "lanczos".

    Returns:
        tuple or ndarray: (`resized_img`, `w_scale`, `h_scale`) or
            `resized_img`.
    """
    h, w = imread(img).shape[:2]
    resized_img = cv2.resize(img,
      size, interpolation=(interp_codes[interpolation]))
    if not return_scale:
        return resized_img
    else:
        w_scale = size[0] / w
        h_scale = size[1] / h
        return (resized_img, w_scale, h_scale)


def imresize_like(img, dst_img, return_scale=False, interpolation='bilinear'):
    """Resize image to the same size of a given image.

    Args:
        img (ndarray): The input image.
        dst_img (ndarray): The target image.
        return_scale (bool): Whether to return `w_scale` and `h_scale`.
        interpolation (str): Same as :func:`resize`.

    Returns:
        tuple or ndarray: (`resized_img`, `w_scale`, `h_scale`) or
            `resized_img`.
    """
    h, w = imread(dst_img).shape[:2]
    return imresize(imread(img), (w, h), return_scale, interpolation)


def imrescale(img, scale, return_scale=False, interpolation='bilinear'):
    """Resize image while keeping the aspect ratio.

    Args:
        img (ndarray): The input image.
        scale (float or tuple[int]): The scaling factor or maximum size.
            If it is a float number, then the image will be rescaled by this
            factor, else if it is a tuple of 2 integers, then the image will
            be rescaled as large as possible within the scale.
        return_scale (bool): Whether to return the scaling factor besides the
            rescaled image.
        interpolation (str): Same as :func:`resize`.

    Returns:
        ndarray: The rescaled image.
    """
    h, w = imread(img).shape[:2]
    if isinstance(scale, (float, int)):
        if scale <= 0:
            raise ValueError('Invalid scale {}, must be positive.'.format(scale))
        scale_factor = scale
    else:
        if isinstance(scale, tuple):
            max_long_edge = max(scale)
            max_short_edge = min(scale)
            scale_factor = min(max_long_edge / max(h, w), max_short_edge / min(h, w))
        else:
            raise TypeError('Scale must be a number or tuple of int, but got {}'.format(type(scale)))
    new_size = _scale_size((w, h), scale_factor)
    rescaled_img = imresize(img, new_size, interpolation=interpolation)
    if return_scale:
        return (rescaled_img, scale_factor)
    else:
        return rescaled_img