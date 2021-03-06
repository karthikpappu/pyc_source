# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eevee/dev/camel.git/build/lib/camel/__init__.py
# Compiled at: 2015-10-19 22:59:14
# Size of source mod 2**32: 13179 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import base64, collections, functools
from io import StringIO
import types, yaml
try:
    from yaml import CSafeDumper as SafeDumper
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeDumper
    from yaml import SafeLoader

YAML_TAG_PREFIX = 'tag:yaml.org,2002:'
_str = type('')
_bytes = type(b'')
_long = type(18446744073709551617)

class CamelDumper(SafeDumper):
    __doc__ = "Subclass of yaml's `SafeDumper` that scopes representers to the\n    instance, rather than to the particular class, because damn.\n    "

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('allow_unicode', True)
        super(CamelDumper, self).__init__(*args, **kwargs)
        self.yaml_representers = SafeDumper.yaml_representers.copy()
        self.yaml_multi_representers = SafeDumper.yaml_multi_representers.copy()
        self.add_representer(bytes, CamelDumper.represent_binary)

    def represent_binary(self, data):
        if hasattr(base64, 'encodebytes'):
            data = base64.encodebytes(data).decode('ascii')
        else:
            data = base64.encodestring(data).decode('ascii')
        return self.represent_scalar(YAML_TAG_PREFIX + 'binary', data, style='|')

    def add_representer(self, data_type, representer):
        self.yaml_representers[data_type] = representer

    def add_multi_representer(self, data_type, representer):
        self.yaml_multi_representers[data_type] = representer


class CamelLoader(SafeLoader):
    __doc__ = "Subclass of yaml's `SafeLoader` that scopes constructors to the\n    instance, rather than to the particular class, because damn.\n    "

    def __init__(self, *args, **kwargs):
        super(CamelLoader, self).__init__(*args, **kwargs)
        self.yaml_constructors = SafeLoader.yaml_constructors.copy()
        self.yaml_multi_constructors = SafeLoader.yaml_multi_constructors.copy()
        self.yaml_implicit_resolvers = SafeLoader.yaml_implicit_resolvers.copy()

    def add_constructor(self, data_type, constructor):
        self.yaml_constructors[data_type] = constructor

    def add_multi_constructor(self, data_type, constructor):
        self.yaml_multi_constructors[data_type] = constructor

    def add_implicit_resolver(self, tag, regexp, first):
        if first is None:
            first = [
             None]
        for ch in first:
            self.yaml_implicit_resolvers.setdefault(ch, []).append((tag, regexp))

    def add_path_resolver(self, *args, **kwargs):
        raise NotImplementedError


class Camel(object):

    def __init__(self, registries=()):
        self.registries = (
         STANDARD_TYPES,) + tuple(registries)
        self.version_locks = {}

    def lock_version(self, cls, version):
        self.version_locks[cls] = version

    def make_dumper(self, stream):
        dumper = CamelDumper(stream, default_flow_style=False)
        for registry in self.registries:
            registry.inject_dumpers(dumper, version_locks=self.version_locks)

        return dumper

    def dump(self, data):
        stream = StringIO()
        dumper = self.make_dumper(stream)
        dumper.open()
        dumper.represent(data)
        dumper.close()
        return stream.getvalue()

    def make_loader(self, stream):
        loader = CamelLoader(stream)
        for registry in self.registries:
            registry.inject_loaders(loader)

        return loader

    def load(self, data):
        stream = StringIO(data)
        loader = self.make_loader(stream)
        obj = loader.get_data()
        if loader.check_node():
            raise RuntimeError('Multiple documents found in stream; use load_all')
        return obj

    def load_first(self, data):
        stream = StringIO(data)
        loader = self.make_loader(stream)
        return loader.get_data()

    def load_all(self, data):
        stream = StringIO(data)
        loader = self.make_loader(stream)
        while loader.check_node():
            yield loader.get_data()


class DuplicateVersion(ValueError):
    pass


