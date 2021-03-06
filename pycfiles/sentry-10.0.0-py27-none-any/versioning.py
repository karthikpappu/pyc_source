# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/versioning.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import six
from sentry.exceptions import InvalidConfiguration
from sentry.utils import warnings

class Version(tuple):

    def __str__(self):
        return ('.').join(map(six.binary_type, self))


def summarize(sequence, max=3):
    items = sequence[:max]
    remainder = len(sequence) - max
    if remainder == 1:
        items.append('and one other')
    elif remainder > 1:
        items.append('and %s others' % (remainder,))
    return items


def make_upgrade_message(service, modality, version, hosts):
    return ('{service} {modality} be upgraded to {version} on {hosts}.').format(hosts=(',').join(map(six.binary_type, summarize(hosts.keys(), 2))), modality=modality, service=service, version=version)


def check_versions(service, versions, required, recommended=None):
    """
    Check that hosts fulfill version requirements.

    :param service: service label, such as ``Redis``
    :param versions: mapping of host to ``Version``
    :param required: lowest supported ``Version``. If any host does not fulfill
        this requirement, an ``InvalidConfiguration`` exception is raised.
    :param recommended: recommended version. If any host does not fulfill this
        requirement, a ``PendingDeprecationWarning`` is raised.
    """
    must_upgrade = dict(filter(lambda x: required > x[1], versions.items()))
    if must_upgrade:
        raise InvalidConfiguration(make_upgrade_message(service, 'must', required, must_upgrade))
    if recommended:
        should_upgrade = dict(filter(lambda x: recommended > x[1], versions.items()))
        if should_upgrade:
            warnings.warn(make_upgrade_message(service, 'should', recommended, should_upgrade), PendingDeprecationWarning)