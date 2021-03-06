# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/total_scattering/reduction/total_scattering_reduction.py
# Compiled at: 2019-10-03 13:30:51
from __future__ import absolute_import, division, print_function
import os, itertools, numpy as np
from scipy.constants import Avogadro
from mantid import mtd
from mantid.simpleapi import CarpenterSampleCorrection, CloneWorkspace, CompressEvents, ConvertToDistribution, ConvertToHistogram, ConvertUnits, CreateEmptyTableWorkspace, CreateGroupingWorkspace, CropWorkspaceRagged, Divide, FFTSmooth, GenerateEventsFilter, GroupWorkspaces, Load, LoadDetectorsGroupingFile, LoadDiffCal, MayersSampleCorrection, Minus, PDDetermineCharacterizations, PropertyManagerDataService, Rebin, SaveGSS, SetSample, SetUncertainties, StripVanadiumPeaks
from total_scattering.file_handling.load import load
from total_scattering.file_handling.save import save_banks
from total_scattering.inelastic.placzek import CalculatePlaczekSelfScattering, FitIncidentSpectrum, GetIncidentSpectrumFromMonitor

def generate_cropping_table(qmin, qmax):
    """ Generate a Table workspace that can be used to crop
    another workspace in reciprocal space (ie MomentumTransfer)

    :param qmin: list of Qmin values to crop each spectra by
    :type qmin: str (example: '0.2,0.4,1.0')
    :param qmax: list of Qmax values to crop each spectra by
    :type qmax: str (example: '10.5,12.0,40.0')

    :return: Cropping table with columns of ("SpectraList","Xmin","Xmax")
    :rtype: TableWorkspace
    """
    mask_info = CreateEmptyTableWorkspace()
    mask_info.addColumn('str', 'SpectraList')
    mask_info.addColumn('double', 'XMin')
    mask_info.addColumn('double', 'XMax')
    for i, value in enumerate(qmin):
        mask_info.addRow([str(i), 0.0, value])

    for i, value in enumerate(qmax):
        mask_info.addRow([str(i), value, 100.0])

    return mask_info


def get_each_spectra_xmin_xmax(wksp):
    """ Get Xmin and Xmax lists for Workspace, excluding
    values of inf and NaN

    :param wksp: Workspace to extract the xmin and xmax values from
    :type qmin: Mantid Workspace

    :return: Lists for XMin and XMax values:
    :rtype: (list, list) == (xmin, xmax)
    """
    xmin = list()
    xmax = list()
    numSpectra = wksp.getNumberHistograms()
    for i in range(numSpectra):
        x = wksp.readX(i)
        xmin.append(np.nanmin(x[(x != -np.inf)]))
        xmax.append(np.nanmax(x[(x != np.inf)]))

    return (
     xmin, xmax)


def expand_ints(s):
    spans = (el.partition('-')[::2] for el in s.split(','))
    ranges = (range(int(s), int(e) + 1 if e else int(s) + 1) for s, e in spans)
    all_nums = itertools.chain.from_iterable(ranges)
    return list(all_nums)


def compress_ints(line_nums):
    seq = []
    final = []
    last = 0
    for index, val in enumerate(line_nums):
        if last + 1 == val or index == 0:
            seq.append(val)
            last = val
        else:
            if len(seq) > 1:
                final.append(str(seq[0]) + '-' + str(seq[(len(seq) - 1)]))
            else:
                final.append(str(seq[0]))
            seq = []
            seq.append(val)
            last = val
        if index == len(line_nums) - 1:
            if len(seq) > 1:
                final.append(str(seq[0]) + '-' + str(seq[(len(seq) - 1)]))
            else:
                final.append(str(seq[0]))

    final_str = (', ').join(map(str, final))
    return final_str


class Shape(object):

    def __init__(self):
        self.shape = None
        return

    def getShape(self):
        return self.shape


class Cylinder(Shape):

    def __init__(self):
        self.shape = 'Cylinder'

    def volume(self, Radius=None, Height=None, **kwargs):
        return np.pi * Height * Radius * Radius


class Sphere(Shape):

    def __init__(self):
        self.shape = 'Sphere'

    def volume(self, Radius=None, **kwargs):
        return 1.3333333333333333 * np.pi * Radius * Radius * Radius


class GeometryFactory(object):

    @staticmethod
    def factory(Geometry):
        factory = {'Cylinder': Cylinder(), 'Sphere': Sphere()}
        return factory[Geometry['Shape']]


