# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/loader.py
# Compiled at: 2020-04-15 09:53:56
# Size of source mod 2**32: 3493 bytes
__doc__ = '\nModule that contains Artella loader implementation for Plot Twist\n'
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os, inspect, logging.config

def init(do_reload=False, import_libs=True, dev=False):
    """
    Initializes Plot Twist library
    """
    if not dev:
        import sentry_sdk
        try:
            sentry_sdk.init('https://d71a4ba272374d7fb845269bb2aebf37@sentry.io/1816355')
        except (RuntimeError, ImportError):
            sentry_sdk.init('https://d71a4ba272374d7fb845269bb2aebf37@sentry.io/1816355', default_integrations=False)

    else:
        from tpDcc.libs.python import importer
        from plottwist import register
        logger = create_logger()
        register.register_class('logger', logger)

        class PlotTwistCore(importer.Importer):

            def __init__(self, debug=False):
                super(PlotTwistCore, self).__init__(module_name='plottwist', debug=debug)

            def get_module_path(self):
                """
            Returns path where plot twist core module is stored
            :return: str
            """
                try:
                    mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
                except Exception:
                    try:
                        mod_dir = os.path.dirname(__file__)
                    except Exception:
                        try:
                            import plottwist
                            mod_dir = plottwist.__path__[0]
                        except Exception:
                            return

                return mod_dir

        packages_order = [
         'plottwist.core']
        if import_libs:
            import artellapipe.loader
            artellapipe.loader.init(do_reload=do_reload, import_libs=True, dev=dev)
        from plottwist.core import project
        plottwist_core_importer = importer.init_importer(importer_class=PlotTwistCore, do_reload=False, debug=dev)
        plottwist_core_importer.import_packages(only_packages=False,
          order=packages_order,
          skip_modules=[
         'plottwist.bootstrap'])
        if do_reload:
            plottwist_core_importer.reload_all()
    import artellapipe.loader
    artellapipe.loader.set_project((project.PlotTwist), do_reload=do_reload)


def create_logger():
    """
    Returns logger of current module
    """
    logging.config.fileConfig((get_logging_config()), disable_existing_loggers=False)
    logger = logging.getLogger('plottwist')
    return logger


def create_logger_directory():
    """
    Creates artellapipe logger directory
    """
    artellapipe_logger_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'plottwist', 'logs'))
    if not os.path.isdir(artellapipe_logger_dir):
        os.makedirs(artellapipe_logger_dir)


def get_logging_config():
    """
    Returns logging configuration file path
    :return: str
    """
    create_logger_directory()
    return os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))


def get_logging_level():
    """
    Returns logging level to use
    :return: str
    """
    if os.environ.get('PLOTTWIST_LOG_LEVEL', None):
        return os.environ.get('PLOTTWIST_LOG_LEVEL')
    else:
        return os.environ.get('PLOTTWIST_LOG_LEVEL', 'WARNING')