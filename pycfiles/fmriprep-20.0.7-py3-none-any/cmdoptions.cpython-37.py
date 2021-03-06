# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_internal/cli/cmdoptions.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 28403 bytes
"""
shared options and groups

The principle here is to define options once, but *not* instantiate them
globally. One reason being that options with action='append' can carry state
between parses. pip parses general options twice internally, and shouldn't
pass on state. To be consistent, all options will follow this design.
"""
from __future__ import absolute_import
import logging, os, textwrap, warnings
from distutils.util import strtobool
from functools import partial
from optparse import SUPPRESS_HELP, Option, OptionGroup
from textwrap import dedent
from pip._internal.cli.progress_bars import BAR_TYPES
from pip._internal.exceptions import CommandError
from pip._internal.locations import USER_CACHE_DIR, get_src_prefix
from pip._internal.models.format_control import FormatControl
from pip._internal.models.index import PyPI
from pip._internal.models.target_python import TargetPython
from pip._internal.utils.hashes import STRONG_HASHES
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Any, Callable, Dict, Optional, Tuple
    from optparse import OptionParser, Values
    from pip._internal.cli.parser import ConfigOptionParser
logger = logging.getLogger(__name__)

def raise_option_error(parser, option, msg):
    """
    Raise an option parsing error using parser.error().

    Args:
      parser: an OptionParser instance.
      option: an Option instance.
      msg: the error text.
    """
    msg = '{} error: {}'.format(option, msg)
    msg = textwrap.fill(' '.join(msg.split()))
    parser.error(msg)


def make_option_group(group, parser):
    """
    Return an OptionGroup object
    group  -- assumed to be dict with 'name' and 'options' keys
    parser -- an optparse Parser
    """
    option_group = OptionGroup(parser, group['name'])
    for option in group['options']:
        option_group.add_option(option())

    return option_group


def check_install_build_global(options, check_options=None):
    """Disable wheels if per-setup.py call options are set.

    :param options: The OptionParser options to update.
    :param check_options: The options to check, if not supplied defaults to
        options.
    """
    if check_options is None:
        check_options = options

    def getname(n):
        return getattr(check_options, n, None)

    names = ['build_options', 'global_options', 'install_options']
    if any(map(getname, names)):
        control = options.format_control
        control.disallow_binaries()
        warnings.warn('Disabling all use of wheels due to the use of --build-option / --global-option / --install-option.',
          stacklevel=2)


def check_dist_restriction(options, check_target=False):
    """Function for determining if custom platform options are allowed.

    :param options: The OptionParser options.
    :param check_target: Whether or not to check if --target is being used.
    """
    dist_restriction_set = any([
     options.python_version,
     options.platform,
     options.abi,
     options.implementation])
    binary_only = FormatControl(set(), {':all:'})
    sdist_dependencies_allowed = options.format_control != binary_only and not options.ignore_dependencies
    if dist_restriction_set:
        if sdist_dependencies_allowed:
            raise CommandError('When restricting platform and interpreter constraints using --python-version, --platform, --abi, or --implementation, either --no-deps must be set, or --only-binary=:all: must be set and --no-binary must not be set (or must be set to :none:).')
    if check_target:
        if dist_restriction_set:
            if not options.target_dir:
                raise CommandError("Can not use any platform or abi specific options unless installing via '--target'")


def _path_option_check(option, opt, value):
    return os.path.expanduser(value)


class PipOption(Option):
    TYPES = Option.TYPES + ('path', )
    TYPE_CHECKER = Option.TYPE_CHECKER.copy()
    TYPE_CHECKER['path'] = _path_option_check


help_ = partial(Option,
  '-h',
  '--help', dest='help',
  action='help',
  help='Show help.')
isolated_mode = partial(Option,
  '--isolated',
  dest='isolated_mode',
  action='store_true',
  default=False,
  help='Run pip in an isolated mode, ignoring environment variables and user configuration.')
require_virtualenv = partial(Option,
  '--require-virtualenv',
  '--require-venv', dest='require_venv',
  action='store_true',
  default=False,
  help=SUPPRESS_HELP)
