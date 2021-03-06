# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymatlab/matlab.py
# Compiled at: 2013-10-24 09:14:32
__doc__ = '\nCopyright 2010-2013 Joakim Möller\n\nThis file is part of pymatlab.\n\npymatlab is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\npymatlab is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with pymatlab.  If not, see <http://www.gnu.org/licenses/>.\n'
from ctypes import *
from numpy import array, ndarray, dtype
from os.path import join
import platform, sys, numpy
from pymatlab.typeconv import *

class mxArray(Structure):
    pass


wrap_script = "\npymatlaberrstring ='';\ntry\n    {0}\ncatch err\n    pymatlaberrstring = sprintf('Error: %s with message: %s\\n',err.identifier,err.message);\n    for i = 1:length(err.stack)\n        pymatlaberrstring = sprintf('%%sError: in fuction %%s in file %%s line %%i\\n',pymatlaberrstring,err.stack(i,1).name,err.stack(i,1).file,err.stack(i,1).line);\n    end\nend\nif exist('pymatlaberrstring','var')==0\n    pymatlaberrstring='';\nend\n"

class MatlabSession(object):

    def __init__(self, matlab_root='', command='', bufsize=128):
        system = platform.system()
        if system == 'Linux' or system == 'Darwin':
            self.engine = CDLL(join(matlab_root, 'bin', 'glnxa64', 'libeng.so'))
            self.mx = CDLL(join(matlab_root, 'bin', 'glnxa64', 'libmx.so'))
            self.ep = self.engine.engOpen(c_char_p(command))
        elif system == 'Windows':
            self.engine = CDLL(join(matlab_root, 'bin', 'glnxa64', 'libeng.dll'))
            self.mx = CDLL(join(matlab_root, 'bin', 'glnxa64', 'libmx.dll'))
            self.ep = self.engine.engOpen(None)
        else:
            raise NotImplementedError(('system {} not yet supported').format(system))
        if self.ep is None:
            raise RuntimeError(('Could not start matlab using command "{}"').format(command))
        self.buff_length = bufsize
        if self.buff_length != 0:
            self.buf = create_string_buffer(self.buff_length)
            self.engine.engOutputBuffer(self.ep, self.buf, self.buff_length - 1)
        return

    def __del__(self):
        self.engine.engClose(self.ep)

    def run(self, matlab_statement):
        real_statement = wrap_script.format(matlab_statement)
        self.engine.engEvalString(self.ep, c_char_p(real_statement))
        self.engine.engGetVariable.restype = POINTER(mxArray)
        mxresult = self.engine.engGetVariable(self.ep, c_char_p('pymatlaberrstring'))
        self.mx.mxArrayToString.restype = c_char_p
        error_string = self.mx.mxArrayToString(mxresult)
        if error_string != '':
            raise RuntimeError(('Error from Matlab: {0}').format(error_string))

    def getvalue(self, variable):
        self.engine.engGetVariable.restype = POINTER(mxArray)
        mx = self.engine.engGetVariable(self.ep, c_char_p(variable))
        self.mx.mxGetNumberOfDimensions.restype = c_size_t
        ndims = self.mx.mxGetNumberOfDimensions(mx)
        self.mx.mxGetDimensions.restype = POINTER(c_size_t)
        dims = self.mx.mxGetDimensions(mx)
        self.mx.mxGetNumberOfElements.restype = c_size_t
        numelems = self.mx.mxGetNumberOfElements(mx)
        self.mx.mxGetElementSize.restype = c_size_t
        elem_size = self.mx.mxGetElementSize(mx)
        self.mx.mxGetClassName.restype = c_char_p
        class_name = self.mx.mxGetClassName(mx)
        self.mx.mxIsNumeric.restype = c_bool
        is_numeric = self.mx.mxIsNumeric(mx)
        if is_numeric:
            self.mx.mxIsComplex.restype = c_bool
            is_complex = self.mx.mxIsComplex(mx)
            returnsize = numelems * elem_size
            self.mx.mxGetData.restype = POINTER(c_void_p)
            data = self.mx.mxGetData(mx)
            realbuf = create_string_buffer(returnsize)
            memmove(realbuf, data, returnsize)
            datatype = class_name
            if is_complex:
                self.mx.mxGetImagData.restype = POINTER(c_void_p)
                data_imag = self.mx.mxGetImagData(mx)
                imagbuf = create_string_buffer(returnsize)
                memmove(imagbuf, data_imag, returnsize)
                pyarray_imag = ndarray(buffer=imagbuf, shape=dims[:ndims], dtype=dtype(datatype), order='F')
            pyarray_real = ndarray(buffer=realbuf, shape=dims[:ndims], dtype=dtype(datatype), order='F')
            if is_complex:
                pyarray = pyarray_real + pyarray_imag * complex(0.0, 1.0)
            else:
                pyarray = pyarray_real
            return pyarray.squeeze()
        if class_name == 'cell':
            raise NotImplementedError(('{}-arrays are not implemented').format(class_name))
        else:
            if class_name == 'char':
                length = numelems + 2
                return_str = create_string_buffer(length)
                self.mx.mxGetString(mx, return_str, length - 1)
                return return_str.value
            if class_name == 'function_handle':
                raise NotImplementedError(('{}-arrays are not implemented').format(class_name))
            else:
                if class_name == 'logical':
                    returnsize = numelems * elem_size
                    self.mx.mxGetData.restype = POINTER(c_void_p)
                    data = self.mx.mxGetData(mx)
                    buf = create_string_buffer(returnsize)
                    memmove(buf, data, returnsize)
                    pyarray = ndarray(buffer=buf, shape=dims[:ndims], dtype=dtype('bool'), order='F')
                    return pyarray.squeeze()
                if class_name == 'struct':
                    raise NotImplementedError(('{}-arrays are not implemented').format(class_name))
                elif class_name == 'unknown':
                    raise NotImplementedError(('{}-arrays are not implemented').format(class_name))
                else:
                    raise NotImplementedError(('{}-arrays are not implemented').format(class_name))

    def putvalue(self, name, pyvariable):
        if type(pyvariable) == str:
            self.mx.mxCreateString.restype = POINTER(mxArray)
            mx = self.mx.mxCreateString(c_char_p(pyvariable))
        elif type(pyvariable) == dict:
            raise NotImplementedError('dictionaries are not supported')
        else:
            if not type(pyvariable) == ndarray:
                pyvariable = array(pyvariable)
            if pyvariable.dtype.kind in ('i', 'u', 'f', 'c'):
                dim = pyvariable.ctypes.shape_as(c_size_t)
                self.mx.mxCreateNumericArray.restype = POINTER(mxArray)
                complex_flag = 0
                if pyvariable.dtype.kind == 'c':
                    complex_flag = 1
                mx = self.mx.mxCreateNumericArray(c_size_t(pyvariable.ndim), dim, np_to_mat(pyvariable), c_int(complex_flag))
                self.mx.mxGetData.restype = POINTER(c_void_p)
                data_old = self.mx.mxGetData(mx)
                datastring = pyvariable.real.tostring('F')
                n_datastring = len(datastring)
                memmove(data_old, datastring, n_datastring)
                if complex_flag:
                    self.mx.mxGetImagData.restype = POINTER(c_void_p)
                    data_old_imag = self.mx.mxGetImagData(mx)
                    datastring = pyvariable.imag.tostring('F')
                    n_datastring = len(datastring)
                    memmove(data_old_imag, datastring, n_datastring)
            elif pyvariable.dtype.kind == 'b':
                dim = pyvariable.ctypes.shape_as(c_size_t)
                self.mx.mxCreateLogicalArray.restype = POINTER(mxArray)
                mx = self.mx.mxCreateLogicalArray(c_size_t(pyvariable.ndim), dim)
                self.mx.mxGetLogicals.restype = POINTER(c_void_p)
                data_old = self.mx.mxGetData(mx)
                datastring = pyvariable.tostring('F')
                n_datastring = len(datastring)
                memmove(data_old, datastring, n_datastring)
            elif pyvariable.dtype.kind == 'S':
                dim = pyvariable.ctypes.shape_as(c_size_t)
                self.mx.mxCreateCharArray.restype = POINTER(mxArray)
                mx = self.mx.mxCreateNumericArray(c_size_t(pyvariable.ndim), dim)
                self.mx.mxGetData.restype = POINTER(c_void_p)
                data_old = self.mx.mxGetData(mx)
                datastring = pyvariable.tostring('F')
                n_datastring = len(datastring)
                memmove(data_old, datastring, n_datastring)
            elif pyvariable.dtype.kind == 'O':
                raise NotImplementedError('Object arrays are not supported')
            else:
                raise NotImplementedError('Type not supported')
        self.engine.engPutVariable(self.ep, c_char_p(name), mx)