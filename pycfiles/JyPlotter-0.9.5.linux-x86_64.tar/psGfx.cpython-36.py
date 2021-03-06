# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/PyPlotter/psGfx.py
# Compiled at: 2017-05-19 15:14:36
# Size of source mod 2**32: 8113 bytes
"""Implements Gfx.Driver for Postscript"""
import re
try:
    import Gfx
except ImportError:
    from . import Gfx

try:
    from Compatibility import *
except ImportError:
    from .Compatibility import *

driverName = 'psGfx'
DPI = 72
RES_X, RES_Y = (842, 595)
SPECIAL_CHARACTERS = {'ä':'/adieresis', 
 'Ä':'/Adieresis', 
 'ö':'/odieresis', 
 'Ö':'/Odieresis', 
 'ü':'/udieresis', 
 'Ü':'/Udieresis', 
 'ß':'/germandbls', 
 'â':'/acircumfles', 
 'à':'/agrave', 
 'á':'/aacute', 
 'é':'/eacute', 
 'É':'/Eacute', 
 'è':'/egrave', 
 'ê':'/ecircumflex', 
 'ë':'/edieresis', 
 'ô':'/ocircumflex', 
 'ï':'/idieresis', 
 'ç':'/ccedilla', 
 'Ç':'/Ccedilla', 
 '€':'/Euro'}
PS_DOCSTART = '%%!PS-Adobe-3.0 EPSF-3.0\n%%%%BoundingBox: 0 0 %d %d\n%%%%Creator: PyPlotter.psGfx graphics driver\n%%%%LanguageLevel: 2\n%%%%EndComments\n\n'
PS_DOCEND = '%%EOF\n'
PS_PAGESTART = '%%Page: 1 1\n'
PS_PAGEEND = '\n'