def getNumberAtoms(PackingFraction, MassDensity, MolecularMass, Geometry=None):
    if Geometry is None:
        Geometry = dict()
    if 'Shape' not in Geometry:
        Geometry['Shape'] = 'Cylinder'
    space = GeometryFactory.factory(Geometry)
    volume_in_beam = space.volume(**Geometry)
    number_density = PackingFraction * MassDensity / MolecularMass * Avogadro
    natoms = number_density * volume_in_beam
    return natoms


def GenerateEventsFilterFromFiles(filenames, OutputWorkspace, InformationWorkspace, **kwargs):
    logName = kwargs.get('LogName', None)
    minValue = kwargs.get('MinimumLogValue', None)
    maxValue = kwargs.get('MaximumLogValue', None)
    logInterval = kwargs.get('LogValueInterval', None)
    unitOfTime = kwargs.get('UnitOfTime', 'Nanoseconds')
    if len(filenames) == 1:
        error = 'Multi-file filtering is not yet supported. (Stay tuned...)'
        raise Exception(error)
    for i, filename in enumerate(filenames):
        Load(Filename=filename, OutputWorkspace=filename)
        splitws, infows = GenerateEventsFilter(InputWorkspace=filename, UnitOfTime=unitOfTime, LogName=logName, MinimumLogValue=minValue, MaximumLogValue=maxValue, LogValueInterval=logInterval)
        if i == 0:
            GroupWorkspaces(splitws, OutputWorkspace=OutputWorkspace)
            GroupWorkspaces(infows, OutputWorkspace=InformationWorkspace)
        else:
            mtd[OutputWorkspace].add(splitws)
            mtd[InformationWorkspace].add(infows)

    return


def print_unit_info(workspace):
    ws = mtd[workspace]
    for i in range(ws.axes()):
        axis = ws.getAxis(i)
        print(('Axis {0} is a {1}{2}{3}').format(i, 'Spectrum Axis' if axis.isSpectra() else '', 'Text Axis' if axis.isText() else '', 'Numeric Axis' if axis.isNumeric() else ''))
        unit = axis.getUnit()
        print(('\n YUnit:{0}').format(ws.YUnit()))
        print(('\t caption:{0}').format(unit.caption()))
        print(('\t symbol:{0}').format(unit.symbol()))


def SetInelasticCorrection(inelastic_dict):
    default_inelastic_dict = {'Type': None}
    if inelastic_dict is None:
        return default_inelastic_dict
    else:
        corr_type = inelastic_dict['Type']
        if corr_type is None or corr_type == 'None':
            return default_inelastic_dict
        if corr_type:
            if corr_type == 'Placzek':
                default_settings = {'Order': '1st', 'Self': True, 'Interference': False, 
                   'FitSpectrumWith': 'GaussConvCubicSpline', 
                   'LambdaBinning': '0.16,0.04,2.8'}
                inelastic_settings = default_settings.copy()
                inelastic_settings.update(inelastic_dict)
            else:
                raise Exception('Unknown Inelastic Correction Type')
        return inelastic_settings


def one_and_only_one(iterable):
    """Determine if iterable (ie list) has one and only one `True` value

    :param iterable: The iterable to check
    :type iterable: list

    :return: If there is one and only one True
    :rtype: bool
    """
    try:
        iterator = iter(iterable)
        has_true = any(iterator)
        has_another_true = any(iterator)
        return has_true and not has_another_true
    except Exception as e:
        print(e)
        raise


def find_key_match_in_dict(keys, dictionary):
    """ Check if one and only one of the keys is in the dictionary
    and return its value

    :param key: Keys we will check for in dictionary
    :type key: str
    :param dictionary: Dictionary to check
    :type dictionary: dict

    :return: Either the value in dictionary for the key or None if not found
    :rtype: value in dict or None
    """
    keys_exist_in_dict = map(lambda key: key in dictionary, keys)
    if one_and_only_one(keys_exist_in_dict):
        for key in keys:
            if key in dictionary:
                return dictionary[key]

    return


def extract_key_match_from_dict(keys, dictionary):
    """ Convienence function for extraction of one key from dictionary

    :param keys: Keys to check against dictionary
    :type keys: list
    :param dictionary: Dictionary to check
    "type dictionary: dict

    :return: The exctracted value
    :rtype: any
    """
    out = find_key_match_in_dict(keys, dictionary)
    if out:
        return out
    e = ('No matching key found. Valid keys are {}').format(keys)
    raise Exception(e)


