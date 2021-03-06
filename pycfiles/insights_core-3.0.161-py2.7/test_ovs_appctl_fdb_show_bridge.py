# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ovs_appctl_fdb_show_bridge.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import SkipException
from insights.parsers import ovs_appctl_fdb_show_bridge
from insights.parsers.ovs_appctl_fdb_show_bridge import OVSappctlFdbShowBridge
from insights.tests import context_wrap
import doctest, pytest
FDB_SHOW_BR_INT = ('\nport  VLAN  MAC                Age\n   6    29  aa:bb:cc:dd:ee:ff  270\n   3    27  gg:hh:ii:jj:kk:ll  266\n   3   100  mm:nn:oo:pp:qq:rr  263\n   1    29  dd:ee:ff:gg:hh:ii  234\n').strip()
FDB_SHOW_BR_TUN = ('\nport  VLAN  MAC                Age\n   7    29  aa:bb:cc:dd:ee:ff  27\n   3    27  gg:hh:ii:jj:kk:ll  266\n').strip()
PATH_BR_INT = ('insights_commands/ovs-appctl_fdb.show_br-int').strip()
PATH_BR_TUN = ('insights_commands/ovs-appctl_fdb.show_br_tun').strip()
EXCEPTION1 = ('\n').strip()
EXCEPTION2 = ('\nport  VLAN  MAC                Age\n').strip()

def test_ovs_appctl_fdb_show_bridge():
    data = OVSappctlFdbShowBridge(context_wrap(FDB_SHOW_BR_INT, path=PATH_BR_INT))
    assert len(data['br-int']) == 4
    assert data['br-int'][0]['VLAN'] == '29'
    assert int(data.get('br-int')[1]['Age']) == 266


def test_ovs_appctl_fdb_show_bridge_documentation():
    env = {'data': OVSappctlFdbShowBridge(context_wrap(FDB_SHOW_BR_TUN, PATH_BR_TUN))}
    failed, total = doctest.testmod(ovs_appctl_fdb_show_bridge, globs=env)
    assert failed == 0


def test_ovs_appctl_fdb_show_bridge_exception1():
    with pytest.raises(SkipException) as (e):
        OVSappctlFdbShowBridge(context_wrap(EXCEPTION1, path=PATH_BR_INT))
    assert 'Empty file' in str(e)


def test_ovs_appctl_fdb_show_bridge_exception2():
    with pytest.raises(SkipException) as (e):
        OVSappctlFdbShowBridge(context_wrap(EXCEPTION2, path=PATH_BR_TUN))
    assert 'No data present for br_tun' in str(e)