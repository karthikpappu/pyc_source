# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\shaonutil\image.py
# Compiled at: 2020-05-02 06:04:33
# Size of source mod 2**32: 2498 bytes
"""Image"""
from PIL import Image, ImageDraw, ImageFont, ImageOps
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import io

def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=(image.format))
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def svg2img(infile, outfile):
    drawing = svg2rlg(infile)
    ext = outfile.split('.')[(-1)]
    renderPM.drawToFile(drawing, outfile, fmt=(ext.upper()))


def svg2pdf(infile, outfile):
    drawing = svg2rlg(infile)
    renderPDF.drawToFile(drawing, outfile)


def change_image_size_ratio(img_name, out_name, percent):
    im = Image.open(img_name)
    width, height = im.size
    Iwidth, Iheight = int(width + width * (percent / 100)), int(height + height * (percent / 100))
    im = im.resize((Iwidth, Iheight), resample=(Image.ANTIALIAS))
    im.save(out_name)


def draw_text(img, text, fnt_name, fnt_size):
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(fnt_name, fnt_size)
    d.text((0, 0), text, font=fnt, fill=(0, 0, 0))
    del d
    return img


def merge_horizontally(images, filename=''):
    if type(images[0]) == Image.Image:
        pass
    elif type(images[0]) == str:
        images = [Image.open(x) for x in images]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]
    else:
        if len(filename) > 0:
            new_im.save(filename)
            return filename
        return new_im


def merge_vertically(images, filename=''):
    if type(images[0]) == Image.Image:
        pass
    elif type(images[0]) == str:
        images = [Image.open(x) for x in images]
    widths, heights = zip(*(i.size for i in images))
    max_width = max(widths)
    total_height = sum(heights)
    new_im = Image.new('RGB', (max_width, total_height))
    y_offset = 0
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]
    else:
        if len(filename) > 0:
            new_im.save(filename)
            return filename
        return new_im


def give_screenshot_caption(img_name, text, fnt_path):
    img1 = Image.open(img_name)
    width, height = img1.size
    x0, y0 = (0, 0)
    x1 = width
    y1 = height * 0.05
    fnt_size = int(y1)
    new_im = Image.new('RGB', (width, fnt_size), (0, 0, 255))
    img_text = draw_text(new_im, text, fnt_path, fnt_size)
    img__ = merge_vertically([img_text, img1])
    img__.save(img_name, 'PNG', quality=75)


if __name__ == '__main__':
    pass