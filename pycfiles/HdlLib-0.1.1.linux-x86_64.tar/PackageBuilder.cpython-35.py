# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/SysGen/PackageBuilder.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 3312 bytes
import os, sys, logging, shutil
from HdlLib.SysGen import HDLEditor as HDL

class PackageBuilder:

    def __init__(self):
        """
                Gather constants and types so as to build a HDL package synthesizable library elements.
                """
        self.Package = {'Constants': {}, 'Types': {}, 'TypeImport': {}, 'EmptyPkg': []}
        self.PkgVars = {}
        self.PkgName = 'Top'

    def GetTopPackName(self):
        """
                Return abstract name of top file if module is abstract.
                """
        return '{0}.vhd'.format(self.PkgName)

    def GenPackage(self, Name, OutputDir):
        """
                Create a file named 'Name' into 'OutputDir' and write package information into it.
                """
        if len(self.Package):
            self.PkgName = Name + '_pkg'
            with open(os.path.join(OutputDir, self.GetTopPackName()), 'w+') as (PKGFILE):
                PKGFILE.write(HDL.Libraries(['IEEE']))
                PKGFILE.write(HDL.Packages(['IEEE.std_logic_1164']))
                PKGFILE.write('\n')
                for CName, Const in self.Package['Constants'].items():
                    if CName in self.PkgVars:
                        Const.InitVal = self.PkgVars[CName]

                TypesList = []
                EmptyPkg = []
                for NewType, TypeDesc in self.Package['TypeImport'].items():
                    SubSize, SubType, Pkg, UsedConst = TypeDesc
                    TypesList.append(HDL.ArrayType(NewType, SubSize, SubType, ArraySize=None))
                    for CName in UsedConst:
                        if CName in self.Params:
                            self.Package['Constants'][CName] = self.Params[CName].HDLFormat()
                        elif CName not in self.Package['Constants']:
                            logging.error("Constant '{0}' not in parameters or constants of '{1}'".format(CName, self))

                TypesList += [HDL.ArrayType(TName, eval(TSize, self.PkgVars), TType) for TName, TSize, TType in list(self.Package['Types'].values())]
                for CName, C in self.Package['Constants'].items():
                    C.Name = CName

                ConstantsList = [x.Declare(Constant=True) for x in list(self.Package['Constants'].values())]
                PKGFILE.write(HDL.PkgDeclaration(self.PkgName, ''.join(ConstantsList + TypesList)))
                EmptyPkg = []
                for EmptyPkgName in self.Package['EmptyPkg']:
                    EmptyPkg.append(HDL.PkgDeclaration(EmptyPkgName, []))

                for PkgDeclaration in EmptyPkg:
                    PKGFILE.write('\n')
                    PKGFILE.write(PkgDeclaration)

            return (
             self.PkgName, os.path.join(OutputDir, '{0}.vhd'.format(self.PkgName)))
        else:
            return (None, )

    def CollectPkg(self, PkgObject):
        """
                Update PkgObject package dictionary with this package.
                """
        self.Package['Constants'].update(PkgObject.Package['Constants'])
        self.Package['Types'].update(PkgObject.Package['Types'])
        self.Package['TypeImport'].update(PkgObject.Package['TypeImport'])
        self.Package['EmptyPkg'] += PkgObject.Package['EmptyPkg']
        self.Package['EmptyPkg'] = list(set(self.Package['EmptyPkg']))