def get_sample(config):
    """ Extract the sample section from JSON input

    :param config: JSON input for reduction
    :type config: dict

    :return: The exctracted value for sample in the input
    :rtype: any
    """
    keys = [
     'Sample']
    out = extract_key_match_from_dict(keys, config)
    return out


def get_normalization(config):
    """ Extract the normalization section from JSON input

    :param config: JSON input for reduction
    :type config: dict

    :return: The exctracted value for normalization in the input
    :rtype: any
    """
    keys = [
     'Normalization', 'Normalisation', 'Vanadium']
    out = extract_key_match_from_dict(keys, config)
    return out


def TotalScatteringReduction(config=None):
    facility = config['Facility']
    title = config['Title']
    instr = config['Instrument']
    sample = get_sample(config)
    sam_mass_density = sample.get('MassDensity', None)
    sam_packing_fraction = sample.get('PackingFraction', None)
    sam_geometry = sample.get('Geometry', None)
    sam_material = sample.get('Material', None)
    van = get_normalization(config)
    van_mass_density = van.get('MassDensity', None)
    van_packing_fraction = van.get('PackingFraction', 1.0)
    van_geometry = van.get('Geometry', None)
    van_material = van.get('Material', 'V')
    merging = config['Merging']
    binning = merging['QBinning']
    characterizations = merging.get('Characterizations', None)
    grouping = merging.get('Grouping', None)
    cache_dir = config.get('CacheDir', os.path.abspath('.'))
    OutputDir = config.get('OutputDir', os.path.abspath('.'))
    sample['Runs'] = expand_ints(sample['Runs'])
    sample['Background']['Runs'] = expand_ints(sample['Background'].get('Runs', None))
    if facility == 'SNS':
        facility_file_format = '%s_%d'
    else:
        facility_file_format = '%s%d'
    sam_scans = (',').join([ facility_file_format % (instr, num) for num in sample['Runs']
                           ])
    container_scans = (',').join([ facility_file_format % (instr, num) for num in sample['Background']['Runs']
                                 ])
    container_bg = None
    if 'Background' in sample['Background']:
        sample['Background']['Background']['Runs'] = expand_ints(sample['Background']['Background']['Runs'])
        container_bg = (',').join([ facility_file_format % (instr, num) for num in sample['Background']['Background']['Runs']
                                  ])
        if len(container_bg) == 0:
            container_bg = None
    van['Runs'] = expand_ints(van['Runs'])
    van_scans = (',').join([ facility_file_format % (instr, num) for num in van['Runs']
                           ])
    van_bg_scans = None
    if 'Background' in van:
        van_bg_scans = van['Background']['Runs']
        van_bg_scans = expand_ints(van_bg_scans)
        van_bg_scans = (',').join([ facility_file_format % (instr, num) for num in van_bg_scans
                                  ])
    if 'Filenames' in sample:
        sam_scans = (',').join(sample['Filenames'])
    if 'Filenames' in sample['Background']:
        container_scans = (',').join(sample['Background']['Filenames'])
    if 'Background' in sample['Background']:
        if 'Filenames' in sample['Background']['Background']:
            container_bg = (',').join(sample['Background']['Background']['Filenames'])
    if 'Filenames' in van:
        van_scans = (',').join(van['Filenames'])
    if 'Background' in van:
        if 'Filenames' in van['Background']:
            van_bg_scans = (',').join(van['Background']['Filenames'])
    nexus_filename = title + '.nxs'
    try:
        os.remove(nexus_filename)
    except OSError:
        pass

    sam_abs_corr = sample.get('AbsorptionCorrection', None)
    sam_ms_corr = sample.get('MultipleScatteringCorrection', None)
    sam_inelastic_corr = SetInelasticCorrection(sample.get('InelasticCorrection', None))
    van_mass_density = van.get('MassDensity', van_mass_density)
    van_packing_fraction = van.get('PackingFraction', van_packing_fraction)
    van_abs_corr = van.get('AbsorptionCorrection', {'Type': None})
    van_ms_corr = van.get('MultipleScatteringCorrection', {'Type': None})
    van_inelastic_corr = SetInelasticCorrection(van.get('InelasticCorrection', None))
    alignAndFocusArgs = dict()
    alignAndFocusArgs['CalFilename'] = config['Calibration']['Filename']
    alignAndFocusArgs['ResampleX'] = -6000
    alignAndFocusArgs['Dspacing'] = False
    alignAndFocusArgs['PreserveEvents'] = False
    alignAndFocusArgs['MaxChunkSize'] = 8
    alignAndFocusArgs['CacheDir'] = os.path.abspath(cache_dir)
    if 'AlignAndFocusArgs' in config:
        otherArgs = config['AlignAndFocusArgs']
        alignAndFocusArgs.update(otherArgs)
    print(alignAndFocusArgs)
    output_grouping = False
    grp_wksp = 'wksp_output_group'
    if grouping:
        if 'Initial' in grouping:
            if grouping['Initial'] and not grouping['Initial'] == '':
                alignAndFocusArgs['GroupFilename'] = grouping['Initial']
        if 'Output' in grouping:
            if grouping['Output'] and not grouping['Output'] == '':
                output_grouping = True
                LoadDetectorsGroupingFile(InputFile=grouping['Output'], OutputWorkspace=grp_wksp)
    if not output_grouping:
        LoadDiffCal(alignAndFocusArgs['CalFilename'], InstrumentName=instr, WorkspaceName=grp_wksp.replace('_group', ''), MakeGroupingWorkspace=True, MakeCalWorkspace=False, MakeMaskWorkspace=False)
    if not grouping:
        CreateGroupingWorkspace(InstrumentName=instr, GroupDetectorsBy='Group', OutputWorkspace=grp_wksp)
        alignAndFocusArgs['GroupingWorkspace'] = grp_wksp
    print('#-----------------------------------#')
    print('# Sample')
    print('#-----------------------------------#')
    sam_wksp = load('sample', sam_scans, sam_geometry, sam_material, sam_mass_density, **alignAndFocusArgs)
    sample_title = 'sample_and_container'
    print(os.path.join(OutputDir, sample_title + '.dat'))
    print('HERE:', mtd[sam_wksp].getNumberHistograms())
    print(grp_wksp)
    save_banks(InputWorkspace=sam_wksp, Filename=nexus_filename, Title=sample_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    sam_molecular_mass = mtd[sam_wksp].sample().getMaterial().relativeMolecularMass()
    natoms = getNumberAtoms(sam_packing_fraction, sam_mass_density, sam_molecular_mass, Geometry=sam_geometry)
    print('#-----------------------------------#')
    print('# Sample Container')
    print('#-----------------------------------#')
    container = load('container', container_scans, **alignAndFocusArgs)
    save_banks(InputWorkspace=container, Filename=nexus_filename, Title=container, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    if container_bg is not None:
        print('#-----------------------------------#')
        print("# Sample Container's Background")
        print('#-----------------------------------#')
        container_bg = load('container_background', container_bg, **alignAndFocusArgs)
        save_banks(InputWorkspace=container_bg, Filename=nexus_filename, Title=container_bg, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    print('#-----------------------------------#')
    print('# Vanadium')
    print('#-----------------------------------#')
    van_wksp = load('vanadium', van_scans, van_geometry, van_material, van_mass_density, **alignAndFocusArgs)
    vanadium_title = 'vanadium_and_background'
    save_banks(InputWorkspace=van_wksp, Filename=nexus_filename, Title=vanadium_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    van_material = mtd[van_wksp].sample().getMaterial()
    van_molecular_mass = van_material.relativeMolecularMass()
    nvan_atoms = getNumberAtoms(1.0, van_mass_density, van_molecular_mass, Geometry=van_geometry)
    print('Sample natoms:', natoms)
    print('Vanadium natoms:', nvan_atoms)
    print('Vanadium natoms / Sample natoms:', nvan_atoms / natoms)
    van_bg = None
    if van_bg_scans is not None:
        print('#-----------------------------------#')
        print('# Vanadium Background')
        print('#-----------------------------------#')
        van_bg = load('vanadium_background', van_bg_scans, **alignAndFocusArgs)
        vanadium_bg_title = 'vanadium_background'
        save_banks(InputWorkspace=van_bg, Filename=nexus_filename, Title=vanadium_bg_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    if characterizations:
        PDDetermineCharacterizations(InputWorkspace=sam_wksp, Characterizations='characterizations', ReductionProperties='__snspowderreduction')
        propMan = PropertyManagerDataService.retrieve('__snspowderreduction')
        qmax = 2.0 * np.pi / propMan['d_min'].value
        qmin = 2.0 * np.pi / propMan['d_max'].value
        for a, b in zip(qmin, qmax):
            print('Qrange:', a, b)

    sam_raw = 'sam_raw'
    CloneWorkspace(InputWorkspace=sam_wksp, OutputWorkspace=sam_raw)
    container_raw = 'container_raw'
    CloneWorkspace(InputWorkspace=container, OutputWorkspace=container_raw)
    if van_bg is not None:
        Minus(LHSWorkspace=van_wksp, RHSWorkspace=van_bg, OutputWorkspace=van_wksp)
    Minus(LHSWorkspace=sam_wksp, RHSWorkspace=container, OutputWorkspace=sam_wksp)
    if container_bg is not None:
        Minus(LHSWorkspace=container, RHSWorkspace=container_bg, OutputWorkspace=container)
    for wksp in [container, van_wksp, sam_wksp]:
        ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target='MomentumTransfer', EMode='Elastic')

    container_title = 'container_minus_back'
    vanadium_title = 'vanadium_minus_back'
    sample_title = 'sample_minus_back'
    save_banks(InputWorkspace=container, Filename=nexus_filename, Title=container_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    save_banks(InputWorkspace=van_wksp, Filename=nexus_filename, Title=vanadium_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    save_banks(InputWorkspace=sam_wksp, Filename=nexus_filename, Title=sample_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    van_corrected = 'van_corrected'
    ConvertUnits(InputWorkspace=van_wksp, OutputWorkspace=van_corrected, Target='Wavelength', EMode='Elastic')
    if 'Type' in van_abs_corr:
        if van_abs_corr['Type'] == 'Carpenter' or van_ms_corr['Type'] == 'Carpenter':
            CarpenterSampleCorrection(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, CylinderSampleRadius=van['Geometry']['Radius'])
        elif van_abs_corr['Type'] == 'Mayers' or van_ms_corr['Type'] == 'Mayers':
            if van_ms_corr['Type'] == 'Mayers':
                MayersSampleCorrection(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, MultipleScattering=True)
            else:
                MayersSampleCorrection(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, MultipleScattering=False)
        else:
            print('NO VANADIUM absorption or multiple scattering!')
    else:
        CloneWorkspace(InputWorkspace=van_corrected, OutputWorkspace=van_corrected)
    ConvertUnits(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, Target='MomentumTransfer', EMode='Elastic')
    vanadium_title += '_ms_abs_corrected'
    save_banks(InputWorkspace=van_corrected, Filename=nexus_filename, Title=vanadium_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    save_banks(InputWorkspace=van_corrected, Filename=nexus_filename, Title=vanadium_title + '_with_peaks', OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    ConvertUnits(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, Target='dSpacing', EMode='Elastic')
    StripVanadiumPeaks(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, BackgroundType='Quadratic')
    ConvertUnits(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, Target='MomentumTransfer', EMode='Elastic')
    vanadium_title += '_peaks_stripped'
    save_banks(InputWorkspace=van_corrected, Filename=nexus_filename, Title=vanadium_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    ConvertUnits(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, Target='TOF', EMode='Elastic')
    FFTSmooth(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, Filter='Butterworth', Params='20,2', IgnoreXBins=True, AllSpectra=True)
    ConvertUnits(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, Target='MomentumTransfer', EMode='Elastic')
    vanadium_title += '_smoothed'
    save_banks(InputWorkspace=van_corrected, Filename=nexus_filename, Title=vanadium_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    if van_inelastic_corr['Type'] == 'Placzek':
        van_scan = van['Runs'][0]
        van_incident_wksp = 'van_incident_wksp'
        van_inelastic_opts = van['InelasticCorrection']
        lambda_binning_fit = van_inelastic_opts['LambdaBinningForFit']
        lambda_binning_calc = van_inelastic_opts['LambdaBinningForCalc']
        print('van_scan:', van_scan)
        GetIncidentSpectrumFromMonitor(Filename=facility_file_format % (instr, van_scan), OutputWorkspace=van_incident_wksp)
        fit_type = van['InelasticCorrection']['FitSpectrumWith']
        FitIncidentSpectrum(InputWorkspace=van_incident_wksp, OutputWorkspace=van_incident_wksp, FitSpectrumWith=fit_type, BinningForFit=lambda_binning_fit, BinningForCalc=lambda_binning_calc, PlotDiagnostics=False)
        van_placzek = 'van_placzek'
        SetSample(InputWorkspace=van_incident_wksp, Material={'ChemicalFormula': str(van_material), 'SampleMassDensity': str(van_mass_density)})
        CalculatePlaczekSelfScattering(IncidentWorkspace=van_incident_wksp, ParentWorkspace=van_corrected, OutputWorkspace=van_placzek, L1=19.5, L2=alignAndFocusArgs['L2'], Polar=alignAndFocusArgs['Polar'])
        ConvertToHistogram(InputWorkspace=van_placzek, OutputWorkspace=van_placzek)
        for wksp in [van_placzek, van_corrected]:
            ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target='MomentumTransfer', EMode='Elastic')
            Rebin(InputWorkspace=wksp, OutputWorkspace=wksp, Params=binning, PreserveEvents=True)

        save_banks(InputWorkspace=van_placzek, Filename=nexus_filename, Title='vanadium_placzek', OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
        for wksp in [van_placzek, van_corrected]:
            ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target='Wavelength', EMode='Elastic')
            Rebin(InputWorkspace=wksp, OutputWorkspace=wksp, Params=lambda_binning_calc, PreserveEvents=True)

        for wksp in [van_placzek, van_corrected]:
            ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target='MomentumTransfer', EMode='Elastic')

        for wksp in [van_placzek, van_corrected]:
            ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target='Wavelength', EMode='Elastic')
            if not mtd[wksp].isDistribution():
                ConvertToDistribution(wksp)

        Minus(LHSWorkspace=van_corrected, RHSWorkspace=van_placzek, OutputWorkspace=van_corrected)
        for wksp in [van_placzek, van_corrected]:
            ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target='MomentumTransfer', EMode='Elastic')

        vanadium_title += '_placzek_corrected'
        save_banks(InputWorkspace=van_corrected, Filename=nexus_filename, Title=vanadium_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    ConvertUnits(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, Target='MomentumTransfer', EMode='Elastic')
    SetUncertainties(InputWorkspace=van_corrected, OutputWorkspace=van_corrected, SetError='zero')
    wksp_list = [
     sam_wksp, sam_raw, van_corrected]
    for name in wksp_list:
        ConvertUnits(InputWorkspace=name, OutputWorkspace=name, Target='MomentumTransfer', EMode='Elastic', ConvertFromPointData=False)
        Rebin(InputWorkspace=name, OutputWorkspace=name, Params=binning, PreserveEvents=True)

    Divide(LHSWorkspace=sam_wksp, RHSWorkspace=van_corrected, OutputWorkspace=sam_wksp)
    sample_title += '_normalized'
    save_banks(InputWorkspace=sam_wksp, Filename=nexus_filename, Title=sample_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    Divide(LHSWorkspace=sam_raw, RHSWorkspace=van_corrected, OutputWorkspace=sam_raw)
    save_banks(InputWorkspace=sam_raw, Filename=nexus_filename, Title='sample_normalized', OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    iq_filename = title + '_initial_iofq_banks.nxs'
    save_banks(InputWorkspace=sam_wksp, Filename=iq_filename, Title='IQ_banks', OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    wksp_list = [
     container, container_raw, van_corrected]
    if container_bg is not None:
        wksp_list.append(container_bg)
    if van_bg is not None:
        wksp_list.append(van_bg)
    for name in wksp_list:
        ConvertUnits(InputWorkspace=name, OutputWorkspace=name, Target='MomentumTransfer', EMode='Elastic', ConvertFromPointData=False)
        Rebin(InputWorkspace=name, OutputWorkspace=name, Params=binning, PreserveEvents=True)

    Divide(LHSWorkspace=container, RHSWorkspace=van_corrected, OutputWorkspace=container)
    container_title += '_normalized'
    save_banks(InputWorkspace=container, Filename=nexus_filename, Title=container_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    Divide(LHSWorkspace=container_raw, RHSWorkspace=van_corrected, OutputWorkspace=container_raw)
    save_banks(InputWorkspace=container_raw, Filename=nexus_filename, Title='container_normalized', OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    if container_bg is not None:
        Divide(LHSWorkspace=container_bg, RHSWorkspace=van_corrected, OutputWorkspace=container_bg)
        container_bg_title = 'container_back_normalized'
        save_banks(InputWorkspace=container_bg, Filename=nexus_filename, Title=container_bg_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    if van_bg is not None:
        Divide(LHSWorkspace=van_bg, RHSWorkspace=van_corrected, OutputWorkspace=van_bg)
        vanadium_bg_title += '_normalized'
        save_banks(InputWorkspace=van_bg, Filename=nexus_filename, Title=vanadium_bg_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    ConvertUnits(InputWorkspace=sam_wksp, OutputWorkspace=sam_wksp, Target='Wavelength', EMode='Elastic')
    sam_corrected = 'sam_corrected'
    if sam_abs_corr:
        if sam_abs_corr['Type'] == 'Carpenter' or sam_ms_corr['Type'] == 'Carpenter':
            CarpenterSampleCorrection(InputWorkspace=sam_wksp, OutputWorkspace=sam_corrected, CylinderSampleRadius=sample['Geometry']['Radius'])
        elif sam_abs_corr['Type'] == 'Mayers' or sam_ms_corr['Type'] == 'Mayers':
            if sam_ms_corr['Type'] == 'Mayers':
                MayersSampleCorrection(InputWorkspace=sam_wksp, OutputWorkspace=sam_corrected, MultipleScattering=True)
            else:
                MayersSampleCorrection(InputWorkspace=sam_wksp, OutputWorkspace=sam_corrected, MultipleScattering=False)
        else:
            print('NO SAMPLE absorption or multiple scattering!')
            CloneWorkspace(InputWorkspace=sam_wksp, OutputWorkspace=sam_corrected)
        ConvertUnits(InputWorkspace=sam_corrected, OutputWorkspace=sam_corrected, Target='MomentumTransfer', EMode='Elastic')
        sample_title += '_ms_abs_corrected'
        save_banks(InputWorkspace=sam_corrected, Filename=nexus_filename, Title=sample_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    else:
        CloneWorkspace(InputWorkspace=sam_wksp, OutputWorkspace=sam_corrected)
    mtd[sam_corrected] = nvan_atoms / natoms * mtd[sam_corrected]
    ConvertUnits(InputWorkspace=sam_corrected, OutputWorkspace=sam_corrected, Target='MomentumTransfer', EMode='Elastic')
    sample_title += '_norm_by_atoms'
    save_banks(InputWorkspace=sam_corrected, Filename=nexus_filename, Title=sample_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    van_material = mtd[van_corrected].sample().getMaterial()
    sigma_v = van_material.totalScatterXSection()
    prefactor = sigma_v / (4.0 * np.pi)
    msg = 'Total scattering cross-section of Vanadium:{} sigma_v / 4*pi: {}'
    print(msg.format(sigma_v, prefactor))
    mtd[sam_corrected] = prefactor * mtd[sam_corrected]
    sample_title += '_multiply_by_vanSelfScat'
    save_banks(InputWorkspace=sam_corrected, Filename=nexus_filename, Title=sample_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    ConvertUnits(InputWorkspace=sam_corrected, OutputWorkspace=sam_corrected, Target='Wavelength', EMode='Elastic')
    if sam_inelastic_corr['Type'] == 'Placzek':
        if sam_material is None:
            error = 'For Placzek correction, must specifiy a sample material.'
            raise Exception(error)
        for sam_scan in sample['Runs']:
            sam_incident_wksp = 'sam_incident_wksp'
            sam_inelastic_opts = sample['InelasticCorrection']
            lambda_binning_fit = sam_inelastic_opts['LambdaBinningForFit']
            lambda_binning_calc = sam_inelastic_opts['LambdaBinningForCalc']
            GetIncidentSpectrumFromMonitor(Filename=facility_file_format % (instr, sam_scan), OutputWorkspace=sam_incident_wksp)
            fit_type = sample['InelasticCorrection']['FitSpectrumWith']
            FitIncidentSpectrum(InputWorkspace=sam_incident_wksp, OutputWorkspace=sam_incident_wksp, FitSpectrumWith=fit_type, BinningForFit=lambda_binning_fit, BinningForCalc=lambda_binning_calc)
            sam_placzek = 'sam_placzek'
            SetSample(InputWorkspace=sam_incident_wksp, Material={'ChemicalFormula': str(sam_material), 'SampleMassDensity': str(sam_mass_density)})
            CalculatePlaczekSelfScattering(IncidentWorkspace=sam_incident_wksp, ParentWorkspace=sam_corrected, OutputWorkspace=sam_placzek, L1=19.5, L2=alignAndFocusArgs['L2'], Polar=alignAndFocusArgs['Polar'])
            ConvertToHistogram(InputWorkspace=sam_placzek, OutputWorkspace=sam_placzek)

        for wksp in [sam_placzek, sam_corrected]:
            ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target='MomentumTransfer', EMode='Elastic')
            Rebin(InputWorkspace=wksp, OutputWorkspace=wksp, Params=binning, PreserveEvents=True)

        save_banks(InputWorkspace=sam_placzek, Filename=nexus_filename, Title='sample_placzek', OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
        for wksp in [sam_placzek, sam_corrected]:
            ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target='MomentumTransfer', EMode='Elastic')

        Minus(LHSWorkspace=sam_corrected, RHSWorkspace=sam_placzek, OutputWorkspace=sam_corrected)
        for wksp in [sam_placzek, sam_corrected]:
            ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp, Target='MomentumTransfer', EMode='Elastic')

        sample_title += '_placzek_corrected'
        save_banks(InputWorkspace=sam_corrected, Filename=nexus_filename, Title=sample_title, OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    print('sam:', mtd[sam_corrected].id())
    print('van:', mtd[van_corrected].id())
    if alignAndFocusArgs['PreserveEvents']:
        CompressEvents(InputWorkspace=sam_corrected, OutputWorkspace=sam_corrected)
    fq_banks_wksp = 'FQ_banks_wksp'
    CloneWorkspace(InputWorkspace=sam_corrected, OutputWorkspace=fq_banks_wksp)
    material = mtd[sam_corrected].sample().getMaterial()
    if material.name() is None or len(material.name().strip()) == 0:
        raise RuntimeError('Sample material was not set')
    bcoh_avg_sqrd = material.cohScatterLength() * material.cohScatterLength()
    btot_sqrd_avg = material.totalScatterLengthSqrd()
    laue_monotonic_diffuse_scat = btot_sqrd_avg / bcoh_avg_sqrd
    sq_banks_wksp = 'SQ_banks_wksp'
    CloneWorkspace(InputWorkspace=sam_corrected, OutputWorkspace=sq_banks_wksp)
    save_banks(InputWorkspace=fq_banks_wksp, Filename=nexus_filename, Title='FQ_banks', OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    save_banks(InputWorkspace=sq_banks_wksp, Filename=nexus_filename, Title='SQ_banks', OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    fq_filename = title + '_fofq_banks_corrected.nxs'
    save_banks(InputWorkspace=fq_banks_wksp, Filename=fq_filename, Title='FQ_banks', OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    sq_filename = title + '_sofq_banks_corrected.nxs'
    save_banks(InputWorkspace=sq_banks_wksp, Filename=sq_filename, Title='SQ_banks', OutputDir=OutputDir, GroupingWorkspace=grp_wksp, Binning=binning)
    print('<b>^2:', bcoh_avg_sqrd)
    print('<b^2>:', btot_sqrd_avg)
    print('Laue term:', laue_monotonic_diffuse_scat)
    print('sample total xsection:', mtd[sam_corrected].sample().getMaterial().totalScatterXSection())
    print('vanadium total xsection:', mtd[van_corrected].sample().getMaterial().totalScatterXSection())
    ConvertUnits(InputWorkspace=sam_corrected, OutputWorkspace=sam_corrected, Target='TOF', EMode='Elastic')
    ConvertToHistogram(InputWorkspace=sam_corrected, OutputWorkspace=sam_corrected)
    xmin, xmax = get_each_spectra_xmin_xmax(mtd[sam_corrected])
    CropWorkspaceRagged(InputWorkspace=sam_corrected, OutputWorkspace=sam_corrected, Xmin=xmin, Xmax=xmax)
    xmin_rebin = min(xmin)
    xmax_rebin = max(xmax)
    tof_binning = ('{xmin},-0.01,{xmax}').format(xmin=xmin_rebin, xmax=xmax_rebin)
    Rebin(InputWorkspace=sam_corrected, OutputWorkspace=sam_corrected, Params=tof_binning)
    SaveGSS(InputWorkspace=sam_corrected, Filename=os.path.join(os.path.abspath(OutputDir), title + '.gsa'), SplitFiles=False, Append=False, MultiplyByBinWidth=True, Format='SLOG', ExtendedHeader=True)
    return mtd[sam_corrected]