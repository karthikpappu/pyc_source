# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/wsiprocess/utils.py
# Compiled at: 2019-11-26 07:49:32
# Size of source mod 2**32: 902 bytes
import json, cv2
from pathlib import Path

def show_bounding_box(patch_path, result_path, save_as):
    img = cv2.imread(patch_path)
    with open(result_path, 'r') as (f):
        result = json.load(f)
    x, y = Path(patch_path).stem.split('_')
    for patch in result['result']:
        if patch['x'] == int(x) and patch['y'] == int(y):
            for bbs in patch['bbs']:
                x1 = bbs['x']
                y1 = bbs['y']
                x2 = bbs['x'] + bbs['w']
                y2 = bbs['y'] + bbs['h']
                color = (255, 255, 0)
                cv2.rectangle(img, (x1, y1), (x2, y2), color)

    cv2.imwrite(save_as, img)


def show_mask_on_patch(patch_path, mask_path, save_as):
    patch = cv2.imread(str(patch_path))
    mask = cv2.imread(str(mask_path)) * 255
    patch_with_mask = cv2.addWeighted(patch, 0.7, mask, 0.3, 0)
    cv2.imwrite(save_as, patch_with_mask)