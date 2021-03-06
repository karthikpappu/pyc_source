# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/conf.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = "\nThe global configuration of a Camelot application is handled through a LazyProxy\nobject that reads settings from various targets.  The default target reads\nthe attributes from the 'settings' module, if this is found on the PYTHONPATH.\n\nTo access the global configuration, simply import the settings object::\n    \n    from camelot.core.conf import settings\n    \n    print settings.CAMELOT_MEDIA_ROOT\n    \nDevelopers can add targets to the settings proxy, to enable reading settings\nfrom other sources.\n"
import logging, os, sys
LOGGER = logging.getLogger('camelot.core.conf')

class LazyProxy(list):
    """A lazy proxy of the 'settings' module on the PYTHONPATH, or other
    targets that contain global configuration.  This proxy behaves as a list
    to which targets can be appended.  The value of the first target in the
    list that has the requested attribute will be returned.
    
    The Proxy is Lazy, because on each request of an attribute, the target
    is queried again.
    """

    def get(self, name, default):
        """Get an attribute of the proxy, and when not found return default
        as value.  This function behaves the same as the get function of a
        dictionary.
        """
        try:
            return getattr(self, name)
        except AttributeError:
            return default

    def __getattr__(self, name):
        if not len(self):
            self.append_settings_module()
        for target in self:
            if hasattr(target, name):
                return getattr(target, name)

        LOGGER.warning('no such settings attribute : %s' % name)
        raise AttributeError()

    def append_settings_module(self):
        """Import the 'settings' module and append it as a target to
        the list of targets.  This function will be called, if no other
        targets are specified"""
        try:
            mod = __import__('settings', {}, {}, [''])
        except ImportError as e:
            raise ImportError, 'Could not import settings (Is it on sys.path? Does it have syntax errors?): %s' % e

        self.append(mod)


settings = LazyProxy()

class SimpleSettings(object):
    """Settings that can be used for the creation of a simple Camelot
    application.  Use these settings by appending them to the global settings
    at application startup::
    
        from camelot.core.conf import settings, SimpleSettings
        
        settings.append( SimpleSettings('myapp') )
    """

    def __init__(self, author, name, data='data.sqlite'):
        """
        :param author: the name of the writer of the application
        :param name: the name of the application
        :param data: the name of the sqlite database file
        
        These names will be used to create a folder where the local data will 
        be stored.  On Windows this will be in the AppData folder of the user,
        otherwise it will be in a `.author` folder in the home directory of the
        user.
        """
        self.data = data
        if 'win' in sys.platform and 'darwin' not in sys.platform:
            import winpaths
            self._local_folder = os.path.join(winpaths.get_local_appdata(), author, name)
        else:
            self._local_folder = os.path.join(os.path.expanduser('~'), '.%s' % author, name)
        if not os.path.exists(self._local_folder):
            os.makedirs(self._local_folder)
        LOGGER.info('store database and media in %s' % self._local_folder)

    def CAMELOT_MEDIA_ROOT(self):
        return os.path.join(self._local_folder, 'media')

    def ENGINE(self):
        from sqlalchemy import create_engine
        return create_engine('sqlite:///%s/%s' % (self._local_folder,
         self.data))