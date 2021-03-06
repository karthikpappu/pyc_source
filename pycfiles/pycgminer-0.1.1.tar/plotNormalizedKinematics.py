# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:/Users/HLS501/Documents/Programming/API/pyCGM2/pyCGM2/Apps/DataProcessing\plotNormalizedKinematics.py
# Compiled at: 2019-03-07 07:04:50
__doc__ = 'Nexus Operation : **plotNormalizedKinematics**\n\nThe script displays Gait-Normalized kinematics\n\n:param -ps, --pointSuffix [string]: suffix adds to the vicon nomenclature outputs\n:param -c, --consistency [bool]: display consistency plot ( ie : all gait cycle) instead of a descriptive statistics view\n:param -nd, --normativeData [string]: Normative data set ( choice: Schwartz2008 [DEFAULT] or Pinzone2014)\n:param -ndm, --normativeDataModality [string]: modalities associated with the selected normative dataset. (choices: if  Schwartz2008: VerySlow,Slow,Free[DEFAULT],Fast,VeryFast.  if Pinzone2014 : CentreOne,CentreTwo)\n\n\nExamples:\n    In the script argument box of a python nexus operation, you can edit:\n\n    >>>  -normativeData=Schwartz2008 --normativeDataModality=VeryFast\n    (your gait panel will display as normative data, results from the modality VeryFast of the nomative dataset collected by Schwartz2008)\n\n'
import logging, argparse, matplotlib.pyplot as plt, traceback, pyCGM2
from pyCGM2 import log
log.setLoggingLevel(logging.INFO)
import ViconNexus
from pyCGM2 import enums
from pyCGM2.Lib import analysis
from pyCGM2.Lib import plot
from pyCGM2.Report import normativeDatasets
from pyCGM2.Nexus import nexusTools
from pyCGM2.Utils import files

def main(args):
    NEXUS = ViconNexus.ViconNexus()
    NEXUS_PYTHON_CONNECTED = NEXUS.Client.IsConnected()
    if NEXUS_PYTHON_CONNECTED:
        normativeData = {'Author': args.normativeData, 'Modality': args.normativeDataModality}
        if normativeData['Author'] == 'Schwartz2008':
            chosenModality = normativeData['Modality']
            nds = normativeDatasets.Schwartz2008(chosenModality)
        elif normativeData['Author'] == 'Pinzone2014':
            chosenModality = normativeData['Modality']
            nds = normativeDatasets.Pinzone2014(chosenModality)
        consistencyFlag = True if args.consistency else False
        pointSuffix = args.pointSuffix
        DEBUG = False
        if DEBUG:
            DATA_PATH = 'C:\\Users\\HLS501\\Documents\\VICON DATA\\pyCGM2-Data\\Release Tests\\CGM1\\lowerLimbTrunk\\'
            modelledFilenameNoExt = 'PN01NORMSS02'
            NEXUS.OpenTrial(str(DATA_PATH + modelledFilenameNoExt), 30)
        else:
            DATA_PATH, modelledFilenameNoExt = NEXUS.GetTrialName()
        modelledFilename = modelledFilenameNoExt + '.c3d'
        logging.info('data Path: ' + DATA_PATH)
        logging.info('file: ' + modelledFilename)
        subjects = NEXUS.GetSubjectNames()
        subject = nexusTools.checkActivatedSubject(NEXUS, subjects)
        logging.info('Subject name : ' + subject)
        model = files.loadModel(DATA_PATH, subject)
        modelVersion = model.version
        analysisInstance = analysis.makeAnalysis(DATA_PATH, [modelledFilename], pointLabelSuffix=pointSuffix)
        if not consistencyFlag:
            if model.m_bodypart in [enums.BodyPart.LowerLimb, enums.BodyPart.LowerLimbTrunk, enums.BodyPart.FullBody]:
                plot.plot_DescriptiveKinematic(DATA_PATH, analysisInstance, 'LowerLimb', nds, pointLabelSuffix=pointSuffix, exportPdf=True, outputName=modelledFilename)
            if model.m_bodypart in [enums.BodyPart.LowerLimbTrunk, enums.BodyPart.FullBody]:
                plot.plot_DescriptiveKinematic(DATA_PATH, analysisInstance, 'Trunk', nds, pointLabelSuffix=pointSuffix, exportPdf=True, outputName=modelledFilename)
            if model.m_bodypart in [enums.BodyPart.UpperLimb, enums.BodyPart.FullBody]:
                pass
        else:
            if model.m_bodypart in [enums.BodyPart.LowerLimb, enums.BodyPart.LowerLimbTrunk, enums.BodyPart.FullBody]:
                plot.plot_ConsistencyKinematic(DATA_PATH, analysisInstance, bodyPart, 'LowerLimb', nds, pointLabelSuffix=pointSuffix, exportPdf=True, outputName=modelledFilename)
            if model.m_bodypart in [enums.BodyPart.LowerLimbTrunk, enums.BodyPart.FullBody]:
                plot.plot_ConsistencyKinematic(DATA_PATH, analysisInstance, bodyPart, 'Trunk', nds, pointLabelSuffix=pointSuffix, exportPdf=True, outputName=modelledFilename)
            if model.m_bodypart in [enums.BodyPart.UpperLimb, enums.BodyPart.FullBody]:
                pass
    else:
        raise Exception('NO Nexus connection. Turn on Nexus')


if __name__ == '__main__':
    plt.close('all')
    parser = argparse.ArgumentParser(description='CGM Gait Processing')
    parser.add_argument('-nd', '--normativeData', type=str, help='normative Data set (Schwartz2008 or Pinzone2014)', default='Schwartz2008')
    parser.add_argument('-ndm', '--normativeDataModality', type=str, help='if Schwartz2008 [VerySlow,SlowFree,Fast,VeryFast] - if Pinzone2014 [CentreOne,CentreTwo]', default='Free')
    parser.add_argument('-ps', '--pointSuffix', type=str, help='suffix of model outputs')
    parser.add_argument('-c', '--consistency', action='store_true', help='consistency plots')
    args = parser.parse_args()
    try:
        main(args)
    except Exception as errormsg:
        print 'Error message: %s' % errormsg
        traceback.print_exc()
        raise