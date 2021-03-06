# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apgl/io/MDLGraphsReader.py
# Compiled at: 2012-04-06 16:42:21
__doc__ = '\nA class to read a set of graphs in MDL format, the vertex is labelled according\nto the atom type.\n'
import numpy
from apgl.graph.VertexList import VertexList
from apgl.graph.SparseGraph import SparseGraph

class MDLGraphsReader:

    def __init__(self):
        self.atomDict = {}
        self.atomDict['C'] = 0
        self.atomDict['H'] = 1
        self.atomDict['N'] = 2
        self.atomDict['O'] = 3

    def readFromFile(self, fileName):
        inFile = open(fileName, 'r')
        numFeatures = 1
        graphList = []
        line = inFile.readline()
        while line != '':
            inFile.readline()
            inFile.readline()
            line = inFile.readline()
            valueList = line.split(None)
            numVertices = int(valueList[0])
            numEdges = int(valueList[1])
            vList = VertexList(numVertices, numFeatures)
            for i in range(numVertices):
                line = inFile.readline()
                valueList = line.split(None)
                vList.setVertex(i, numpy.array([self.atomDict[valueList[3]]]))

            graph = SparseGraph(vList)
            for i in range(numEdges):
                line = inFile.readline()
                valueList = line.split(None)
                graph.addEdge(int(valueList[0]) - 1, int(valueList[1]) - 1)

            graphList.append(graph)
            inFile.readline()
            inFile.readline()
            line = inFile.readline()

        return graphList