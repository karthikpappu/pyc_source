# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\tikon\Cultivo\ModExtern\DSSAT\DSSAT.py
# Compiled at: 2017-02-17 15:05:05
# Size of source mod 2**32: 14144 bytes
import datetime as ft, glob, numpy as np, os, re
from tikon.Cultivo.ModExtern.DSSAT import fileC, fileS, fileX, fileW
import tikon.Controles as Ctrl
from tikon.Cultivo.Suelo import Suelo
dir_DSSAT = Ctrl.dirs_modelos['DSSAT']

def gen_ingr(nombre, cultivo=None, suelo=None, meteo=None, manejo=None):
    fileC.escribir(nombre, cultivo)
    fileS.escribir(nombre, suelo)
    fileX.escribir(nombre, manejo, cultivo=nombre, suelo=nombre, meteo=nombre)
    fileW.escribir(nombre, meteo)


def leer_egr(directorio):
    [
     'ET', 'Evaluate', 'Mulch', 'PlantGro', 'PlantN', 'SoilNi', 'SoilOrg', 'SoilTemp', 'SoilWat', 'Weather']


def leer_datos_egr(d, dic_vars):
    """

    :param d:
    :type d:
    :return:
    :rtype:

    """
    with open(d, 'r', encoding='UTF-8') as (d):
        l_vars = next(x for x in d.readline() if re.match('@', x))


def importar_suelo(archivo, nombre):
    """
    Esta función importa un suelo DSSAT en particular.

    :param archivo: El archivo donde se ubica el suelo.
    :type archivo: str

    :param nombre: El nombre del suelo.
    :type nombre: str

    :return: El objeto de suelo Tiko'n correspondiendo al document DSSAT.
    :rtype: Suelo

    """
    if not len(os.path.splitdrive(archivo)[0]):
        archivo = os.path.join(dir_DSSAT, archivo)
    if not len(os.path.splitext(archivo)[1]):
        archivo += '.SOL'
    dic_info, dic_coefs = fileS.cargar_suelo(nombre=nombre, archivo=archivo)
    suelo = Suelo(nombre=nombre, proyecto='Suelos DSSAT')
    suelo.receta['info'].update(dic_info)
    for ll, v in dic_coefs.items:
        suelo.especificar_apriori(rango=(v, v), certidumbre=1)

    return suelo


def importar_todos_suelos(directorio=os.path.join(dir_DSSAT, 'Soil')):
    """
    Esta función importa todos los suelos disponibles en DSSAT.

    :param directorio: El directorio del cual hay que importar los suelos.
    :type directorio: str

    """
    l_archivos = glob.glob(('{}/**/*.SOL'.format(directorio)), recursive=True)
    for a in l_archivos:
        l_nombres, l_d_info, l_d_coefs = fileS.cargar_suelos_doc(archivo=a)
        for n, dic in enumerate(l_d_coefs):
            suelo = Suelo(nombre=(l_nombres[n]), proyecto='Suelos DSSAT')
            suelo.receta['info'].update(l_d_info)
            for ll, v in dic.items:
                suelo.especificar_apriori(rango=(v, v), certidumbre=1)

            suelo.guardar(especificados=True)


