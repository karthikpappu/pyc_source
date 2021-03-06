# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/v2/Param.py
# Compiled at: 2020-01-20 06:37:24
# Size of source mod 2**32: 9491 bytes
"""
This class extend the standard dictionnary behaviour.
It is used to read and store all the parameters used by the NPK program.

- it adds the possibility to load from files and dump/store to files the content of the dictionnary
  the file will be of the form :
  key=value, with one entry per line

- when extracted from the dictionnnary, values are interpreted in several manner
    o 1k is replaced by 1024 and all multiples (4k; 24k; etc...)
    o 1M is replaced by 1024*1024 and all multiples (4M; 24M; etc...)
    o 1G is replaced by 1024*1024*1à24 and all multiples (4M; 24M; etc...)
    o if surrounded by parenthesis
        - all arithmetic is evaluated : math.pi/2, 0.1*get_si1_2d(), etc...
        - all current NPKData is available as 'data'
        - basic python modules are available: time os sys math   
"""
from __future__ import print_function
__author__ = 'Marc A. Delsuc <delsuc@igbmc.fr>'
__date__ = 'Oct 2020'
import os, re, sys, time, math, copy
try:
    from UserDict import UserDict
except ImportError:
    from collections import UserDict

def parse(line):
    """Parse one property entry and prepare it to be entered in the  dictionnary
    """
    l = re.split('(?<!\\\\)=', line, 1)
    dkey = re.sub('\\\\=', '=', l[0])
    val = re.sub('\\\\=', '=', l[1])
    return (
     dkey, val)


class NPKParam(UserDict):
    __doc__ = 'NPKParam class handles the parameter set used by NPK'

    def __init__(self, npkd, *arg, **kw):
        self.npkd = npkd
        (UserDict.__init__)(self, *arg, **kw)

    def __str__(self):
        return 'parameters :\n' + repr(self)

    def __getitem__(self, key):
        """overloading of the dictionnary [] method
        evaluates the content
        """
        i = self.evaluate(self.data[key])
        return i

    def raw(self, key):
        """
        acces to the raw data present in the dictionnary, necessary in certain cases
        """
        return self.data[key]

    def dump(self, fname):
        """
        dump the content of the Parameter dictionnary as a property list file
        entries are not evaluated
        
        one entry per line with the following syntax :
        entry=value
        
        """
        try:
            fout = open(fname, 'w')
        except:
            print('Error while opening file :', sys.exc_info()[0])
            raise

        fout.write('#Property list file, dumped :' + time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime()) + '\n')
        for i in self.keys():
            lk = re.sub('=', '\\\\=', i)
            lv = re.sub('=', '\\\\=', str(self.data[i]))
            fout.write(lk + '=' + lv + '\n')

        fout.close()

    def store(self, fname):
        """
        write the content of the Parameter dictionnary as a property list file
        equivalent to dump, BUT entries are evaluated
        
        one entry per line with the following syntax :
        entry=value
        
        """
        try:
            fout = open(fname, 'w')
        except:
            print('Error while opening file :', sys.exc_info()[0])
            raise

        fout.write('#Property list file, output :' + time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime()) + '\n')
        for i in self.keys():
            lk = re.sub('=', '\\\\=', i)
            lv = re.sub('=', '\\\\=', self[i])
            fout.write(lk + '=' + lv + '\n')

        fout.close()

    def load(self, fname):
        """
        load a property list file as a dictionary
        
        one entry per line with the following syntax :
        entry=value
        
        keys are set to lowercase
        """
        try:
            fin = open(fname)
            f = fin.read()
            ls = f.split('\n')
            for v in ls:
                if not v == '':
                    if v[0] == '#':
                        continue
                    dkey, fval = parse(v.strip())
                    try:
                        val = self.data[dkey]
                    except:
                        pass

                    self.data[dkey] = fval

            fin.close
        except:
            print('File ' + fname + ' not found.')
            print('Creating empty parameter list\n')

    def build_default(self, default_list, paramlistdir):
        """ build the default parameter dictionary
        
        used in standard actions,
        returns a dictionary built from the default parmaters (see do_default.py and paramlistdir/*)
        and the additional parameters defined in the optionnal p_in_arg overwrite the default values
        
        """
        base = paramlistdir
        for l in default_list:
            self.load(os.path.join(base, l) + '.gtb')

    def change_key(self, patternOut, patternIn):
        """
        goes though the given dictionnay (which remains unchanged)
        and changes in keys the pattern "patternIn" to "patternOut"
        and returns the modified dictionnary

        typically used in 3D processing :
        
        p_in.change_key('f1', 'f2').change_key('f2', 'f3')

            substitutes F2 (of the 3D) by F1 (of the 2D plane)
            substitutes F3 (of the 3D) by F2 (of the 2D plane)

        """
        verbose = 0
        if verbose:
            print('change_key\n', patternIn, patternOut, self)
        p = NPKParam()
        if len(self) > 0:
            for i in self.keys():
                j = re.sub(patternIn, patternOut, i)
                try:
                    p[j] = self.raw(i)
                except:
                    p[j] = self[i]

        if verbose:
            print(p)
            raise Exception('stop due to verbose mode')
        return p

    def evaluate(self, val):
        """
        - val is interpreted in several manner
            o 1k is replaced by 1024 and all multiples (4k; 24k; etc...)
            o 1M is replaced by 1024*1024 and all multiples (4M; 24M; etc...)
            o 1G is replaced by 1024*1024*1à24 and all multiples (4M; 24M; etc...)
            o all arithmetic is evaluated : math.pi/2, 0.1*get_si1_2d(), etc...
            o all current NPKData is available as 'data'
        """
        found = 0
        data = self.npkd
        if re.match('^\\s*[0-9.-E]*\\s*$', val) or re.match('^\\s*\\(.+\\)\\s*$', val):
            try:
                fval = eval(val, globals(), locals())
                found = 1
            except:
                pass

        if not found:
            try:
                if val.endswith('k'):
                    fval = 1024 * int(val[0:len(val) - 1])
                    found = 1
                else:
                    if val.endswith('M'):
                        fval = 1048576 * int(val[0:len(val) - 1])
                        found = 1
                    else:
                        if val.endswith('G'):
                            fval = 1073741824 * int(val[0:len(val) - 1])
                            found = 1
                        else:
                            fval = float(val)
                            found = 1
            except ValueError:
                pass

        if (found or val.lower()) == 'false':
            fval = 0
            found = 1
        else:
            if val.lower() == 'true':
                fval = 1
                found = 1
            if not found:
                fval = val
            return fval


if __name__ == '__main__':
    from spike import NPKData
    dummy = NPKData.NPKData(dim=1)
    p = NPKParam(dummy)
    p['a'] = 'some text'
    p['aa'] = '1.2E3'
    p['b'] = '1234'
    p['bb'] = '4k'
    p['c'] = '1G'
    p['d'] = '(math.pi)'
    p['e'] = '(2*(3+2))'
    p['f'] = '(2*data.axis1.size)'
    p['g'] = '(1, 2, 3)'
    for i in p.keys():
        print('%s: "%s" => %s  /  %s' % (i, p.raw(i), p[i], type(p[i])))