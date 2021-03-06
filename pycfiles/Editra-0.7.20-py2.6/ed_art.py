# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_art.py
# Compiled at: 2011-01-31 18:30:59
"""
Provides and ArtProvider class that works off of object ID's to return an
associated art resource. The provider works hand in hand with Editra's theme
framework that allows for themes to be provided as plugins that act as the
resource providers for the ArtProvider.

@summary: Editra's ArtProvider, supplies icons based off of object ids

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__cvsid__ = '$Id: ed_art.py 66815 2011-01-29 20:46:20Z CJP $'
__revision__ = '$Revision: 66815 $'
import wx, ed_glob
from profiler import Profile_Get
import syntax.syntax, ed_theme
DEFAULT = {ed_glob.ID_ADD_BM: wx.ART_ADD_BOOKMARK, 
   ed_glob.ID_BIN_FILE: wx.ART_EXECUTABLE_FILE, 
   ed_glob.ID_CDROM: wx.ART_CDROM, 
   ed_glob.ID_COPY: wx.ART_COPY, 
   ed_glob.ID_CUT: wx.ART_CUT, 
   ed_glob.ID_DELETE: wx.ART_DELETE, 
   ed_glob.ID_DEL_BM: wx.ART_DEL_BOOKMARK, 
   ed_glob.ID_DOWN: wx.ART_GO_DOWN, 
   ed_glob.ID_EXIT: wx.ART_QUIT, 
   ed_glob.ID_FILE: wx.ART_NORMAL_FILE, 
   ed_glob.ID_FIND: wx.ART_FIND, 
   ed_glob.ID_FIND_REPLACE: wx.ART_FIND_AND_REPLACE, 
   ed_glob.ID_FLOPPY: wx.ART_FLOPPY, 
   ed_glob.ID_FOLDER: wx.ART_FOLDER, 
   ed_glob.ID_HARDDISK: wx.ART_HARDDISK, 
   ed_glob.ID_NEW: wx.ART_NEW, 
   ed_glob.ID_NEXT_MARK: wx.ART_GO_FORWARD, 
   ed_glob.ID_OPEN: wx.ART_FILE_OPEN, 
   ed_glob.ID_PASTE: wx.ART_PASTE, 
   ed_glob.ID_PRE_MARK: wx.ART_GO_BACK, 
   ed_glob.ID_PRINT: wx.ART_PRINT, 
   ed_glob.ID_REDO: wx.ART_REDO, 
   ed_glob.ID_SAVE: wx.ART_FILE_SAVE, 
   ed_glob.ID_SAVEAS: wx.ART_FILE_SAVE_AS, 
   ed_glob.ID_STOP: wx.ART_ERROR, 
   ed_glob.ID_UNDO: wx.ART_UNDO, 
   ed_glob.ID_UP: wx.ART_GO_UP, 
   ed_glob.ID_USB: wx.ART_REMOVABLE}

class EditraArt(wx.ArtProvider):
    """Editras Art Provider. Provides the mimetype images and loads any custom
    user defined icon sets as well. Editra theme specific icons are looked up
    by passing an objects related id as a string to this providers CreateBitmap
    function for it to talk to the theme resource provider. If the id is not
    a defined object ID it is simply ignored or passed to the the next
    ArtProvider in the chain to handle.

    """

    def __init__(self):
        """Initializes Editra's art provider"""
        super(EditraArt, self).__init__()
        self._library = ed_theme.BitmapProvider(wx.GetApp().GetPluginManager())

    def CreateBitmap(self, art_id, client, size):
        """Lookup and return an associated bitmap from the current theme if
        one exisists. If the art_id is not a theme defined id and is a wx
        defined art resource then it is passed to the next ArtProvider in the
        stack to evaluate.

        @return: Requested bitmap from current theme if one exists
        @rtype: wx.Bitmap

        """
        try:
            art_id = int(art_id)
        except ValueError:
            return wx.NullBitmap
        else:
            if Profile_Get('ICONS', 'str').lower() == 'default' and art_id in DEFAULT:
                if client == wx.ART_MENU:
                    size = (16, 16)
                elif client == wx.ART_TOOLBAR:
                    size = Profile_Get('ICON_SZ', default=(24, 24))
                return wx.ArtProvider.GetBitmap(DEFAULT[art_id], client, size)
            bmp = self._library.GetBitmap(art_id, client)
            if not bmp.IsNull() and bmp.IsOk():
                if client == wx.ART_TOOLBAR and not wx.Platform == '__WXMAC__':
                    if size == wx.DefaultSize:
                        size = Profile_Get('ICON_SZ', default=(24, 24))
                    img_sz = bmp.GetSize()
                    if size[0] < img_sz[0]:
                        img = wx.ImageFromBitmap(bmp)
                        img.Rescale(size[0], size[1], wx.IMAGE_QUALITY_HIGH)
                        bmp = wx.BitmapFromImage(img)
                elif client == wx.ART_MENU and bmp.GetSize() != (16, 16):
                    img = wx.ImageFromBitmap(bmp)
                    img.Rescale(16, 16, wx.IMAGE_QUALITY_HIGH)
                    bmp = wx.BitmapFromImage(img)
            elif client == wx.ART_TOOLBAR:
                bmp = wx.ArtProvider.GetBitmap(wx.ART_WARNING, client, size)
            elif art_id in syntax.SYNTAX_IDS:
                bmp = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_MENU, (16,
                                                                                 16))

        if bmp.IsOk() and not bmp.IsNull():
            return bmp
        return wx.NullBitmap