verbose = partial(Option,
  '-v',
  '--verbose', dest='verbose',
  action='count',
  default=0,
  help='Give more output. Option is additive, and can be used up to 3 times.')
no_color = partial(Option,
  '--no-color',
  dest='no_color',
  action='store_true',
  default=False,
  help='Suppress colored output')
version = partial(Option,
  '-V',
  '--version', dest='version',
  action='store_true',
  help='Show version and exit.')
quiet = partial(Option,
  '-q',
  '--quiet', dest='quiet',
  action='count',
  default=0,
  help='Give less output. Option is additive, and can be used up to 3 times (corresponding to WARNING, ERROR, and CRITICAL logging levels).')
progress_bar = partial(Option,
  '--progress-bar',
  dest='progress_bar',
  type='choice',
  choices=(list(BAR_TYPES.keys())),
  default='on',
  help=('Specify type of progress to be displayed [' + '|'.join(BAR_TYPES.keys()) + '] (default: %default)'))
log = partial(PipOption,
  '--log',
  '--log-file', '--local-log', dest='log',
  metavar='path',
  type='path',
  help='Path to a verbose appending log.')
no_input = partial(Option,
  '--no-input',
  dest='no_input',
  action='store_true',
  default=False,
  help=SUPPRESS_HELP)
proxy = partial(Option,
  '--proxy',
  dest='proxy',
  type='str',
  default='',
  help='Specify a proxy in the form [user:passwd@]proxy.server:port.')
retries = partial(Option,
  '--retries',
  dest='retries',
  type='int',
  default=5,
  help='Maximum number of retries each connection should attempt (default %default times).')
timeout = partial(Option,
  '--timeout',
  '--default-timeout', metavar='sec',
  dest='timeout',
  type='float',
  default=15,
  help='Set the socket timeout (default %default seconds).')

def exists_action():
    return Option('--exists-action',
      dest='exists_action',
      type='choice',
      choices=[
     's', 'i', 'w', 'b', 'a'],
      default=[],
      action='append',
      metavar='action',
      help='Default action when a path already exists: (s)witch, (i)gnore, (w)ipe, (b)ackup, (a)bort.')


cert = partial(PipOption,
  '--cert',
  dest='cert',
  type='path',
  metavar='path',
  help='Path to alternate CA bundle.')
client_cert = partial(PipOption,
  '--client-cert',
  dest='client_cert',
  type='path',
  default=None,
  metavar='path',
  help='Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.')
index_url = partial(Option,
  '-i',
  '--index-url', '--pypi-url', dest='index_url',
  metavar='URL',
  default=(PyPI.simple_url),
  help='Base URL of the Python Package Index (default %default). This should point to a repository compliant with PEP 503 (the simple repository API) or a local directory laid out in the same format.')

def extra_index_url():
    return Option('--extra-index-url',
      dest='extra_index_urls',
      metavar='URL',
      action='append',
      default=[],
      help='Extra URLs of package indexes to use in addition to --index-url. Should follow the same rules as --index-url.')


no_index = partial(Option,
  '--no-index',
  dest='no_index',
  action='store_true',
  default=False,
  help='Ignore package index (only looking at --find-links URLs instead).')

def find_links():
    return Option('-f',
      '--find-links', dest='find_links',
      action='append',
      default=[],
      metavar='url',
      help="If a URL or path to an html file, then parse for links to archives such as sdist (.tar.gz) or wheel (.whl) files. If a local path or file:// URL that's a directory,  then look for archives in the directory listing. Links to VCS project URLs are not supported.")


def trusted_host():
    return Option('--trusted-host',
      dest='trusted_hosts',
      action='append',
      metavar='HOSTNAME',
      default=[],
      help='Mark this host or host:port pair as trusted, even though it does not have valid or any HTTPS.')


def constraints():
    return Option('-c',
      '--constraint', dest='constraints',
      action='append',
      default=[],
      metavar='file',
      help='Constrain versions using the given constraints file. This option can be used multiple times.')


