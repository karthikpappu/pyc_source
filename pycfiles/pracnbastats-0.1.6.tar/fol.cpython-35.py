# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nyga/work/code/pracmln/python3/pracmln/logic/fol.py
# Compiled at: 2018-04-24 04:48:32
# Size of source mod 2**32: 13377 bytes
from dnutils import ifnone
from .common import Logic
from ..mln.util import fstr

class FirstOrderLogic(Logic):
    """FirstOrderLogic"""

    class Constraint(Logic.Constraint):
        pass

    class Formula(Logic.Formula, Constraint):

        def noisyor(self, world):
            """
            Computes the noisy-or distribution of this formula.
            """
            return self.cnf().noisyor(world)

        def _getEvidenceTruthDegreeCW(self, gndAtom, worldValues):
            """
                gets (soft or hard) evidence as a degree of belief from 0 to 1, making the closed world assumption,
                soft evidence has precedence over hard evidence
            """
            se = self._getSoftEvidence(gndAtom)
            if se is not None:
                if True == worldValues[gndAtom.idx] or None == worldValues[gndAtom.idx]:
                    return se
                return 1.0 - se
            if worldValues[gndAtom.idx]:
                return 1.0
            return 0.0

        def _noisyOr(self, mln, worldValues, disj):
            if isinstance(disj, FirstOrderLogic.GroundLit):
                lits = [
                 disj]
            else:
                if isinstance(disj, FirstOrderLogic.TrueFalse):
                    return disj.isTrue(worldValues)
                lits = disj.children
            prod = 1.0
            for lit in lits:
                p = mln._getEvidenceTruthDegreeCW(lit.gndAtom, worldValues)
                if not lit.negated:
                    factor = p
                else:
                    factor = 1.0 - p
                prod *= 1.0 - factor

            return 1.0 - prod

    class ComplexFormula(Logic.ComplexFormula, Formula):
        pass

    class Lit(Logic.Lit, Formula):
        pass

    class Litgroup(Logic.LitGroup, Formula):
        pass

    class GroundAtom(Logic.GroundAtom):
        pass

    class GroundLit(Logic.GroundLit, Formula):

        def noisyor(self, world):
            truth = self(world)
            if self.negated:
                truth = 1.0 - truth
            return truth

    class Disjunction(Logic.Disjunction, ComplexFormula):

        def truth(self, world):
            dontKnow = False
            for child in self.children:
                childValue = child.truth(world)
                if childValue == 1:
                    return 1
                if childValue is None:
                    dontKnow = True

            if dontKnow:
                return
            else:
                return 0

        def simplify(self, world):
            sf_children = []
            for child in self.children:
                child = child.simplify(world)
                t = child.truth(world)
                if t == 1:
                    return self.mln.logic.true_false(1, mln=self.mln, idx=self.idx)
                if t == 0:
                    continue
                else:
                    sf_children.append(child)

            if len(sf_children) == 1:
                return sf_children[0].copy(idx=self.idx)
            else:
                if len(sf_children) >= 2:
                    return self.mln.logic.disjunction(sf_children, mln=self.mln, idx=self.idx)
                return self.mln.logic.true_false(0, mln=self.mln, idx=self.idx)

        def noisyor(self, world):
            prod = 1.0
            for lit in self.children:
                p = ifnone(lit(world), 1)
                if not lit.negated:
                    factor = p
                else:
                    factor = 1.0 - p
                prod *= 1.0 - factor

            return 1.0 - prod

    class Conjunction(Logic.Conjunction, ComplexFormula):

        def truth(self, world):
            dontKnow = False
            for child in self.children:
                childValue = child.truth(world)
                if childValue == 0:
                    return 0.0
                if childValue is None:
                    dontKnow = True

            if dontKnow:
                return
            else:
                return 1.0

        def simplify(self, world):
            sf_children = []
            for child in self.children:
                child = child.simplify(world)
                t = child.truth(world)
                if t == 0:
                    return self.mln.logic.true_false(0, mln=self.mln, idx=self.idx)
                if t == 1:
                    pass
                else:
                    sf_children.append(child)

            if len(sf_children) == 1:
                return sf_children[0].copy(idx=self.idx)
            else:
                if len(sf_children) >= 2:
                    return self.mln.logic.conjunction(sf_children, mln=self.mln, idx=self.idx)
                return self.mln.logic.true_false(1, mln=self.mln, idx=self.idx)

        def noisyor(self, world):
            cnf = self.cnf()
            prod = 1.0
            if isinstance(cnf, FirstOrderLogic.Conjunction):
                for disj in cnf.children:
                    prod *= disj.noisyor(world)

            else:
                prod *= cnf.noisyor(world)
            return prod

    class Implication(Logic.Implication, ComplexFormula):

        def truth(self, world):
            ant = self.children[0].truth(world)
            cons = self.children[1].truth(world)
            if ant == 0 or cons == 1:
                return 1
            if ant is None or cons is None:
                return
            return 0

    class Biimplication(Logic.Biimplication, ComplexFormula):

        def truth(self, world):
            c1 = self.children[0].truth(world)
            c2 = self.children[1].truth(world)
            if c1 is None or c2 is None:
                return
            if c1 == c2:
                return 1
            return 0

    class Negation(Logic.Negation, ComplexFormula):
        pass

    class Exist(Logic.Exist, ComplexFormula):
        pass

    class Equality(Logic.Equality, ComplexFormula):
        pass

    class TrueFalse(Logic.TrueFalse, Formula):

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, truth):
            if not truth == 0 and not truth == 1:
                raise Exception('Truth values in first-order logic cannot be %s' % truth)
            self._value = truth

        def __str__(self):
            return str(True if self.value == 1 else False)

        def noisyor(self, world):
            return self(world)

    class ProbabilityConstraint(object):
        """FirstOrderLogic.ProbabilityConstraint"""

        def __init__(self, formula, p):
            self.formula = formula
            self.p = p

        def __repr__(self):
            return str(self)

    class PriorConstraint(ProbabilityConstraint):
        """FirstOrderLogic.PriorConstraint"""

        def __str__(self):
            return 'P(%s) = %.2f' % (fstr(self.formula), self.p)

    class PosteriorConstraint(ProbabilityConstraint):
        """FirstOrderLogic.PosteriorConstraint"""

        def __str__(self):
            return 'P(%s|E) = %.2f' % (fstr(self.formula), self.p)

    def conjunction(self, *args, **kwargs):
        return FirstOrderLogic.Conjunction(*args, **kwargs)

    def disjunction(self, *args, **kwargs):
        return FirstOrderLogic.Disjunction(*args, **kwargs)

    def negation(self, *args, **kwargs):
        return FirstOrderLogic.Negation(*args, **kwargs)

    def implication(self, *args, **kwargs):
        return FirstOrderLogic.Implication(*args, **kwargs)

    def biimplication(self, *args, **kwargs):
        return FirstOrderLogic.Biimplication(*args, **kwargs)

    def equality(self, *args, **kwargs):
        return FirstOrderLogic.Equality(*args, **kwargs)

    def exist(self, *args, **kwargs):
        return FirstOrderLogic.Exist(*args, **kwargs)

    def gnd_atom(self, *args, **kwargs):
        return FirstOrderLogic.GroundAtom(*args, **kwargs)

    def lit(self, *args, **kwargs):
        return FirstOrderLogic.Lit(*args, **kwargs)

    def litgroup(self, *args, **kwargs):
        return FirstOrderLogic.LitGroup(*args, **kwargs)

    def gnd_lit(self, *args, **kwargs):
        return FirstOrderLogic.GroundLit(*args, **kwargs)

    def count_constraint(self, *args, **kwargs):
        return FirstOrderLogic.CountConstraint(*args, **kwargs)

    def true_false(self, *args, **kwargs):
        return FirstOrderLogic.TrueFalse(*args, **kwargs)


Constraint = FirstOrderLogic.Constraint
Formula = FirstOrderLogic.Formula
ComplexFormula = FirstOrderLogic.ComplexFormula
Conjunction = FirstOrderLogic.Conjunction
Disjunction = FirstOrderLogic.Disjunction
Lit = FirstOrderLogic.Lit
GroundLit = FirstOrderLogic.GroundLit
GroundAtom = FirstOrderLogic.GroundAtom
Equality = FirstOrderLogic.Equality
Implication = FirstOrderLogic.Implication
Biimplication = FirstOrderLogic.Biimplication
Negation = FirstOrderLogic.Negation
Exist = FirstOrderLogic.Exist
TrueFalse = FirstOrderLogic.TrueFalse
NonLogicalConstraint = FirstOrderLogic.NonLogicalConstraint
CountConstraint = FirstOrderLogic.CountConstraint
GroundCountConstraint = FirstOrderLogic.GroundCountConstraint