# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/mln/mlnpreds.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 5811 bytes
from dnutils import logs
from pracmln.mln.mrfvars import BinaryVariable, FuzzyVariable, SoftMutexVariable, MutexVariable
logger = logs.getlogger(__name__)

class Predicate(object):
    __doc__ = "\n    Represents a logical predicate and its properties.\n    \n    :param predname:    the name of the predicate.\n    :param argdoms:     the list of domains of the predicate's arguments.\n    "

    def __init__(self, name, argdoms):
        self.argdoms = argdoms
        self.name = name

    def varname(self, gndatom):
        """
        Takes an instance of a ground atom and generates the name
        of the corresponding variable.
        """
        return str(gndatom)

    def tovariable(self, mrf, gndatom):
        """
        Creates a new instance of an atomic ground block instance
        depending on the type of the predicate
        """
        return BinaryVariable(mrf, name=self.varname(gndatom), predicate=self)

    def groundatoms(self, mln, domains):
        """
        Iterates over all ground atoms that can be generated by this predicate
        given the domains and the MLN.
        
        :param domains:    dict mapping the domain names to their values.
        """
        for gndatom in self._groundatoms(mln, domains, [], self.argdoms):
            yield gndatom

    def _groundatoms(self, mln, domains, values, argdoms):
        if not argdoms:
            yield mln.logic.gnd_atom(self.name, values, mln)
            return
        dom = domains.get(argdoms[0])
        if dom is None or len(dom) == 0:
            logger.info("Ground Atoms for predicate %s could not be generated, since the domain '%s' is empty" % (str(self), argdoms[0]))
            return
        for value in dom:
            for gndatom in self._groundatoms(mln, domains, values + [value], argdoms[1:]):
                yield gndatom

    def __eq__(self, other):
        return type(other) == type(self) and other.name == self.name and other.argdoms == self.argdoms

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return '%s(%s)' % (self.name, self.argstr())

    def __repr__(self):
        return '<Predicate: %s>' % str(self)

    def argstr(self):
        return ','.join(map(str, self.argdoms))


class FuzzyPredicate(Predicate):
    __doc__ = '\n    Represents a predicate whose atom can take fuzzy degrees of truth in [0,1].\n    '

    def __init__(self, name, argdoms):
        Predicate.__init__(self, name, argdoms)

    def __repr__(self):
        return '<FuzzyPredicate: %s>' % str(self)

    def tovariable(self, mrf, gndatom):
        return FuzzyVariable(mrf, name=self.varname(gndatom), predicate=self)


class FunctionalPredicate(Predicate):
    __doc__ = '\n    Represents a predicate declaration for a functional constraint.\n \n    :param mutex:    (int) the index of the mutex argument\n    \n    .. seealso:: :class:`mln.base.Predicate` \n    \n    '

    def __init__(self, name, argdoms, mutex):
        Predicate.__init__(self, name, argdoms)
        self.mutex = mutex

    def varname(self, gndatom):
        nonfuncargs = [p if i != self.mutex else '_' for i, p in enumerate(gndatom.args)]
        return '%s(%s)' % (gndatom.predname, ','.join(nonfuncargs))

    def tovariable(self, mrf, name):
        return MutexVariable(mrf, name, self)

    def __eq__(self, other):
        return Predicate.__eq__(self, other) and self.mutex == other.mutex

    def __str__(self):
        return '%s(%s)' % (self.name, self.argstr())

    def __repr__(self):
        return '<FunctionalPredicate: %s>' % str(self)

    def argstr(self):
        return ','.join([arg if i != self.mutex else '%s!' % arg for i, arg in enumerate(self.argdoms)])


class SoftFunctionalPredicate(FunctionalPredicate):
    __doc__ = '\n    Represents a predicate declaration for soft function constraint.\n    '

    def tovariable(self, mrf, name):
        return SoftMutexVariable(mrf, name, self)

    def __str__(self):
        return '%s(%s)' % (self.name, self.argstr())

    def argstr(self):
        return ','.join([arg if i != self.mutex else '%s?' % arg for i, arg in enumerate(self.argdoms)])

    def __repr__(self):
        return '<SoftFunctionalPredicate: %s>' % str(self)