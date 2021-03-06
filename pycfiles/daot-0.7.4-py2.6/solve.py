# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dao\solve.py
# Compiled at: 2011-11-10 02:08:10
from dao.env import GlobalEnvironment
from dao.base import is_subclass

class CutException(Exception):
    pass


class DaoStopIteration(Exception):
    pass


class DaoUncaughtThrow(Exception):

    def __init__(self, tag):
        self.tag = tag


class DaoSyntaxError(Exception):
    pass


class NoSolutionFound:
    cont_order = 0

    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'exit!'


class NoMoreSolution(Exception):
    pass


def tag_lookup(fun):

    def lookup_tagger(tagged_fun):
        tagged_fun.lookup = fun
        return tagged_fun

    return lookup_tagger


def done_lookup(cont, tag, stop_cont, solver):
    raise DaoUncaughtThrow(tag)


from dao.env import unwind

def done_lookup(cont, tag, stop_cont, solver):

    @mycont(cont)
    def loopkup_fail_cont(value, solver):
        raise DaoUncaughtThrow(tag)

    return unwind(stop_cont, None, tag, loopkup_fail_cont, solver)


def tag_unwind(fun):

    def unwind_tagger(tagged_fun):
        tagged_fun.unwind = fun
        return tagged_fun

    return unwind_tagger


def done_unwind(cont, value, tag, stop_cont_cont, solver, next_cont=None):
    if cont is stop_cont_cont:
        if next_cont is None:
            return cont
        return next_cont
    else:
        raise DaoUncaughtThrow(tag)
        return


def mycont(cont):

    def mycont_tagger(fun):
        fun.cont = cont
        fun.cont_order = cont.cont_order + 1
        return fun

    return mycont_tagger


@tag_lookup(done_lookup)
@tag_unwind(done_unwind)
@mycont(NoSolutionFound)
def done(value, solver):
    yield (
     done, value)


def value_cont(exp, cont):

    @mycont(cont)
    def value_cont(value, solver):
        return cont(exp, solver)

    return value_cont


def cut(cont_gen):
    try:
        return cont_gen.cut
    except:
        return False


class Parser:

    def parse(self, exp):
        try:
            exp_parse = exp.___parse___
        except:
            if isinstance(exp, list) or isinstance(exp, tuple):
                return tuple(self.parse(e) for e in exp)
            else:
                return exp

        try:
            return exp_parse(self)
        except TypeError:
            return exp


def preparse(exp):
    return Parser().parse(exp)


class LoopExitNextTagger:
    """ use tagger to preprocess before solve expression"""
    surfix = '$'

    def __init__(self):
        self.new_label_id = 1
        self.labels = {}

    def make_label(self, label):
        if label is None:
            label = '$' + str(self.new_label_id)
            self.new_label_id += 1
        return label

    def push_label(self, control_struct_type, label):
        self.labels.setdefault(control_struct_type, []).append(label)
        self.labels.setdefault(None, []).append(label)
        return

    def pop_label(self, control_struct_type):
        self.labels[control_struct_type].pop()
        self.labels[None].pop()
        return

    def tag_loop_label(self, exp):
        try:
            exp_tag_loop_label = exp.tag_loop_label
        except:
            if isinstance(exp, list):
                return [ self.tag_loop_label(e) for e in exp ]
            else:
                if isinstance(exp, tuple):
                    return tuple(self.tag_loop_label(e) for e in exp)
                return exp

        try:
            return exp_tag_loop_label(self)
        except TypeError:
            return exp


def tag_loop_label(exp):
    return LoopExitNextTagger().tag_loop_label(exp)


def dao_repr(exp):
    try:
        exp_____repr____ = exp.____repr____
    except:
        if isinstance(exp, list) or isinstance(exp, tuple):
            return (',').join([ dao_repr(e) for e in exp ])
        else:
            return repr(exp)

    try:
        return exp_____repr____()
    except TypeError:
        return repr(exp)


def make_solver():
    global_env = GlobalEnvironment({})
    env = global_env.extend()
    return Solver(global_env, env, None, None)


def to_sexpression(exp):
    try:
        exp_to_sexpression = exp.to_sexpression
    except:
        if isinstance(exp, tuple):
            return tuple(to_sexpression(x) for x in exp)
        else:
            return exp

    if isinstance(exp, type):
        return exp
    return exp_to_sexpression()


def eval(exp):
    sexp = to_sexpression(exp)
    return make_solver().eval(sexp)


class Solutions:

    def __init__(self, solutions):
        self.solutions = solutions

    def next(self):
        try:
            return self.solutioins.next()
        except StopIteration:
            return 'No more solutions!'


def solve(exp):
    sexp = to_sexpression(exp)
    return Solutions(Solver.solve(exp))


