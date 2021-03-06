# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\ROC\read.py
# Compiled at: 2018-07-30 03:33:59


def read(root):
    u"""
    读取一个xml文件的所有标签
    """
    Reframe = []
    xmin = root.getElementsByTagName('xmin')
    xmax = root.getElementsByTagName('xmax')
    ymin = root.getElementsByTagName('ymin')
    ymax = root.getElementsByTagName('ymax')
    rectnum = len(xmin)
    for i in range(0, rectnum):
        n1 = xmin[i]
        n2 = xmax[i]
        n3 = ymin[i]
        n4 = ymax[i]
        Xmin = Ymin = Xmax = Ymax = 0
        Xmin = int(n1.firstChild.data)
        Xmax = int(n2.firstChild.data)
        Ymin = int(n3.firstChild.data)
        Ymax = int(n4.firstChild.data)
        Reframe.append([Xmin, Ymin, Xmax, Ymax])

    return Reframe