# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_cpu_vulns_all.py
# Compiled at: 2019-11-14 13:57:46
from insights.tests import context_wrap
from insights.parsers.cpu_vulns import CpuVulns
from insights.combiners import cpu_vulns_all
from insights.combiners.cpu_vulns_all import CpuVulnsAll
from insights.parsers import SkipComponent
import doctest, pytest
IMPUT_MELTDOWN_EMPTY = ('\n').strip()
INPUT_MELTDOWN = ('\nMitigation: PTI\n').strip()
INPUT_SPECTRE_V1 = ('\nMitigation: Load fences\n').strip()
INPUT_SPECTRE_V2 = ('\nMitigation: Full generic retpoline, IBPB: conditional, IBRS_FW, STIBP: conditional, RSB filling\n').strip()
INPUT_SPEC_STORE_BYPASS = ('\nMitigation: Speculative Store Bypass disabled\n').strip()
INPUT_SMT = ('\nMitigation: PTE Inversion; VMX: conditional cache flushes, SMT vulnerable\n').strip()
INPUT_MDS = ('\nVulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable\n').strip()
INPUT0 = context_wrap(INPUT_MELTDOWN, path='')
INPUT1 = context_wrap(INPUT_MELTDOWN, path='/sys/devices/system/cpu/vulnerabilities/meltdown')
INPUT2 = context_wrap(INPUT_SPECTRE_V1, path='/sys/devices/system/cpu/vulnerabilities/spectre_v1')
INPUT3 = context_wrap(INPUT_SPECTRE_V2, path='/sys/devices/system/cpu/vulnerabilities/spectre_v2')
INPUT4 = context_wrap(INPUT_SPEC_STORE_BYPASS, path='/sys/devices/system/cpu/vulnerabilities/spec_store_bypass')
INPUT5 = context_wrap(INPUT_SMT, path='/sys/devices/system/cpu/vulnerabilities/l1tf')
INPUT6 = context_wrap(INPUT_MDS, path='/sys/devices/system/cpu/vulnerabilities/mds')
parser0 = CpuVulns(INPUT0)
parser1 = CpuVulns(INPUT1)
parser2 = CpuVulns(INPUT2)
parser3 = CpuVulns(INPUT3)
parser4 = CpuVulns(INPUT4)
parser5 = CpuVulns(INPUT5)
parser6 = CpuVulns(INPUT6)

def test_values_comb_meltdown():
    obj = CpuVulnsAll([parser1, parser2, parser3])
    assert 'meltdown' in obj
    assert obj == {'meltdown': 'Mitigation: PTI', 'spectre_v1': 'Mitigation: Load fences', 'spectre_v2': 'Mitigation: Full generic retpoline, IBPB: conditional, IBRS_FW, STIBP: conditional, RSB filling'}


def test_values_comb_spectre_v1():
    obj = CpuVulnsAll([parser1, parser2])
    assert 'spectre_v1' in obj
    assert obj == {'meltdown': 'Mitigation: PTI', 'spectre_v1': 'Mitigation: Load fences'}


def test_values_comb_spectre_v2():
    obj = CpuVulnsAll([parser1, parser3])
    assert 'spectre_v2' in obj
    assert obj == {'meltdown': 'Mitigation: PTI', 'spectre_v2': 'Mitigation: Full generic retpoline, IBPB: conditional, IBRS_FW, STIBP: conditional, RSB filling'}


def test_values_comb_spec_store_bypass():
    obj = CpuVulnsAll([parser1, parser4])
    assert 'spec_store_bypass' in obj
    assert obj == {'meltdown': 'Mitigation: PTI', 'spec_store_bypass': 'Mitigation: Speculative Store Bypass disabled'}


def test_values_comb_l1tf():
    obj = CpuVulnsAll([parser1, parser5])
    assert 'l1tf' in obj
    assert obj == {'meltdown': 'Mitigation: PTI', 'l1tf': 'Mitigation: PTE Inversion; VMX: conditional cache flushes, SMT vulnerable'}


def test_values_comb_mds():
    obj = CpuVulnsAll([parser6])
    assert 'mds' in obj
    assert obj == {'mds': 'Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable'}


def test_values_integration():
    obj = CpuVulnsAll([parser1, parser2, parser3, parser4, parser5, parser6])
    assert 'spectre_v1' and 'spec_store_bypass' in obj
    assert obj == {'meltdown': 'Mitigation: PTI', 'spectre_v1': 'Mitigation: Load fences', 'spectre_v2': 'Mitigation: Full generic retpoline, IBPB: conditional, IBRS_FW, STIBP: conditional, RSB filling', 'spec_store_bypass': 'Mitigation: Speculative Store Bypass disabled', 'l1tf': 'Mitigation: PTE Inversion; VMX: conditional cache flushes, SMT vulnerable', 'mds': 'Vulnerable: Clear CPU buffers attempted, no microcode; SMT vulnerable'}


def test_values_exp():
    with pytest.raises(SkipComponent) as (pe):
        CpuVulnsAll([parser0])
    assert 'Not available data' in str(pe)


def test_x86_enabled_documentation():
    """
    Here we test the examples in the documentation automatically using
    doctest.  We set up an environment which is similar to what a rule
    writer might see - a '/sys/devices/system/cpu/vulnerabilities/*' output
    that has been passed in as a parameter to the rule declaration.
    """
    parser1 = CpuVulns(INPUT1)
    parser2 = CpuVulns(INPUT2)
    env = {'cvb': CpuVulnsAll([parser1, parser2])}
    failed, total = doctest.testmod(cpu_vulns_all, globs=env)
    assert failed == 0