class CamelRegistry(object):
    frozen = False

    def __init__(self, tag_prefix='!'):
        self.tag_prefix = tag_prefix
        self.dumpers = collections.defaultdict(dict)
        self.loaders = collections.defaultdict(dict)

    def freeze(self):
        self.frozen = True

    def _check_tag(self, tag):
        if self.frozen:
            raise RuntimeError("Can't add to a frozen registry")
        if ';' in tag:
            raise ValueError('Tags may not contain semicolons: {0!r}'.format(tag))

    def dumper(self, cls, tag, version):
        self._check_tag(tag)
        if version in self.dumpers[cls]:
            raise DuplicateVersion
        tag = self.tag_prefix + tag
        if version is None:
            full_tag = tag
        else:
            if isinstance(version, (int, _long)) and version > 0:
                full_tag = '{0};{1}'.format(tag, version)
            else:
                raise TypeError('Expected None or a positive integer version; got {0!r} instead'.format(version))

        def decorator(f):
            self.dumpers[cls][version] = functools.partial(self.run_representer, f, full_tag)
            return f

        return decorator

    def run_representer(self, representer, tag, dumper, data):
        canon_value = representer(data)
        canon_type = type(canon_value)
        if canon_type in (dict, collections.OrderedDict):
            return dumper.represent_mapping(tag, canon_value, flow_style=False)
        if canon_type in (tuple, list):
            return dumper.represent_sequence(tag, canon_value, flow_style=False)
        if canon_type in (int, _long, float, bool, _str, type(None)):
            return dumper.represent_scalar(tag, canon_value)
        raise TypeError('Representers must return native YAML types, but the representer for {!r} returned {!r}, which is of type {!r}'.format(data, canon_value, canon_type))

    def inject_dumpers(self, dumper, version_locks=None):
        if not version_locks:
            version_locks = {}
        for cls, versions in self.dumpers.items():
            version = version_locks.get(cls, max)
            if versions and version is max:
                if None in versions:
                    representer = versions[None]
                else:
                    representer = versions[max(versions)]
            else:
                if version in versions:
                    representer = versions[version]
                else:
                    raise KeyError("Don't know how to dump version {0!r} of type {1!r}".format(version, cls))
            dumper.add_representer(cls, representer)

    def loader(self, tag, version):
        self._check_tag(tag)
        if version in self.loaders[tag]:
            raise DuplicateVersion
        tag = self.tag_prefix + tag

        def decorator(f):
            self.loaders[tag][version] = functools.partial(self.run_constructor, f, version)
            return f

        return decorator

    def run_constructor(self, constructor, version, *yaml_args):
        if len(yaml_args) == 3:
            loader, suffix, node = yaml_args
            version = int(suffix)
        else:
            loader, node = yaml_args
        if isinstance(node, yaml.ScalarNode):
            data = loader.construct_scalar(node)
        else:
            if isinstance(node, yaml.SequenceNode):
                data = loader.construct_sequence(node, deep=True)
            else:
                if isinstance(node, yaml.MappingNode):
                    data = loader.construct_mapping(node, deep=True)
                else:
                    raise TypeError('Not a primitive node: {!r}'.format(node))
        return constructor(data, version)

    def inject_loaders(self, loader):
        for tag, versions in self.loaders.items():
            if all in versions:
                if None in versions:
                    loader.add_constructor(tag, versions[None])
                else:
                    loader.add_constructor(tag, versions[all])
                loader.add_multi_constructor(tag + ';', versions[all])
                continue
                for version, constructor in versions.items():
                    if version is None:
                        loader.add_constructor(tag, constructor)
                    elif version is any:
                        loader.add_multi_constructor(tag + ';', versions[any])
                        if None not in versions:
                            loader.add_constructor(tag, versions[any])
                        else:
                            full_tag = '{0};{1}'.format(tag, version)
                            loader.add_constructor(full_tag, constructor)


STANDARD_TYPES = CamelRegistry(tag_prefix=YAML_TAG_PREFIX)

@STANDARD_TYPES.dumper(frozenset, 'set', version=None)
def _dump_frozenset(data):
    return dict.fromkeys(data)


@STANDARD_TYPES.dumper(collections.OrderedDict, 'omap', version=None)
def _dump_ordered_dict(data):
    pairs = []
    for key, value in data.items():
        pairs.append({key: value})

    return pairs


@STANDARD_TYPES.loader('omap', version=None)
def _load_ordered_dict(data, version):
    return collections.OrderedDict(pair for datum in data for pair, in [datum.items()])


PYTHON_TYPES = CamelRegistry(tag_prefix=YAML_TAG_PREFIX)

@PYTHON_TYPES.dumper(tuple, 'python/tuple', version=None)
def _dump_tuple(data):
    return list(data)


@STANDARD_TYPES.loader('python/tuple', version=None)
def _load_tuple(data, version):
    return tuple(data)


@PYTHON_TYPES.dumper(complex, 'python/complex', version=None)
def _dump_complex(data):
    ret = repr(data)
    if str is bytes:
        ret = ret.decode('ascii')
    if ret[0] == '(' and ret[(-1)] == ')':
        return ret[1:-1]
    else:
        return ret


@STANDARD_TYPES.loader('python/complex', version=None)
def _load_complex(data, version):
    return complex(data)


@PYTHON_TYPES.dumper(frozenset, 'python/frozenset', version=None)
def _dump_frozenset(data):
    try:
        return list(sorted(data))
    except TypeError:
        return list(data)


@STANDARD_TYPES.loader('python/frozenset', version=None)
def _load_frozenset(data, version):
    return frozenset(data)


if hasattr(types, 'SimpleNamespace'):

    @PYTHON_TYPES.dumper(types.SimpleNamespace, 'python/namespace', version=None)
    def _dump_simple_namespace(data):
        return data.__dict__


    @STANDARD_TYPES.loader('python/namespace', version=None)
    def _load_simple_namespace(data, version):
        return types.SimpleNamespace(**data)


STANDARD_TYPES.freeze()
PYTHON_TYPES.freeze()