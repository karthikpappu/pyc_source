# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/parse/versions.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = 'Parsers for Tor version number strings.\n\n.. py:module:: bridgedb.parse.versions\n    :synopsis: Parsers for Tor version number strings.\n\nbridgedb.parse.versions\n=======================\n::\n\n  Version - Holds, parses, and does comparison operations for package\n            version numbers.\n..\n'
from twisted import version as _txversion
if _txversion.major >= 14:
    from twisted.python.versions import Version as _Version
else:
    from twisted.python.util import Version as _Version

class InvalidVersionStringFormat(ValueError):
    """Raised when a version string is not in a parseable format."""


class Version(_Version):
    """Holds, parses, and does comparison operations for version numbers.

    :attr str package: The package name, if available.
    :attr int major: The major version number.
    :attr int minor: The minor version number.
    :attr int micro: The micro version number.
    :attr str prerelease: The **prerelease** specifier isn't always present,
        though when it is, it's usually separated from the main
        ``major.minor.micro`` part of the version string with a ``-``, ``+``,
        or ``#`` character. Sometimes the **prerelease** is another number,
        although often it can be a word specifying the release state,
        i.e. ``+alpha``, ``-rc2``, etc.
    """

    def __init__(self, version, package=None):
        """Create a version object.

        Comparisons may be computed between instances of :class:`Version`s.

        >>> from bridgedb.parse.versions import Version
        >>> v1 = Version("0.2.3.25", package="tor")
        >>> v1.base()
        '0.2.3.25'
        >>> v1.package
        'tor'
        >>> v2 = Version("0.2.5.1-alpha", package="tor")
        >>> v2
        Version(package=tor, major=0, minor=2, micro=5, prerelease=1-alpha)
        >>> v1 == v2
        False
        >>> v2 > v1
        True

        :param str version: A Tor version string specifier, i.e. one taken
            from either the ``client-versions`` or ``server-versions`` lines
            within a Tor ``cached-consensus`` file.
        :param str package: The package or program which we are creating a
            version number for.
        """
        if version.find('.') == -1:
            raise InvalidVersionStringFormat('Invalid delimiters in version string: %r' % version)
        package = package if package is not None else str()
        major, minor, micro = [ int() for _ in range(3) ]
        prerelease = str()
        components = version.split('.')
        if len(components) > 0:
            try:
                prerelease = str(components.pop())
                micro = int(components.pop())
                minor = int(components.pop())
                major = int(components.pop())
            except IndexError:
                pass

        super(Version, self).__init__(package, major, minor, micro, prerelease)
        return

    def base(self):
        """Get the base version number (with prerelease).

        :rtype: string
        :returns: A version number, without the package/program name, and with
            the prefix (if available). For example: '0.2.5.1-alpha'.
        """
        pre = self.getPrefixedPrerelease()
        return '%s.%s.%s%s' % (self.major, self.minor, self.micro, pre)

    def getPrefixedPrerelease(self, separator='.'):
        """Get the prerelease string, prefixed by the separator ``prefix``.

        :param string separator: The separator to use between the rest of the
            version string and the :attr:`prerelease` string.
        :rtype: string
        :returns: The separator plus the ``prefix``, i.e. '.1-alpha'.
        """
        pre = ''
        if self.prerelease is not None:
            pre = separator + self.prerelease
        return pre

    def __repr__(self):
        prerelease = self.getPrefixedPrerelease('')
        return '%s(package=%s, major=%s, minor=%s, micro=%s, prerelease=%s)' % (
         str(self.__class__.__name__),
         str(self.package),
         str(self.major),
         str(self.minor),
         str(self.micro),
         str(prerelease))