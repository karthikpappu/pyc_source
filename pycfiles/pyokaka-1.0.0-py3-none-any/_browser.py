# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\js\dojo\_browser.py
# Compiled at: 2013-05-30 06:32:18
__doc__ = ' Client browser utilities.\n\n\n\n'
from _base import Dojo

class window(Dojo):
    """ Functions related to the viewport.
    """
    require = [
     'dojo/window']

    def getBox(self):
        pass

    def get(self):
        pass

    def scrollIntoView(self):
        pass


class cookie(Dojo):
    """ Handling client side cookies.
    """
    require = [
     'dojo/cookie']


class has(Dojo):
    """ Provides standardized feature detection.
    """
    require = [
     'dojo/has']


class sniff(Dojo):
    """ Browser feature detection.
    """
    require = [
     'dojo/sniff']


class back(Dojo):
    u""" Allows you to update the browser history, so that it’s possible to 
    use the Back and Forward buttons.
    """
    require = [
     'dojo/back']

    def init(self):
        pass

    def addToHistory(self):
        pass


class hash(Dojo):
    """ Aprovides methods for monitoring and updating the hash (history) 
    in the browser URL.
    """
    require = [
     'dojo/back']


class colors(Dojo):
    """ Augments the base dojo/_base/Color class with additional methods and 
    named colors.
    """
    require = [
     'dojo/colors']


class hccss(Dojo):
    u""" Provides “High Contrast” feature detection for accessibility purposes.
    """
    require = [
     'dojo/hccss']