class Experimento(object):

    def __init__(símismo, carpeta, suelo, variedad, meteo, cultivo, manejo):
        símismo.directorio = carpeta
        símismo.variedad = variedad
        símismo.suelo = suelo
        símismo.meteo = meteo
        símismo.cultivo = cultivo
        símismo.manejo = manejo

    def gen_ingresos(símismo):

        def convertir(obj, documento_conv):
            conversiones = {}
            with open(os.path.join(os.getcwd(), 'Cultivo', 'ModExtern', documento_conv)) as (d):
                doc = d.readlines()
            col = doc[0].replace('\n', '').split(',').index('DSSAT')
            for núm_línea, línea in enumerate(doc[1:]):
                datos = línea.replace('\n', '').split(',')
                var_tikon = datos[0]
                var_dssat = datos[col]
                conversiones[var_tikon] = var_dssat

            if type(obj) is FileS:
                documento = FileS()
            else:
                if type(obj) is FileW:
                    documento = FileW()
                else:
                    if type(obj) is FileC:
                        documento = FileC()
                    else:
                        if type(obj) is dict:
                            return conversiones
                        else:
                            return False
            for var_tikon in obj.dic:
                documento.dic[conversiones[var_tikon]] = obj.dic[var_tikon]
                if var_tikon == 'Fecha':
                    fecha = obj.dic[var_tikon]
                    if type(fecha) is str:
                        f = ft.datetime(1, 1, 1)
                        fecha = f.strptime(fecha, '%Y-%m-%d')
                    documento.dic[conversiones[var_tikon]] = str(fecha.date().year)[-2:] + fecha.date().strftime('%j')

            return documento

        filec = convertir(símismo.variedad, 'Variables_variedades.csv')
        files = convertir(símismo.suelo, 'Variables_suelo.csv')
        filew = convertir(símismo.meteo, 'Variables_meteo.csv')
        filec.escribir()
        files.escribir()
        filew.escribir()
        filex = FileX()
        filex.dic['EXP.DETAILS'] = 'Autogenerado por Tikon el %d' % ft.datetime.now().strftime('%d-%m-%Y %H:%M')
        filex.dic['GENERAL']['People'] = 'Tikon fue desarrollado por Julien Malard y Marcela Rojas Díaz.'
        filex.dic['GENERAL']['Address'] = 'Universidad McGill, Dept de Biorecursos, Saint-Anne-de-Bellevue, Canadá'
        filex.dic['GENERAL']['NOTES'] = 'Contacto: julien.malard@mail.mcgill.ca'
        filex.dic['GENERAL']['PAREA'] = símismo.manejo['Área']
        filex.dic['GENERAL']['PRNO'] = símismo.manejo['Surcos']
        filex.dic['GENERAL']['PLDR'] = símismo.manejo['Long_surcos']
        filex.dic['TREATMENTS']['R'] = 1
        filex.dic['TREATMENTS']['O'] = 0
        filex.dic['TREATMENTS']['O'] = 0
        for i in ('CU', 'FL', 'SA', 'IC', 'MP', 'MI', 'MF', 'MR', 'MC', 'MT', 'ME',
                  'MH', 'SM'):
            filex.dic['TREATMENTS'][i] = 1

        filex.dic['CULTIVARS']['CR'] = símismo.cultivo.cód_cultivo
        filex.dic['CULTIVARS']['INGEN'] = filec.dic['VAR#']
        filex.dic['CULTIVARS']['CNAME'] = filec.dic['VRNAME']
        filex.dic['FIELDS']['ID_FIELD'] = símismo.manejo.nombre[:4] + '0001'
        filex.dic['FIELDS']['WSTA'] = filew.dic['INSI'] + 'TKON'
        filex.dic['FIELDS']['PLOB'] = símismo.manejo['Pendiente_orientación']
        filex.dic['FIELDS']['FLST'] = símismo.manejo['Piedras']
        filex.dic['FIELDS']['SLTX'] = files.dic['SLTX']
        filex.dic['FIELDS']['SLDP'] = files.dic['SLDP']
        filex.dic['FIELDS']['ID_SOIL'] = files.dic['ID_SOIL']
        manejo = símismo.manejo['Manejo']
        for sección in ('PLANTING DETAILS', 'FERTILIZERS (INORGANIC)', 'RESIDUES AND ORGANIC FERTILIZER',
                        'IRRIGATION AND WATER MANAGEMENT', 'TILLAGE', 'HARVEST DETAILS'):
            conv_dssat = convertir(filex.dic[sección], 'Variables_manejo.csv')
            for var in conv_dssat:
                if var in manejo and conv_dssat[var] in filex.dic[sección]:
                    filex.dic[sección][conv_dssat[var]] = manejo[var]

        filex.dic['SIMULATION CONTROLS']['GENERAL'] = 'GE'
        filex.dic['SIMULATION CONTROLS']['NYERS'] = 1
        filex.dic['SIMULATION CONTROLS']['NREPS'] = 1
        filex.dic['SIMULATION CONTROLS']['START'] = 'S'
        filex.dic['SIMULATION CONTROLS']['SDATE'] = manejo['Fecha_siembra']
        filex.dic['SIMULATION CONTROLS']['RSEED'] = 88
        filex.dic['SIMULATION CONTROLS']['OPTIONS'] = 'OP'
        filex.dic['SIMULATION CONTROLS']['WATER'] = 'Y'
        filex.dic['SIMULATION CONTROLS']['NITRO'] = 'Y'
        filex.dic['SIMULATION CONTROLS']['SYMBI'] = 'Y'
        filex.dic['SIMULATION CONTROLS']['PHOSP'] = 'Y'
        filex.dic['SIMULATION CONTROLS']['POTAS'] = 'Y'
        filex.dic['SIMULATION CONTROLS']['DISES'] = 'N'
        filex.dic['SIMULATION CONTROLS']['CHEM'] = 'N'
        filex.dic['SIMULATION CONTROLS']['CO2'] = 'M'
        filex.dic['SIMULATION CONTROLS']['METHODS'] = 'ME'
        filex.dic['SIMULATION CONTROLS']['WTHER'] = 'M'
        filex.dic['SIMULATION CONTROLS']['INCON'] = 'M'
        filex.dic['SIMULATION CONTROLS']['LIGHT'] = 'E'
        filex.dic['SIMULATION CONTROLS']['EVAPO'] = 'R'
        filex.dic['SIMULATION CONTROLS']['INFIL'] = 'S'
        filex.dic['SIMULATION CONTROLS']['PHOTO'] = 'L'
        filex.dic['SIMULATION CONTROLS']['HYDRO'] = 'R'
        filex.dic['SIMULATION CONTROLS']['NSWIT'] = 1
        filex.dic['SIMULATION CONTROLS']['MESOM'] = 'G'
        filex.dic['SIMULATION CONTROLS']['MESEV'] = 'S'
        filex.dic['SIMULATION CONTROLS']['MESOL'] = 2
        filex.dic['SIMULATION CONTROLS']['MANAGEMENT'] = 'MG'
        filex.dic['SIMULATION CONTROLS']['PLANT'] = 'R'
        if manejo['Irrig']:
            if manejo['Irrig_auto']:
                filex.dic['SIMULATION CONTROLS']['IRRIG'] = 'A'
            else:
                filex.dic['SIMULATION CONTROLS']['IRRIG'] = 'R'
        else:
            filex.dic['SIMULATION CONTROLS']['IRRIG'] = 'N'
        filex.dic['SIMULATION CONTROLS']['FERTI'] = 'R'
        filex.dic['SIMULATION CONTROLS']['RESID'] = 'R'
        filex.dic['SIMULATION CONTROLS']['HARVS'] = 'M'
        filex.dic['SIMULATION CONTROLS']['OUTPUTS'] = 'OU'
        filex.dic['SIMULATION CONTROLS']['FNAME'] = 'N'
        filex.dic['SIMULATION CONTROLS']['OVVEW'] = 'Y'
        filex.dic['SIMULATION CONTROLS']['SUMRY'] = 'Y'
        filex.dic['SIMULATION CONTROLS']['FROPT'] = 'N'
        filex.dic['SIMULATION CONTROLS']['GROUT'] = 'N'
        filex.dic['SIMULATION CONTROLS']['CAOUT'] = 'N'
        filex.dic['SIMULATION CONTROLS']['WAOUT'] = 'N'
        filex.dic['SIMULATION CONTROLS']['NIOUT'] = 'N'
        filex.dic['SIMULATION CONTROLS']['MIOUT'] = 'N'
        filex.dic['SIMULATION CONTROLS']['DIOUT'] = 'N'
        filex.dic['SIMULATION CONTROLS']['VBOSE'] = 0
        filex.dic['SIMULATION CONTROLS']['CHOUT'] = 'N'
        filex.dic['SIMULATION CONTROLS']['OPOUT'] = 'N'
        filex.dic['SIMULATION CONTROLS']['PLANTING'] = 'PL'
        filex.dic['SIMULATION CONTROLS']['PFRST'] = -99
        filex.dic['SIMULATION CONTROLS']['PLAST'] = -99
        filex.dic['SIMULATION CONTROLS']['PH2OL'] = -99
        filex.dic['SIMULATION CONTROLS']['PH2OU'] = -99
        filex.dic['SIMULATION CONTROLS']['PH2OD'] = -99
        filex.dic['SIMULATION CONTROLS']['PSTMX'] = -99
        filex.dic['SIMULATION CONTROLS']['PSTMN'] = -99
        filex.dic['SIMULATION CONTROLS']['IRRIGATION'] = 'IR'
        filex.dic['SIMULATION CONTROLS']['IMDEP'] = '30'
        filex.dic['SIMULATION CONTROLS']['ITHRL'] = '50'
        filex.dic['SIMULATION CONTROLS']['ITHRU'] = '100'
        filex.dic['SIMULATION CONTROLS']['IROFF'] = -99
        filex.dic['SIMULATION CONTROLS']['IMETH'] = 'IR004'
        if manejo['Irrig_auto']:
            filex.dic['SIMULATION CONTROLS']['IRAMT'] = -99
        else:
            filex.dic['SIMULATION CONTROLS']['IRAMT'] = manejo['Cant_irrig_auto']
        filex.dic['SIMULATION CONTROLS']['IREFF'] = 1
        filex.dic['SIMULATION CONTROLS']['NITROGEN'] = 'NI'
        filex.dic['SIMULATION CONTROLS']['NMDEP'] = -99
        filex.dic['SIMULATION CONTROLS']['NMTHR'] = -99
        filex.dic['SIMULATION CONTROLS']['NAMNT'] = -99
        filex.dic['SIMULATION CONTROLS']['NCODE'] = -99
        filex.dic['SIMULATION CONTROLS']['NAOFF'] = -99
        filex.dic['SIMULATION CONTROLS']['RESIDUES'] = 'RE'
        filex.dic['SIMULATION CONTROLS']['RIPCN'] = 100
        filex.dic['SIMULATION CONTROLS']['RTIME'] = -99
        filex.dic['SIMULATION CONTROLS']['RIDEP'] = 20
        filex.dic['SIMULATION CONTROLS']['HARVEST'] = 'HA'
        filex.dic['SIMULATION CONTROLS']['HFRST'] = 0
        filex.dic['SIMULATION CONTROLS']['HLAST'] = -99
        filex.dic['SIMULATION CONTROLS']['HPCNP'] = 100
        filex.dic['SIMULATION CONTROLS']['HPCNR'] = 0
        filex.escribir(os.path.join(símismo.directorio, 'TIKON.', símismo.cultivo.cód_cultivo, 'X'))
        símismo.gen_dssbatch()

    def gen_dssbatch(símismo):
        with open('DSSBatchv46.txt', 'r') as (d):
            esquema = []
            for línea in d:
                esquema.append(línea)

        esquema.append('\n')
        dic = {'Cultivo':símismo.cultivo.cultivo, 
         'FILEX':os.path.join(símismo.directorio, 'TIKON.', símismo.cultivo.cód_cultivo, 'X')}
        for núm_lín, línea in enumerate(esquema):
            if '{' in línea:
                esquema[núm_lín] = (línea.format)(**dic)

        esquema = ''.join(esquema)
        with open(os.path.join(símismo.directorio, 'TIKON.', símismo.cultivo.cód_cultivo, 'X'), 'w') as (d):
            d.write(''.join(esquema))