def requirements():
    return Option('-r',
      '--requirement', dest='requirements',
      action='append',
      default=[],
      metavar='file',
      help='Install from the given requirements file. This option can be used multiple times.')


def editable():
    return Option('-e',
      '--editable', dest='editables',
      action='append',
      default=[],
      metavar='path/url',
      help='Install a project in editable mode (i.e. setuptools "develop mode") from a local project path or a VCS url.')


def _handle_src(option, opt_str, value, parser):
    value = os.path.abspath(value)
    setattr(parser.values, option.dest, value)


src = partial(PipOption,
  '--src',
  '--source', '--source-dir', '--source-directory', dest='src_dir',
  type='path',
  metavar='dir',
  default=(get_src_prefix()),
  action='callback',
  callback=_handle_src,
  help='Directory to check out editable projects into. The default in a virtualenv is "<venv path>/src". The default for global installs is "<current dir>/src".')

def _get_format_control(values, option):
    """Get a format_control object."""
    return getattr(values, option.dest)


def _handle_no_binary(option, opt_str, value, parser):
    existing = _get_format_control(parser.values, option)
    FormatControl.handle_mutual_excludes(value, existing.no_binary, existing.only_binary)


def _handle_only_binary(option, opt_str, value, parser):
    existing = _get_format_control(parser.values, option)
    FormatControl.handle_mutual_excludes(value, existing.only_binary, existing.no_binary)


def no_binary():
    format_control = FormatControl(set(), set())
    return Option('--no-binary',
      dest='format_control', action='callback', callback=_handle_no_binary,
      type='str',
      default=format_control,
      help='Do not use binary packages. Can be supplied multiple times, and each time adds to the existing value. Accepts either ":all:" to disable all binary packages, ":none:" to empty the set (notice the colons), or one or more package names with commas between them (no colons). Note that some packages are tricky to compile and may fail to install when this option is used on them.')


def only_binary():
    format_control = FormatControl(set(), set())
    return Option('--only-binary',
      dest='format_control', action='callback', callback=_handle_only_binary,
      type='str',
      default=format_control,
      help='Do not use source packages. Can be supplied multiple times, and each time adds to the existing value. Accepts either ":all:" to disable all source packages, ":none:" to empty the set, or one or more package names with commas between them. Packages without binary distributions will fail to install when this option is used on them.')


platform = partial(Option,
  '--platform',
  dest='platform',
  metavar='platform',
  default=None,
  help='Only use wheels compatible with <platform>. Defaults to the platform of the running system.')

def _convert_python_version(value):
    """
    Convert a version string like "3", "37", or "3.7.3" into a tuple of ints.

    :return: A 2-tuple (version_info, error_msg), where `error_msg` is
        non-None if and only if there was a parsing error.
    """
    if not value:
        return (None, None)
    else:
        parts = value.split('.')
        if len(parts) > 3:
            return ((), 'at most three version parts are allowed')
        if len(parts) == 1:
            value = parts[0]
            if len(value) > 1:
                parts = [
                 value[0], value[1:]]
    try:
        version_info = tuple((int(part) for part in parts))
    except ValueError:
        return ((), 'each version part must be an integer')
    else:
        return (
         version_info, None)


def _handle_python_version(option, opt_str, value, parser):
    """
    Handle a provided --python-version value.
    """
    version_info, error_msg = _convert_python_version(value)
    if error_msg is not None:
        msg = 'invalid --python-version value: {!r}: {}'.format(value, error_msg)
        raise_option_error(parser, option=option, msg=msg)
    parser.values.python_version = version_info


python_version = partial(Option,
  '--python-version',
  dest='python_version',
  metavar='python_version',
  action='callback',
  callback=_handle_python_version,
  type='str',
  default=None,
  help=(dedent('    The Python interpreter version to use for wheel and "Requires-Python"\n    compatibility checks. Defaults to a version derived from the running\n    interpreter. The version can be specified using up to three dot-separated\n    integers (e.g. "3" for 3.0.0, "3.7" for 3.7.0, or "3.7.3"). A major-minor\n    version can also be given as a string without dots (e.g. "37" for 3.7.0).\n    ')))
