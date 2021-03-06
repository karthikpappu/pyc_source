# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_code_abinit.py
# Compiled at: 2020-01-17 14:30:03
# Size of source mod 2**32: 3589 bytes


def test_abinit_parser():
    """
    Test (pychemia.code.abinit) [parser]                        :
    """
    from pychemia.code.abinit import parser
    from numpy import array, all, ones
    from math import sqrt
    import tempfile
    wf = tempfile.NamedTemporaryFile(mode='w')
    wf.write('    # Comentario\n')
    wf.write('    ! Comentario\n')
    wf.write('\n')
    wf.write('inputvar1 1 # integer\n')
    wf.write('inputvar2 1.2 # float\n')
    wf.write('inputvar3 3*4 # list of integer\n')
    wf.write('inputvar4 3*4.5 # list of float\n')
    wf.write('inputvar5 3*4.5e6 # list of float\n')
    wf.write('inputvar6 3*4.5d7 # list of float\n')
    wf.write('inputvar7 3*4.5E6 # list of float\n')
    wf.write('inputvar8 3*4.5D7 # list of float\n')
    wf.write('inputvar9 *1\n')
    wf.write('inputvar10 sqrt(2)\n')
    wf.write('inputvar11 6*sqrt(3)\n')
    wf.flush()
    inp = parser(wf.name)
    wf.close()
    assert len(inp.keys()) == 11
    assert inp['inputvar1'] == array([1])
    assert inp['inputvar2'] == array([1.2])
    assert all(inp['inputvar3'] == 4 * ones(3))
    assert all(inp['inputvar4'] == 4.5 * ones(3))
    assert all(inp['inputvar5'] == 4500000.0 * ones(3))
    assert all(inp['inputvar6'] == 45000000.0 * ones(3))
    assert all(inp['inputvar7'] == 4500000.0 * ones(3))
    assert all(inp['inputvar8'] == 45000000.0 * ones(3))
    assert inp['inputvar9'] == '*1'
    assert inp['inputvar10'] == sqrt(2)
    assert all(inp['inputvar11'] == sqrt(3) * ones(6))


def test_abinit_utils():
    """
    Test (pychemia.code.abinit) [utils]                         :
    """
    from pychemia.utils.netcdf import netcdf2dict
    from pychemia.code.abinit import xyz2input, psp_name
    filename = 'tests/data/abinit_05/abinit-o_OUT.nc'
    print(len(netcdf2dict(filename)))
    assert len(netcdf2dict(filename)) == 45
    assert psp_name(1, 'LDA', 'FHI') == '01-H.LDA.fhi'
    filename = 'tests/data/abinit_01/abinit_DS11.xyz'
    assert xyz2input(filename).variables['natom'] == 2


def test_abinit_abifiles():
    """
    Test (pychemia.code.abinit) [abifiles]                      :
    """
    from pychemia.code.abinit import AbiFiles
    filename = 'tests/data/abinit_01/abinit.files'
    abf = AbiFiles(filename)
    assert abf.filename == 'abinit.files'
    assert abf.get_input_filename() == 'tests/data/abinit_01/abinit.in'


def test_abinit_input():
    """
    Test (pychemia.code.abinit) [input]                         :
    """
    from pychemia.code.abinit import AbiFiles, AbinitInput
    filename = 'tests/data/abinit_01/abinit.files'
    abf = AbiFiles(filename)
    inp = AbinitInput(abf.get_input_filename())
    print(inp)
    print(len(inp))
    assert len(inp) == 31
    assert inp.get_value('ecut') == 10
    assert len(inp.get_dtsets_keys()) == 12
    assert inp.get_value('ntime', 41) == 10
    assert inp.get_value('acell', 41)[0] == 14


def test_abinit():
    """
    Test (pychemia.code.abinit) [general]                       :
    """
    import os, pychemia.code.abinit
    af = pychemia.code.abinit.AbiFiles(basedir='tests/data/abinit_03')
    iv = pychemia.code.abinit.AbinitInput('tests/data/abinit_03/rnpg.in')
    af.set_input(iv)
    af.set_psps('LDA', 'FHI')
    af.create()
    iv.write(af.get_input_filename())
    assert len(open(af.get_input_filename()).readlines()) == 71
    rf = open('tests/data/abinit_03/abinit.files')
    data = rf.readlines()
    print(data)
    for i in (-4, -3, -2, -1):
        assert data[i].strip()[-4:] == '.fhi'

    rf.close()
    os.remove('tests/data/abinit_03/abinit.files')