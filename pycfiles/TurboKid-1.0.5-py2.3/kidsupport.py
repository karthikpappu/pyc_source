# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbokid\kidsupport.py
# Compiled at: 2010-01-25 14:33:01
"""Template support for Kid"""
import sys
from os import stat
from itertools import count
from threading import RLock
from logging import getLogger
from pkg_resources import resource_filename
import kid
log = getLogger('turbokid.kidsupport')

def _compile_template(package, basename, tfile, classname):
    mod = kid.load_template(tfile, name=classname)
    setattr(sys.modules[package], basename, mod)
    return mod


def _get_extended_modules(template):
    """Recursively builds and returns a list containing all modules
    of the templates extended from the template passed as parameter."""
    excluded_modules = [
     '__builtin__', 'kid']
    modules_list = []
    for base_template in template.__bases__:
        if base_template.__module__ not in excluded_modules:
            modules_list.append(base_template.__module__)
        if hasattr(base_template, '__bases__'):
            modules_list.extend(_get_extended_modules(base_template))

    return modules_list


class KidSupport(object):
    __module__ = __name__
    extension = '.kid'
    assume_encoding = encoding = 'utf-8'
    precompiled = False
    string_template_serial = count()

    def __init__(self, extra_vars_func=None, options=None):
        if options is None:
            options = dict()
        self.options = options
        self.get_extra_vars = extra_vars_func
        self.assume_encoding = options.get('kid.assume_encoding', KidSupport.assume_encoding)
        self.encoding = options.get('kid.encoding', KidSupport.encoding)
        self.precompiled = options.get('kid.precompiled', KidSupport.precompiled)
        if not self.precompiled:
            self.compile_lock = RLock()
        self.serializer = kid.HTMLSerializer(encoding=self.encoding)
        self.sitetemplate = None
        self.stname = options.get('kid.sitetemplate', None)
        if options.get('kid.i18n.run_template_filter', False):
            template_filter = options.get('kid.i18n_filter')
            if not callable(template_filter):
                template_filter = None
        else:
            template_filter = None
        self.filter = template_filter
        self.compiled_templates = {}
        return

    def load_template_string(self, template_string):
        if not isinstance(template_string, basestring):
            raise ValueError('You must pass a template string')
        serial = self.string_template_serial.next()
        tempclass = kid.load_template(template_string, name='KidTemplateFromString-%d' % serial).Template
        tempclass.serializer = self.serializer
        return tempclass

    def load_template(self, classname=None, template_string=None, loadingSite=False):
        """Searches for a template along the Python path.

        Template files must end in ".kid" and be in legitimate packages.
        If the templates are precompiled to ".pyc" files, you can set the
        "kid.precompiled" option to just do a straight import of the template.

        """
        if template_string is not None:
            return self.load_template_string(template_string)
        elif classname is None:
            raise ValueError('You must pass at least a classsname or template_string as parameters')
        if not loadingSite:
            if self.stname and (not self.sitetemplate or self.stname not in sys.modules):
                self.load_template(self.stname, loadingSite=True)
                sys.modules['sitetemplate'] = sys.modules[self.stname]
                self.sitetemplate = sys.modules['sitetemplate']
        lastdot = classname.rfind('.')
        if lastdot < 0:
            raise ValueError('All Kid templates must be in a package')
        (package, basename) = (
         classname[:lastdot], classname[lastdot + 1:])
        if self.precompiled:
            mod = __import__(classname, dict(), dict(), [basename])
        else:
            tfile = resource_filename(package, basename + self.extension)
            ct = self.compiled_templates
            self.compile_lock.acquire()
            try:
                if classname in sys.modules and classname in ct:
                    tclass = sys.modules[classname].Template
                    ttime = ct[classname]
                    mtime = stat(sys.modules[classname].__file__).st_mtime
                    reload_modules = mtime > ttime
                    if reload_modules:
                        ttime = mtime
                    for module in _get_extended_modules(tclass):
                        ctime = ct.get(module)
                        try:
                            mtime = stat(sys.modules[module].__file__).st_mtime
                        except KeyError:
                            if ctime is None:
                                mtime = ttime
                            else:
                                mtime = ctime

                        if ctime is None or mtime > ctime:
                            reload_modules = True
                        if mtime > ttime:
                            reload_template = True
                            ttime = mtime

                    if reload_modules:
                        log.debug('Recompiling template for %s' % classname)
                        temp_name = kid.importer.get_template_name(None, tfile)
                        if temp_name != classname and temp_name in sys.modules:
                            sys.modules[temp_name] = kid.load_template(tfile, temp_name)
                        del sys.modules[classname]
                        ct[classname] = ttime
                        mod = _compile_template(package, basename, tfile, classname)
                    else:
                        mod = __import__(classname, dict(), dict(), [basename])
                else:
                    log.debug('Compiling template for %s' % classname)
                    mod = _compile_template(package, basename, tfile, classname)
                    tclass = mod.Template
                    ttime = stat(sys.modules[classname].__file__).st_mtime
                    for module in _get_extended_modules(tclass):
                        mtime = stat(sys.modules[module].__file__).st_mtime
                        ct[module] = mtime
                        if mtime > ttime:
                            ttime = mtime

                    ct[classname] = ttime
            finally:
                self.compile_lock.release()
        tempclass = mod.Template
        tempclass.serializer = self.serializer
        return tempclass
        return

    def render(self, info, format='html', fragment=False, template=None):
        """Renders data in the desired format.

        @param info: the data itself
        @type info: dict
        @param format: Kid output method and format, separated by whitespace
        @type format: string
        @param fragment: passed through to tell the template if only a
                         fragment of a page is desired
        @type fragment: bool
        @param template: the name of the template to use
        @type template: string
        """
        if isinstance(template, type):
            tclass = template
        else:
            tclass = self.load_template(template)
        log.debug('Applying template %s' % tclass.__module__)
        data = dict()
        if self.get_extra_vars:
            data.update(self.get_extra_vars())
        if info:
            data.update(info)
        template = tclass(**data)
        if self.assume_encoding:
            template.assume_encoding = self.assume_encoding
        if self.filter and self.filter not in template._filters:
            template._filters.append(self.filter)
        if isinstance(format, str):
            if format.endswith('-straight'):
                format = (format[:-9], format[-8:])
            else:
                format = format.split()
        elif not isinstance(format, (tuple, list)):
            format = (
             format,)
        if len(format) < 2:
            (output, format) = (
             format[0], None)
        else:
            (output, format) = format[:2]
        return template.serialize(encoding=self.encoding, fragment=fragment, output=output, format=format)
        return

    def transform(self, info, template):
        if isinstance(template, type):
            tclass = template
        else:
            tclass = self.load_template(template)
        data = dict()
        if self.get_extra_vars:
            data.update(self.get_extra_vars())
        data.update(info)
        template = tclass(**data)
        if self.filter and self.filter not in template._filters:
            template._filters.append(self.filter)
        return kid.ElementStream(template.transform()).expand()