implementation = partial(Option,
  '--implementation',
  dest='implementation',
  metavar='implementation',
  default=None,
  help="Only use wheels compatible with Python implementation <implementation>, e.g. 'pp', 'jy', 'cp',  or 'ip'. If not specified, then the current interpreter implementation is used.  Use 'py' to force implementation-agnostic wheels.")
abi = partial(Option,
  '--abi',
  dest='abi',
  metavar='abi',
  default=None,
  help="Only use wheels compatible with Python abi <abi>, e.g. 'pypy_41'.  If not specified, then the current interpreter abi tag is used.  Generally you will need to specify --implementation, --platform, and --python-version when using this option.")

def add_target_python_options(cmd_opts):
    cmd_opts.add_option(platform())
    cmd_opts.add_option(python_version())
    cmd_opts.add_option(implementation())
    cmd_opts.add_option(abi())


def make_target_python(options):
    target_python = TargetPython(platform=(options.platform),
      py_version_info=(options.python_version),
      abi=(options.abi),
      implementation=(options.implementation))
    return target_python


def prefer_binary():
    return Option('--prefer-binary',
      dest='prefer_binary',
      action='store_true',
      default=False,
      help='Prefer older binary packages over newer source packages.')


cache_dir = partial(PipOption,
  '--cache-dir',
  dest='cache_dir',
  default=USER_CACHE_DIR,
  metavar='dir',
  type='path',
  help='Store the cache data in <dir>.')

def _handle_no_cache_dir(option, opt, value, parser):
    """
    Process a value provided for the --no-cache-dir option.

    This is an optparse.Option callback for the --no-cache-dir option.
    """
    if value is not None:
        try:
            strtobool(value)
        except ValueError as exc:
            try:
                raise_option_error(parser, option=option, msg=(str(exc)))
            finally:
                exc = None
                del exc

    parser.values.cache_dir = False


no_cache = partial(Option,
  '--no-cache-dir',
  dest='cache_dir',
  action='callback',
  callback=_handle_no_cache_dir,
  help='Disable the cache.')
no_deps = partial(Option,
  '--no-deps',
  '--no-dependencies', dest='ignore_dependencies',
  action='store_true',
  default=False,
  help="Don't install package dependencies.")

def _handle_build_dir(option, opt, value, parser):
    if value:
        value = os.path.abspath(value)
    setattr(parser.values, option.dest, value)


build_dir = partial(PipOption,
  '-b',
  '--build', '--build-dir', '--build-directory', dest='build_dir',
  type='path',
  metavar='dir',
  action='callback',
  callback=_handle_build_dir,
  help='Directory to unpack packages into and build in. Note that an initial build still takes place in a temporary directory. The location of temporary directories can be controlled by setting the TMPDIR environment variable (TEMP on Windows) appropriately. When passed, build directories are not cleaned in case of failures.')
ignore_requires_python = partial(Option,
  '--ignore-requires-python',
  dest='ignore_requires_python',
  action='store_true',
  help='Ignore the Requires-Python information.')
no_build_isolation = partial(Option,
  '--no-build-isolation',
  dest='build_isolation',
  action='store_false',
  default=True,
  help='Disable isolation when building a modern source distribution. Build dependencies specified by PEP 518 must be already installed if this option is used.')

def _handle_no_use_pep517(option, opt, value, parser):
    """
    Process a value provided for the --no-use-pep517 option.

    This is an optparse.Option callback for the no_use_pep517 option.
    """
    if value is not None:
        msg = 'A value was passed for --no-use-pep517,\n        probably using either the PIP_NO_USE_PEP517 environment variable\n        or the "no-use-pep517" config file option. Use an appropriate value\n        of the PIP_USE_PEP517 environment variable or the "use-pep517"\n        config file option instead.\n        '
        raise_option_error(parser, option=option, msg=msg)
    parser.values.use_pep517 = False


