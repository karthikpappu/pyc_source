# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\gaeio\src\vis\font.py
# Compiled at: 2020-04-25 14:33:31
# Size of source mod 2**32: 2581 bytes
import matplotlib.pyplot as plt, sys, os
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-6])
from gaeio.src.vis.color import color
__all__ = [
 'font']
FontNameList = [
 'Arial', 'Helvetica', 'Segoe UI', 'Tahoma', 'Times New Roman', 'Verdana']
FontStyleList = ['Normal', 'Italic', 'Oblique']
FontWeightList = ['Normal', 'Light', 'Medium', 'Bold', 'Semibold', 'Heavy', 'Black']
FontSizeList = [i for i in range(1, 50)]

def updatePltFont(fontstyle):
    """
    Update the font style in matplotlib

    Args:
        fontstyle: Font style dictionary with the following keys: Name, Size, Weight, Color,

    Return:
        N/A
    """
    if fontstyle is None or len(fontstyle.keys()) < 1:
        return
    else:
        if 'Name' in fontstyle.keys():
            plt.rcParams['font.sans-serif'] = fontstyle['Name']
        else:
            if 'Size' in fontstyle.keys():
                plt.rcParams['font.size'] = fontstyle['Size']
                plt.rcParams['axes.titlesize'] = fontstyle['Size']
                plt.rcParams['axes.labelsize'] = fontstyle['Size']
            if 'Weight' in fontstyle.keys():
                plt.rcParams['font.weight'] = fontstyle['Weight'].lower()
                plt.rcParams['axes.titleweight'] = fontstyle['Weight'].lower()
                plt.rcParams['axes.labelweight'] = fontstyle['Weight'].lower()
        if 'Color' in fontstyle.keys():
            plt.rcParams['text.color'] = fontstyle['Color'].lower()
            plt.rcParams['axes.labelcolor'] = fontstyle['Color'].lower()
            plt.rcParams['xtick.color'] = fontstyle['Color'].lower()
            plt.rcParams['ytick.color'] = fontstyle['Color'].lower()


class font:
    FontNameList = FontNameList
    FontColorList = color.ColorList
    FontStyleList = FontStyleList
    FontWeightList = FontWeightList
    FontSizeList = FontSizeList
    updatePltFont = updatePltFont