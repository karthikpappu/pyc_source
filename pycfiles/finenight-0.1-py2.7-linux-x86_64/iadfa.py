# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/finenight/iadfa.py
# Compiled at: 2015-02-12 13:30:08
from fsa import *
from nameGenerator import *

class IncrementalAdfa(Dfa):
    """This class is an Acyclic Deterministic Finite State Automaton
    constructed by a list of words.
    """

    def __init__(self, nameGenerator=None):
        if nameGenerator is None:
            nameGenerator = IndexNameGenerator()
        self.nameGenerator = nameGenerator
        self.register = {}
        self.finalStates = []
        self.startState = self.nameGenerator.generate()
        self.states = {self.startState: State(self.startState)}
        return

    def initSearch(self):
        self.replaceOrRegister(self.startState)

    def getCommonPrefix(self, word):
        stateName = self.startState
        index = 0
        nextStateName = stateName
        while nextStateName is not None:
            symbol = word[index]
            stateName = nextStateName
            if self.states[stateName].transitions.has_key(symbol):
                nextStateName = self.states[stateName].transitions[symbol]
                index += 1
            else:
                nextStateName = None

        return (
         stateName, word[index:])

    def hasChildren(self, stateName):
        okay = False
        if filter(lambda s: s, self.states[stateName].transitions.values()):
            okay = True
        return okay

    def addSuffix(self, stateName, currentSuffix):
        lastState = stateName
        while len(currentSuffix) > 0:
            newStateName = self.nameGenerator.generate()
            symbol = currentSuffix[0]
            currentSuffix = currentSuffix[1:]
            self.states[stateName].transitions[symbol] = newStateName
            self.states[newStateName] = State(newStateName)
            stateName = newStateName

        self.finalStates.append(stateName)

    def markedAsRegistered(self, stateName):
        return self.register.has_key(stateName)

    def markAsRegistered(self, stateName):
        self.register[stateName] = True

    def equivalentRegisteredState(self, stateName):
        equivatentState = None
        for state in self.register.keys():
            print stateName, state
            if self.areEquivalents(state, stateName):
                equivatentState = state
                print 'foo', state,

        return equivatentState

    def lastChild(self, stateName):
        input = self.states[stateName].transitions.keys()
        input.sort()
        return (self.states[stateName].transitions[input[(-1)]], input[(-1)])

    def replaceOrRegister(self, stateName):
        childName, lastSymbol = self.lastChild(stateName)
        if not self.markedAsRegistered(childName):
            if self.hasChildren(childName):
                self.replaceOrRegister(childName)
            self.markAsRegistered(childName)

    def deleteBranch(self, child):
        childs = [
         child]
        while len(childs) > 0:
            nextChilds = []
            for child in childs:
                nextChilds += filter(lambda s: not self.markedAsRegistered(s), self.states[child].transitions.values())
                self.states.pop(child)
                if child in self.finalStates:
                    self.finalStates.remove(child)

            childs = nextChilds

    def createFromSortedListOfWords(self, word):
        word = unicode(word)
        if word.endswith('\n'):
            word = word[:-1]
        lastStateName, currentSuffix = self.getCommonPrefix(word)
        if self.hasChildren(lastStateName):
            self.replaceOrRegister(lastStateName)
        self.addSuffix(lastStateName, currentSuffix)

    def createFromArbitraryListOfWords(self, words):
        self.register = {}
        self.finalStates = []
        self.startState = self.nameGenerator.generate()
        self.states = {self.startState: State(self.startState)}