use_pep517 = partial(Option,
  '--use-pep517',
  dest='use_pep517',
  action='store_true',
  default=None,
  help='Use PEP 517 for building source distributions (use --no-use-pep517 to force legacy behaviour).')
no_use_pep517 = partial(Option,
  '--no-use-pep517',
  dest='use_pep517',
  action='callback',
  callback=_handle_no_use_pep517,
  default=None,
  help=SUPPRESS_HELP)
install_options = partial(Option,
  '--install-option',
  dest='install_options',
  action='append',
  metavar='options',
  help='Extra arguments to be supplied to the setup.py install command (use like --install-option="--install-scripts=/usr/local/bin"). Use multiple --install-option options to pass multiple options to setup.py install. If you are using an option with a directory path, be sure to use absolute path.')
global_options = partial(Option,
  '--global-option',
  dest='global_options',
  action='append',
  metavar='options',
  help='Extra global options to be supplied to the setup.py call before the install command.')
no_clean = partial(Option,
  '--no-clean',
  action='store_true',
  default=False,
  help="Don't clean up build directories.")
pre = partial(Option,
  '--pre',
  action='store_true',
  default=False,
  help='Include pre-release and development versions. By default, pip only finds stable versions.')
disable_pip_version_check = partial(Option,
  '--disable-pip-version-check',
  dest='disable_pip_version_check',
  action='store_true',
  default=False,
  help="Don't periodically check PyPI to determine whether a new version of pip is available for download. Implied with --no-index.")
always_unzip = partial(Option,
  '-Z',
  '--always-unzip', dest='always_unzip',
  action='store_true',
  help=SUPPRESS_HELP)

def _handle_merge_hash(option, opt_str, value, parser):
    """Given a value spelled "algo:digest", append the digest to a list
    pointed to in a dict by the algo name."""
    if not parser.values.hashes:
        parser.values.hashes = {}
    try:
        algo, digest = value.split(':', 1)
    except ValueError:
        parser.error('Arguments to {} must be a hash name followed by a value, like --hash=sha256:abcde...'.format(opt_str))

    if algo not in STRONG_HASHES:
        parser.error('Allowed hash algorithms for {} are {}.'.format(opt_str, ', '.join(STRONG_HASHES)))
    parser.values.hashes.setdefault(algo, []).append(digest)


hash = partial(Option,
  '--hash',
  dest='hashes',
  action='callback',
  callback=_handle_merge_hash,
  type='string',
  help="Verify that the package's archive matches this hash before installing. Example: --hash=sha256:abcdef...")
require_hashes = partial(Option,
  '--require-hashes',
  dest='require_hashes',
  action='store_true',
  default=False,
  help='Require a hash to check each requirement against, for repeatable installs. This option is implied when any package in a requirements file has a --hash option.')
list_path = partial(PipOption,
  '--path',
  dest='path',
  type='path',
  action='append',
  help='Restrict to the specified installation path for listing packages (can be used multiple times).')

def check_list_path_option(options):
    if options.path:
        if options.user or options.local:
            raise CommandError("Cannot combine '--path' with '--user' or '--local'")


no_python_version_warning = partial(Option,
  '--no-python-version-warning',
  dest='no_python_version_warning',
  action='store_true',
  default=False,
  help='Silence deprecation warnings for upcoming unsupported Pythons.')
unstable_feature = partial(Option,
  '--unstable-feature',
  dest='unstable_features',
  metavar='feature',
  action='append',
  default=[],
  choices=[
 'resolver'],
  help=SUPPRESS_HELP)
general_group = {'name':'General Options', 
 'options':[
  help_,
  isolated_mode,
  require_virtualenv,
  verbose,
  version,
  quiet,
  log,
  no_input,
  proxy,
  retries,
  timeout,
  exists_action,
  trusted_host,
  cert,
  client_cert,
  cache_dir,
  no_cache,
  disable_pip_version_check,
  no_color,
  no_python_version_warning,
  unstable_feature]}
index_group = {'name':'Package Index Options', 
 'options':[
  index_url,
  extra_index_url,
  no_index,
  find_links]}