(interactive, noninteractive) = (1, 0)
_run_mode = interactive
_interactive_solver = None
_interactive_parser = None
_interactive_tagger = None

def run_mode():
    global _run_mode
    return _run_mode


def interactive_solver():
    global _interactive_solver
    return _interactive_solver


def interactive_parser():
    global _interactive_parser
    return _interactive_parser


def interactive_tagger():
    global _interactive_tagger
    return _interactive_tagger


def set_run_mode(mode=interactive, solver=None, tagger=None, parser=None):
    global _interactive_parser
    global _interactive_solver
    global _interactive_tagger
    global _run_mode
    if mode == interactive:
        _run_mode = interactive
        if solver is None:
            _interactive_solver = make_solver() if _interactive_solver is None else _interactive_solver
        else:
            _interactive_solver = solver
        if tagger is None:
            _interactive_tagger = LoopExitNextTagger() if _interactive_tagger is None else _interactive_tagger
        else:
            _interactive_tagger = tagger
        if parser is None:
            _interactive_parser = Parser() if _interactive_parser is None else _interactive_parser
        else:
            _interactive_parser = _parser
    else:
        _run_mode = noninteractive
    return


class Solver:

    def __init__(self, global_env, env, parse_state, stop_cont):
        self.global_env = global_env
        self.env = env
        self.stop_cont = stop_cont
        self.parse_state = parse_state
        self.solved = False
        self.sign_state2cont = {}
        self.sign_state2results = {}
        self.call_path = []

    def eval(self, exp):
        for x in self.solve(exp):
            return x

        raise NoSolutionFound(exp)

    def solve(self, exp, stop_cont=done):
        for (_, result) in self.exp_run_cont(exp, stop_cont):
            yield result

    def solve_exps(self, exps, stop_cont=done):
        if len(exps) == 0:
            yield True
        elif len(exps) == 1:
            for (c, x) in self.exp_run_cont(exps[0], stop_cont):
                yield x

        else:
            left_exps_cont = self.exps_cont(exps[1:], stop_cont)
        for (c, x) in self.exp_run_cont(exps[0], left_exps_cont):
            yield x

    def exp_run_cont(self, exp, stop_cont, value=None):
        cont = self.cont(exp, stop_cont)
        return self.run_cont(cont, stop_cont, value)

    def exps_run_cont(self, exps, stop_cont, value=None):
        cont = self.exps_cont(exps, stop_cont)
        return self.run_cont(cont, stop_cont, value)

    def run_cont(self, cont, stop_cont, value=None):
        self1 = self
        self = Solver(self.global_env, self.env, self.parse_state, stop_cont)
        stop_cont = self.stop_cont
        root = cont_gen = cont(value, self)
        cut_gen = {}
        cut_gen[cont_gen] = cut(cont)
        parent = {}
        while 1:
            try:
                (c, v) = cont_gen.next()
                if self.solved or c is stop_cont:
                    env, parse_state = self1.env, self1.parse_state
                    self1.env, self1.parse_state = self.env, self.parse_state
                    yield (c, v)
                    self1.env, self1.parse_state = env, parse_state
                else:
                    cg = c(v, self)
                    cut_gen[cg] = cut(c)
                    parent[cg] = cont_gen
                    cont_gen = cg
            except StopIteration:
                if cont_gen is root:
                    return
                cg = cont_gen
                cont_gen = parent[cont_gen]
                del parent[cg]
            except CutException:
                while not cut_gen[cont_gen] and cont_gen is not root:
                    cont_gen.close()
                    del cut_gen[cont_gen]
                    cg = cont_gen
                    cont_gen = parent[cont_gen]
                    del parent[cg]

                if cont_gen is root:
                    cont_gen.close()
                    return
                cont_gen.close()
                cg = cont_gen
                cont_gen = parent[cont_gen]
                del parent[cg]

    def cont(self, exp, cont):
        if isinstance(exp, tuple):
            if is_subclass(exp[0], object):
                form = exp[0](*exp[1:])
                return form.cont(cont, self)
            else:

                @mycont(cont)
                def evaluate_cont(op, solver):
                    return op.evaluate_cont(solver, cont, exp[1:])

                return self.cont(exp[0], evaluate_cont)
        elif is_subclass(exp, object):
            return value_cont(exp, cont)
        try:
            exp_cont = exp.cont
        except:
            return value_cont(exp, cont)
        else:
            return exp_cont(cont, self)

    def exps_cont(self, exps, cont):
        if len(exps) == 0:
            return value_cont(None, cont)
        else:
            if len(exps) == 1:
                return self.cont(exps[0], cont)
            else:

                @mycont(cont)
                def last_cont(value, solver):
                    yield (solver.cont(exps[(-1)], cont), value)

                return self.exps_cont(exps[:-1], last_cont)
            return