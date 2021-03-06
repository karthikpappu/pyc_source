# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyevolve\Initializators.py
# Compiled at: 2009-01-21 19:09:01
__doc__ = '\n\n:mod:`Initializators` -- initialization methods module\n===================================================================\n\nIn this module we have the genetic operators of initialization for each\nchromosome representation, the most part of initialization is done by\nchoosing random data.\n\n'
from random import randint as rand_randint, uniform as rand_uniform, choice as rand_choice
import logging, Util

def G1DBinaryStringInitializator(genome, **args):
    """ 1D Binary String initializator """
    genome.clearString()
    for i in xrange(len(genome)):
        genome.append(rand_choice((0, 1)))


def G1DListInitializatorAllele(genome, **args):
    """ Allele initialization function of G1DList

   To use this initializator, you must specify the *allele* genome parameter with the
   :class:`GAllele.GAlleles` instance.

   """
    allele = genome.getParam('allele', None)
    if allele is None:
        Util.raiseException("to use the G1DListInitializatorAllele, you must specify the 'allele' parameter")
    genome.clearList()
    for i in xrange(genome.listSize):
        random_allele = allele[i].getRandomAllele()
        genome.append(random_allele)

    return


def G1DListInitializatorInteger(genome, **args):
    """ Integer initialization function of G1DList

   This initializator accepts the *rangemin* and *rangemax* genome parameters.

   """
    genome.clearList()
    for i in xrange(genome.listSize):
        randomInteger = rand_randint(genome.getParam('rangemin', 0), genome.getParam('rangemax', 100))
        genome.append(randomInteger)


def G1DListInitializatorReal(genome, **args):
    """ Real initialization function of G1DList

   This initializator accepts the *rangemin* and *rangemax* genome parameters.

   """
    genome.clearList()
    for i in xrange(genome.listSize):
        randomReal = rand_uniform(genome.getParam('rangemin', 0), genome.getParam('rangemax', 100))
        genome.append(randomReal)


def G2DListInitializatorInteger(genome, **args):
    """ Integer initialization function of G2DList

   This initializator accepts the *rangemin* and *rangemax* genome parameters.
   
   """
    genome.clearList()
    for i in xrange(genome.getHeight()):
        for j in xrange(genome.getWidth()):
            randomInteger = rand_randint(genome.getParam('rangemin', 0), genome.getParam('rangemax', 100))
            genome.setItem(i, j, randomInteger)


def G2DListInitializatorReal(genome, **args):
    """ Integer initialization function of G2DList

   This initializator accepts the *rangemin* and *rangemax* genome parameters.

   """
    genome.clearList()
    for i in xrange(genome.getHeight()):
        for j in xrange(genome.getWidth()):
            randomReal = rand_uniform(genome.getParam('rangemin', 0), genome.getParam('rangemax', 100))
            genome.setItem(i, j, randomReal)


def G2DListInitializatorAllele(genome, **args):
    """ Allele initialization function of G2DList

   To use this initializator, you must specify the *allele* genome parameter with the
   :class:`GAllele.GAlleles` instance.

   .. warning:: the :class:`GAllele.GAlleles` instance must have the homogeneous flag enabled

   """
    allele = genome.getParam('allele', None)
    if allele is None:
        Util.raiseException("to use the G2DListInitializatorAllele, you must specify the 'allele' parameter")
    if allele.homogeneous == False:
        Util.raiseException("to use the G2DListInitializatorAllele, the 'allele' must be homogeneous")
    genome.clearList()
    for i in xrange(genome.getHeight()):
        for j in xrange(genome.getWidth()):
            random_allele = allele[0].getRandomAllele()
            genome.setItem(i, j, random_allele)

    return