class Driver(Gfx.Driver):
    __doc__ = 'A postscript graphics driver      \n    '

    def __init__(self, resX=RES_X, resY=RES_Y):
        Gfx.Driver.__init__(self)
        self.ps = []
        self.resX, self.resY = (0, 0)
        self.setSize(resX, resY)
        self.clear()

    def getPostscript(self):
        """Returns the postscript commands as one long string!"""
        return ''.join(self.ps + [PS_PAGEEND, PS_DOCEND])

    def save(self, fName):
        """Saves the contents as a file."""
        f = open(fName, 'w')
        f.write(self.getPostscript())
        f.close()

    def reset(self):
        self.setColor((0.0, 0.0, 0.0))
        self.setLineWidth(Gfx.THIN)
        self.setLinePattern(Gfx.CONTINUOUS)
        self.setFillPattern(Gfx.SOLID)
        self.setFont(Gfx.SANS, Gfx.NORMAL, Gfx.PLAIN)

    def getSize(self):
        return (
         self.resX, self.resY)

    def setSize(self, resX, resY, keepPageRatio=True):
        if keepPageRatio:
            pageRatio = RES_X / float(RES_Y)
            if resX / resY < pageRatio:
                resX = int(resY * pageRatio + 0.5)
            else:
                resY = int(resX / pageRatio + 0 - 5)
        self.resX = resX
        self.resY = resY
        if self.ps:
            self.ps[0] = PS_DOCSTART % (self.resX, self.resY)

    def getResolution(self):
        return int(self.resX / 11.7)

    def setResolution(self, dpi):
        self.resX = int(dpi * 11.7)
        self.resY = int(dpi * 8.26)

    def setColor(self, rgbTuple):
        self.color = rgbTuple
        self.ps.append('%f %f %f setrgbcolor\n' % rgbTuple)

    def setLineWidth(self, width):
        self.lineWidth = width
        if width == Gfx.THIN:
            tn = 1.0
        else:
            if width == Gfx.MEDIUM:
                tn = 2.0
            else:
                if width == Gfx.THICK:
                    tn = 3.0
                else:
                    raise ValueError("'thickness' must be 'thin', 'medium' or thick' !")
        self.ps.append('%f setlinewidth\n' % tn)

    def setLinePattern(self, pattern):
        self.linePattern = pattern
        if pattern == Gfx.CONTINUOUS:
            lp = '[] 0'
        else:
            if pattern == Gfx.DASHED:
                lp = '[4 4] 2'
            else:
                if pattern == Gfx.DOTTED:
                    lp = '[2 5] 0'
                else:
                    raise ValueError("'pattern' must be 'continuous','dashed' " + "or 'dotted'")
        self.ps.append('%s setdash\n' % lp)

    def setFillPattern(self, pattern):
        self.fillPattern = pattern

    def setFont(self, ftype, size, weight):
        self.fontType = ftype
        self.fontSize = size
        self.fontWeight = weight
        verrorStr = "'weight' must be '','b','i' or 'bi'!"
        if ftype == Gfx.FIXED:
            if weight == Gfx.BOLDITALIC:
                name = '/Courier-BoldOblique'
            else:
                if weight == Gfx.ITALIC:
                    name = '/Courier-Oblique'
                else:
                    if weight == Gfx.BOLD:
                        name = '/Courier-Bold'
                    else:
                        if weight == Gfx.PLAIN:
                            name = '/Courier'
                        else:
                            raise ValueError(verrorStr)
        elif ftype == Gfx.SERIF:
            if weight == Gfx.BOLDITALIC:
                name = '/Times-BoldItalic'
            else:
                if weight == Gfx.ITALIC:
                    name = '/Times-Italic'
                else:
                    if weight == Gfx.BOLD:
                        name = '/Times-Bold'
                    else:
                        if weight == Gfx.PLAIN:
                            name = '/Times-Roman'
                        else:
                            raise ValueError(verrorStr)
        else:
            if ftype == Gfx.SANS:
                if weight == Gfx.BOLDITALIC:
                    name = '/Helvetica-BoldOblique'
                else:
                    if weight == Gfx.ITALIC:
                        name = '/Helvetica-Oblique'
                    else:
                        if weight == Gfx.BOLD:
                            name = '/Helvetica-Bold'
                        else:
                            if weight == Gfx.PLAIN:
                                name = '/Helvetica'
                            else:
                                raise ValueError(verrorStr)
            else:
                raise ValueError("'type' must be 'sans', 'serif' or 'fixed' !")
            self.ps.append(name + ' findfont\n')
            if size == Gfx.SMALL:
                fs = 8.0
            else:
                if size == Gfx.NORMAL:
                    fs = 12.0
                else:
                    if size == Gfx.LARGE:
                        fs = 16.0
                    else:
                        raise ValueError("'size' must be 'small', 'normal' or 'large' !")
            self.ps.append('%f scalefont setfont\n' % fs)

    def getTextSize(self, text):
        if self.fontSize == Gfx.SMALL:
            fs, w = (8, 4)
        else:
            if self.fontSize == Gfx.NORMAL:
                fs, w = (12, 3)
            else:
                if self.fontSize == Gfx.LARGE:
                    fs, w = (16, 3)
        return (
         len(text) * fs * w / 5, fs)

    def clear(self, rgbTuple=(1.0, 1.0, 1.0)):
        self.ps = [
         PS_DOCSTART % (self.resX, self.resY), PS_PAGESTART]
        if rgbTuple != (1.0, 1.0, 1.0):
            w, h = self.getSize()
            saveColor, savePattern = self.color, self.fillPattern
            self.setFillPattern(Gfx.SOLID)
            self.setColor(rgbTuple)
            self.fillRect(0, 0, w - 1, h - 1)
            self.color, self.fillPattern = saveColor, savePattern
        self.setColor(self.color)
        self.setLineWidth(self.lineWidth)
        self.setLinePattern(self.linePattern)
        self.setFillPattern(self.fillPattern)
        self.setFont(self.fontType, self.fontSize, self.fontWeight)

    def drawPoint(self, x, y):
        self.ps.append('newpath\n%d %d moveto\n%d %d lineto\nstroke\n' % (
         x, y, x + 1, y))

    def drawLine(self, x1, y1, x2, y2):
        self.ps.append('newpath\n%d %d moveto\n%d %d lineto\nstroke\n' % (
         x1, y1, x2, y2))

    def drawPoly(self, array):
        if len(array) == 0:
            return
        x, y = array[0]
        self.ps.append('newpath\n%d %d moveto\n' % (x, y))
        for x, y in array:
            self.ps.append('%d %d lineto\n' % (x, y))

        self.ps.append('stroke\n')

    def fillPoly(self, array):
        self.drawPoly(array)
        self.ps[-1] = 'fill\n'

    def writeStr(self, x, y, text, rotationAngle=0.0):
        self.ps.append('%d %d moveto\n' % (x, y))
        if rotationAngle != 0.0:
            self.ps.append('%f rotate\n' % rotationAngle)
        text = re.sub('\\)', '\\)', text)
        text = re.sub('\\(', '\\(', text)
        for k, v in SPECIAL_CHARACTERS.items():
            text = re.sub(k, ') show ' + v + ' glyphshow (', text)

        self.ps.extend(['(', text, ') show\n'])
        if rotationAngle != 0.0:
            self.ps.append('%f rotate\n' % -rotationAngle)


if __name__ == '__main__':
    import systemTest
    systemTest.Test_psGfx()