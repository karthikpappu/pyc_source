# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/lazymodule.py
# Compiled at: 2016-07-03 23:28:12
""" 
Defines the LazyModule class which will delay loading of a python module until
it is accessed the first time.

doing:

scoped_name = LazyModule('package_name.module_name')

is equivalent as doing:

from package_name import module_name as scoped_name

Only the module will not actually load itself until the first time a value
is attempted to pull from the module.  Once loaded, it will be able to be
used like a standard python module.  This is very useful when dealing with
slow loading modules and import cycles.

"""
import logging, os, sys
log = logging.getLogger(__name__)

class LazyModule(object):

    def __dir__(self):
        mod = self.__load_module__()
        return dir(mod)

    def __getattr__(self, key):
        """
        Retrieves the value from the module wrapped by this instance.
        
        :param      key | <str>
        
        :return     <variant>
        """
        mod = self.__load_module__()
        if os.environ.get('DOX_MODE') == '1':
            return getattr(mod, key, object)
        else:
            return getattr(mod, key)

    def __setattr__(self, key, value):
        """
        Sets the value within the module wrapped by this instance to the
        inputted value.
        
        :param      key | <str>
                    value | <variant>
        """
        mod = self.__load_module__()
        return setattr(mod, key, value)

    def __init__(self, module_name):
        self.__dict__['__module_name__'] = module_name

    def __load_module__(self):
        try:
            return self.__dict__['__module_inst__']
        except KeyError:
            mod_name = self.__dict__['__module_name__']
            try:
                self.__dict__['__module_inst__'] = sys.modules[mod_name]
                return self.__dict__['__module_inst__']
            except KeyError:
                if os.environ.get('DOX_MODE') == '1':
                    try:
                        __import__(mod_name)
                        mod = sys.modules.get(mod_name)
                    except ImportError as err:
                        mod = None

                else:
                    __import__(mod_name)
                    mod = sys.modules.get(mod_name)
                self.__dict__['__module_inst__'] = mod
                return mod

        return


lazy_import = LazyModule