# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/CGM2_2\CGM2_2_Fitting.py
# Compiled at: 2019-03-07 07:04:49
__doc__ = 'Nexus Operation : **CGM2.2 Fitting**\n\n:param --proj [string]: define in which coordinate system joint moment will be expressed (Choice : Distal, Proximal, Global)\n:param -mfpa [string]: manual force plate assignement. (Choice: combinaison of  X, L, R depending of your force plate number)\n:param -md, --markerDiameter [int]: marker diameter\n:param -ps, --pointSuffix [string]: suffix adds to the vicon nomenclature outputs\n:param --check [bool]: add "cgm2.2" as point suffix\n\n\nExamples:\n    In the script argument box of a python nexus operation, you can edit:\n\n    >>> --proj=Global\n    (means joint moments will be expressed into the Global Coordinate system)\n\n'
import os, traceback, logging, argparse, matplotlib.pyplot as plt, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
from pyCGM2.Utils import files
from pyCGM2.Nexus import nexusFilters, nexusUtils, nexusTools
from pyCGM2.Configurator import CgmArgsManager
from pyCGM2.Lib.CGM import cgm2_2

def main(args):
    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()
    if NEXUS_PYTHON_CONNECTED:
        if os.path.isfile(pyCGM2.PYCGM2_APPDATA_PATH + 'CGM2_2-pyCGM2.settings'):
            settings = files.openFile(pyCGM2.PYCGM2_APPDATA_PATH, 'CGM2_2-pyCGM2.settings')
        else:
            settings = files.openFile(pyCGM2.PYCGM2_SETTINGS_FOLDER, 'CGM2_2-pyCGM2.settings')
        argsManager = CgmArgsManager.argsManager_cgm(settings, args)
        markerDiameter = argsManager.getMarkerDiameter()
        pointSuffix = argsManager.getPointSuffix('cgm2.2')
        momentProjection = argsManager.getMomentProjection()
        DEBUG = False
        if DEBUG:
            DATA_PATH = pyCGM2.TEST_DATA_PATH + 'CGM3\\Salford_healthy_DataCollection\\PN01OP01S01\\'
            reconstructFilenameLabelledNoExt = 'PN01OP01S01STAT-copy'
            NEXUS.OpenTrial(str(DATA_PATH + reconstructFilenameLabelledNoExt), 10)
        else:
            DATA_PATH, reconstructFilenameLabelledNoExt = NEXUS.GetTrialName()
        reconstructFilenameLabelled = reconstructFilenameLabelledNoExt + '.c3d'
        logging.info('data Path: ' + DATA_PATH)
        logging.info('calibration file: ' + reconstructFilenameLabelled)
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.checkActivatedSubject(NEXUS, subjects)
        logging.info('Subject name : ' + subject)
        model = files.loadModel(DATA_PATH, subject)
        logging.info('loaded model : %s' % model.version)
        if model.version != 'CGM2.2':
            raise Exception('%s-pyCGM2.model file was not calibrated from the CGM2.2 calibration pipeline' % subject)
        translators = files.getTranslators(DATA_PATH, 'CGM2_2.translators')
        if not translators:
            translators = settings['Translators']
        ikWeight = files.getIKweightSet(DATA_PATH, 'CGM2_2.ikw')
        if not ikWeight:
            ikWeight = settings['Fitting']['Weight']
        mfpa = nexusTools.getForcePlateAssignment(NEXUS)
        acqIK = cgm2_2.fitting(model, DATA_PATH, reconstructFilenameLabelled, translators, settings, markerDiameter, pointSuffix, mfpa, momentProjection)
        nexusFilters.NexusModelFilter(NEXUS, model, acqIK, subject, pointSuffix).run()
        nexusTools.createGeneralEvents(NEXUS, subject, acqIK, ['Left-FP', 'Right-FP'])
        if DEBUG:
            NEXUS.SaveTrial(30)
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CGM2-2 Fitting')
    parser.add_argument('--proj', type=str, help='Moment Projection. Choice : Distal, Proximal, Global')
    parser.add_argument('-md', '--markerDiameter', type=float, help='marker diameter')
    parser.add_argument('-ps', '--pointSuffix', type=str, help='suffix of model outputs')
    parser.add_argument('--check', action='store_true', help='force model output suffix')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise