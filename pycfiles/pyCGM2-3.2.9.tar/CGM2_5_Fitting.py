# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/CGM2_5\CGM2_5_Fitting.py
# Compiled at: 2019-03-07 07:04:50
"""Nexus Operation : **CGM2.5 Fitting**

:param --proj [string]: define in which coordinate system joint moment will be expressed (Choice : Distal, Proximal, Global)
:param -md, --markerDiameter [int]: marker diameter
:param -ps, --pointSuffix [string]: suffix adds to the vicon nomenclature outputs
:param --check [bool]: add "cgm2.5" as point suffix
:param --noIk [bool]: disable inverse kinematics

Examples:
    In the script argument box of a python nexus operation, you can edit:

    >>> --proj=Global --noIk
    (means you disable the inverse kinematic solver and joint moments will be expressed into the Global Coordinate system, and )

"""
import os, traceback, logging, argparse, matplotlib.pyplot as plt, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
from pyCGM2.Utils import files
from pyCGM2.Nexus import nexusFilters, nexusUtils, nexusTools
from pyCGM2.Configurator import CgmArgsManager
from pyCGM2.Lib.CGM import cgm2_5

def main(args):
    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()
    if NEXUS_PYTHON_CONNECTED:
        if os.path.isfile(pyCGM2.PYCGM2_APPDATA_PATH + 'CGM2_5-pyCGM2.settings'):
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM2_5-pyCGM2.settings')
        else:
            settings = files.openFile(pyCGM2.PYCGM2_SETTINGS_FOLDER, 'CGM2_5-pyCGM2.settings')
        argsManager = CgmArgsManager.argsManager_cgm(settings, args)
        markerDiameter = argsManager.getMarkerDiameter()
        pointSuffix = argsManager.getPointSuffix('cgm2.5')
        momentProjection = argsManager.getMomentProjection()
        ik_flag = argsManager.enableIKflag()
        DEBUG = False
        if DEBUG:
            DATA_PATH = pyCGM2.TEST_DATA_PATH + 'Release Tests\\CGM2.5\\fullBody\\'
            reconstructFilenameLabelledNoExt = 'dynamic'
            NEXUS.OpenTrial(str(DATA_PATH + reconstructFilenameLabelledNoExt), 10)
            args.noIk = False
        else:
            DATA_PATH, reconstructFilenameLabelledNoExt = NEXUS.GetTrialName()
        reconstructFilenameLabelled = reconstructFilenameLabelledNoExt + '.c3d'
        logging.info('data Path: ' + DATA_PATH)
        logging.info('reconstructed file: ' + reconstructFilenameLabelled)
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.checkActivatedSubject(NEXUS, subjects)
        logging.info('Subject name : ' + subject)
        model = files.loadModel(DATA_PATH, subject)
        logging.info('loaded model : %s' % model.version)
        if model.version != 'CGM2.5':
            raise Exception('%s-pyCGM2.model file was not calibrated from the CGM2.4e calibration pipeline' % subject)
        translators = files.getTranslators(DATA_PATH, 'CGM2_5.translators')
        if not translators:
            translators = settings['Translators']
        ikWeight = files.getIKweightSet(DATA_PATH, 'CGM2_4.ikw')
        if not ikWeight:
            ikWeight = settings['Fitting']['Weight']
        mfpa = nexusTools.getForcePlateAssignment(NEXUS)
        finalAcqGait = cgm2_5.fitting(model, DATA_PATH, reconstructFilenameLabelled, translators, settings, ik_flag, markerDiameter, pointSuffix, mfpa, momentProjection)
        nexusFilters.NexusModelFilter(NEXUS, model, finalAcqGait, subject, pointSuffix).run()
        nexusTools.createGeneralEvents(NEXUS, subject, finalAcqGait, ['Left-FP', 'Right-FP'])
        if DEBUG:
            NEXUS.SaveTrial(30)
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CGM2-5 Fitting')
    parser.add_argument('--proj', type=str, help='Moment Projection. Choice : Distal, Proximal, Global')
    parser.add_argument('-md', '--markerDiameter', type=float, help='marker diameter')
    parser.add_argument('-ps', '--pointSuffix', type=str, help='suffix of model outputs')
    parser.add_argument('--check', action='store_true', help='force model output suffix')
    parser.add_argument('--noIk', action='store_true', help='cancel inverse kinematic')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise