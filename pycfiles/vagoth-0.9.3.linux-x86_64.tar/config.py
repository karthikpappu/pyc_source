# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vagoth/config.py
# Compiled at: 2013-02-09 06:55:48


def get_config(config_searchpaths):
    """
    Given a list of config searchpaths, instantiate the config object for
    the first path, or instantiate an empty config object.  This uses
    the configobj library to load the config.
    """
    from configobj import ConfigObj
    import os.path
    for path in config_searchpaths:
        path = os.path.expanduser(path)
        if os.path.exists(path):
            return ConfigObj(path)

    return ConfigObj()


def dynamic_lookup(moduleColonName):
    """
    Dynamically lookup an object in a module, given input of the form
    modulename:objectname
    """
    modulestr, name = moduleColonName.split(':')
    try:
        module = __import__(modulestr, fromlist=[name])
    except ImportError:
        raise ImportError('Could not import module: %s' % (modulestr,))

    try:
        return getattr(module, name)
    except AttributeError:
        raise AttributeError('Could not load %s from module %s' % (name, modulestr))


_static_config = None

class Config(object):
    """
    Config is a wrapper class around the real config object,
    supplying methods to return or instantate class factories
    found in the configuration.
    """

    def __init__(self, config_searchpaths=None):
        global _static_config
        if _static_config != None:
            self.config = _static_config
        else:
            searchpath = config_searchpaths or ['~/.config/sippe/vagoth.conf', '/etc/sippe/vagoth.conf']
            _static_config = self.config = get_config(searchpath)
        return

    def __getitem__(self, key):
        return self.config[key]

    def _lookup_config_section(self, config_path):
        current = self.config
        try:
            for part in config_path.split('/'):
                current = current[part]

            return current
        except KeyError:
            raise KeyError('Could not locate %s in config file' % (config_path,))

    def get_factory(self, section, factory_key='factory'):
        """Return a tuple for a factory and its configuration dict"""
        config = self._lookup_config_section(section)
        factory_str = config[factory_key]
        return (dynamic_lookup(factory_str), config)

    def make_factory(self, section, context, factory_key='factory'):
        """
        Instantate a factory, passing in a context object and the section
        config to the initialiser.
        """
        factory_class, factory_config = self.get_factory(section, factory_key)
        return factory_class(context, factory_config)

    def get_node_factory(self, node_type):
        """
        Return the class for a given node type
        """
        node_types = self.config['node_types']
        if node_type in node_types:
            return dynamic_lookup(node_types[node_type])

    def get_action(self, action):
        """
        Return the named action callable
        """
        actions = self.config['actions']
        if action in actions:
            return dynamic_lookup(actions[action])