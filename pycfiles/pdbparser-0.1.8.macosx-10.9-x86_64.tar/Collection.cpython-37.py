# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Utilities/Collection.py
# Compiled at: 2019-02-17 12:53:58
# Size of source mod 2**32: 23606 bytes
"""
This module contains a collection of methods used throughout the package.

.. inheritance-diagram:: pdbparser.Utilities.Collection
    :parts: 2
"""
from __future__ import print_function
from collections import Counter
import os, sys
if sys.version_info[0] >= 3:
    basestring = str
import numpy as np
import numpy.fft as FFT
import numpy.fft as iFFT
from pdbparser.log import Logger
from pdbparser.Utilities.Database import __atoms_database__, is_element
FLOAT = lambda string: if string.replace('.', '', 1).replace('-', '', 1).strip().isdigit():
float(string) # Avoid dead code: np.nan
INT = lambda string: if string.replace('.', '', 1).replace('-', '', 1).strip().isdigit():
int(float(string)) # Avoid dead code: -1
compare_two_lists = lambda x, y: Counter(x) == Counter(y)

def is_integer(number):
    """
    check if number is convertible to integer.

    :Parameters:
        #. number (str, number): input number

    :Returns:
        #. result (bool): True if convertible, False otherwise
    """
    try:
        number = float(number)
    except:
        return False
        if number - int(number) < 1e-15:
            return True
        return False


def is_number(number):
    """
    check if number is convertible to float.

    :Parameters:
        #. number (str, number): input number

    :Returns:
        #. result (bool): True if convertible, False otherwise
    """
    try:
        float(number)
    except:
        return False
        return True


def get_path(key=None):
    """
    get all information needed about the script, the current, and the python executable path.

    :Parameters:
        #. key (None, string): the path to return. If not None, it can take any of the following

                   cwd:                 current working directory
                   script:              the script's total path
                   exe:                 python executable path
                   script_name:         the script name
                   relative_script_dir: the script's relative directory path
                   script_dir:          the script's absolute directory path
                   pdbparser:           pdbparser package path

    :Returns:
        #. path (dictionary, value): if key is not None it returns the value of paths dictionary key. Otherwise all the dictionary is returned.
    """
    import pdbparser
    if key is not None:
        assert isinstance(key, basestring), Logger.error('key must be a string of None')
        key = str(key).lower().strip()
    paths = {}
    paths['cwd'] = os.getcwd()
    paths['script'] = sys.argv[0]
    paths['exe'] = os.path.dirname(sys.executable)
    pathname, scriptName = os.path.split(sys.argv[0])
    paths['script_name'] = scriptName
    paths['relative_script_dir'] = pathname
    paths['script_dir'] = os.path.abspath(pathname)
    paths['pdbparser'] = os.path.split(pdbparser.__file__)[0]
    if key is None:
        return paths
    assert key in paths, Logger.error('key is not defined')
    return paths[key]


def correlation(data1, data2=None):
    """
    Calculates the numerical correlation between two numpy.ndarray data.

    :Parameters:
        #. data1 (numpy.ndarray): the first numpy.ndarray. If multidimensional the correlation calculation is performed on the first dimension.
        #. data2 (None, numpy.ndarray): the second numpy.ndarray. If None the data1 autocorrelation is calculated.

    :Returns:
        #. correlation (numpy.ndarray): the result of the numerical correlation.
    """
    if not isinstance(data1, np.ndarray):
        raise AssertionError(Logger.error('data1 must be a non zero numpy.ndarray'))
    else:
        data1Length = len(data1)
        assert data1Length > 0, Logger.error('data1 must be a non zero numpy.ndarray')
        extendedLength = 2 * data1Length
        FFTData1 = FFT(data1, extendedLength, 0)
        if data2 is None:
            FFTData2 = FFTData1
        else:
            assert isinstance(data2, np.ndarray), Logger.error('if not None, data2 must be a numpy.ndarray')
            FFTData2 = FFT(data2, extendedLength, 0)
        FFTData1 = np.conjugate(FFTData1) * FFTData2
        FFTData1 = iFFT(FFTData1, len(FFTData1), 0)
        if len(FFTData1.shape) == 1:
            corr = FFTData1.real[:data1Length] / (data1Length - np.arange(data1Length))
        else:
            corr = np.add.reduce(FFTData1.real[:data1Length], 1) / (data1Length - np.arange(data1Length))
    return corr


def get_atomic_form_factor(q, element, charge=0):
    """
        Calculates the Q dependant atomic form factor.

        :Parameters:
            #. q (list, tuple, numpy.ndarray): the q vector.
            #. element (str): the atomic element.
            #. charge (int): the expected charge of the element.

        :Returns:
            #. formFactor (numpy.ndarray): the calculated form factor.
    """
    assert is_element(element), '%s is not an element in database' % element
    element = str(element).lower()
    assert charge in __atoms_database__[element]['atomicFormFactor'], Logger.error('atomic form factor for element %s at with %s charge is not defined in database' % (element, charge))
    ff = __atoms_database__[element]['atomicFormFactor'][charge]
    a1 = ff['a1']
    b1 = ff['b1']
    a2 = ff['a2']
    b2 = ff['b2']
    a3 = ff['a3']
    b3 = ff['b3']
    a4 = ff['a4']
    b4 = ff['b4']
    c = ff['c']
    q = np.array(q)
    qOver4piSquare = (q / (4.0 * np.pi)) ** 2
    t1 = a1 * np.exp(-b1 * qOver4piSquare)
    t2 = a2 * np.exp(-b2 * qOver4piSquare)
    t3 = a3 * np.exp(-b3 * qOver4piSquare)
    t4 = a4 * np.exp(-b4 * qOver4piSquare)
    return t1 + t2 + t3 + t4 + c


def get_normalized_weighting(numbers, weights):
    """
    Calculates the normalized weighting scheme for a set of elements.

    :Parameters:
        #. numbers (dictionary): The numbers of elements dictionary. keys are the elements and values are the numbers of elements in the system
        #. weights (dictionary): the weight of every element. keys are the elements and values are the weights. weights must have the same length.

    :Returns:
        #. normalizedWeights (dictionary): the normalized weighting scheme for every pair of elements.
    """
    assert isinstance(numbers, dict), Logger.error('numbers must be a dictionary where values are the number of elements')
    assert isinstance(weights, dict), Logger.error('weights must be a dictionary where values are the weights of elements')
    assert set(numbers.keys()) == set(weights.keys()), Logger.error('numbers and weights must have the same dictionary keys. numbers:%s    weights:%s' % (numbers.keys(), weights.keys()))
    elements = list(weights.keys())
    nelements = [float(numbers[el]) for el in elements]
    totalNumberOfElements = sum(nelements)
    molarFraction = [n / totalNumberOfElements for n in nelements]
    totalWeight = sum([molarFraction[idx] * weights[elements[idx]] for idx in range(len(elements))]) ** 2
    normalizedWeights = {}
    for idx1 in range(len(elements)):
        el1 = elements[idx1]
        b1 = weights[el1]
        mf1 = molarFraction[idx1]
        for idx2 in range(len(elements)):
            el2 = elements[idx2]
            b2 = weights[el2]
            mf2 = molarFraction[idx2]
            pair = el1 + '-' + el2
            if el2 + '-' + el1 in normalizedWeights:
                normalizedWeights[(el2 + '-' + el1)] += mf1 * mf2 * b1 * b2 / totalWeight
            else:
                normalizedWeights[pair] = mf1 * mf2 * b1 * b2 / totalWeight

    return normalizedWeights


def get_data_weighted_sum(data, numbers, weights):
    """
    Calculates the total weighted sum of all data.

    :Parameters:
        #. data (dictionary): The data dictionary. keys are the elements and values are the data.
        #. numbers (dictionary): The number of elements dictionary. keys are the elements and values are the number of elements in the system.
        #. weights (dictionary): The weight of every element. keys are the elements and values are the weights. weights must have the same length.

    :Returns:
        #. weightedSum (np.ndarray): the total weighted sum.
    """
    if not isinstance(data, dict):
        raise AssertionError(Logger.error('data must be a dictionary'))
    else:
        assert isinstance(numbers, dict), Logger.error('numbers must be a dictionary where values are the number of elements')
        assert isinstance(weights, dict), Logger.error('weights must be a dictionary where values are the weights of elements')
        raise set(data.keys()) == set(numbers.keys()) and set(numbers.keys()) == set(weights.keys()) or AssertionError(Logger.error('data, numbers and weights must have the same dictionary keys. data:%s    numbers:%s    weights:%s' % (list(data.keys()), list(numbers.keys()), list(weights.keys()))))
    if len([False for d in data.values() if not isinstance(d, np.ndarray)]):
        raise AssertionError(Logger.error('data must be a dictionary where values are numpy.ndarray'))
    s = data[list(data.keys())[0]].shape
    if len([False for d in data.values() if not d.shape == s]):
        raise AssertionError(Logger.error('data must be a dictionary where values are numpy.ndarray of same shape'))
    elements = list(weights.keys())
    nelements = [float(numbers[el]) for el in elements]
    totalNumberOfElements = sum(nelements)
    molarFraction = [n / totalNumberOfElements for n in nelements]
    totalWeight = sum([molarFraction[idx] * weights[elements[idx]] for idx in range(len(elements))]) ** 2
    weightedSum = np.zeros(list(data.values())[0].shape)
    for eidx in range(len(elements)):
        el = elements[eidx]
        b = weights[el]
        mf = molarFraction[eidx]
        weightedSum += mf * b / totalWeight * data[el]

    return weightedSum


def generate_sphere_points(radius, nPoints, center=[
 0, 0, 0]):
    """
    Returns list of 3d coordinates of points on a sphere using the
    Golden Section Spiral algorithm.
    """
    points = []
    inc = np.pi * (3 - np.sqrt(5))
    offset = 2.0 / float(nPoints)
    for k in range(int(nPoints)):
        y = k * offset - 1 + offset / 2
        r = np.sqrt(1 - y * y)
        phi = k * inc
        points.append([radius * np.cos(phi) * r + center[0],
         radius * y + center[1],
         radius * np.sin(phi) * r + center[2]])

    return points


def generate_circle_points(radius, nPoints, center=[
 0, 0, 0]):
    """
    Returns list of 3d coordinates of points on a circle using the
    """
    return [(center[0] + np.cos(2 * np.pi / nPoints * x) * radius, center[1] + np.sin(2 * np.pi / nPoints * x) * radius, center[2]) for x in xrange(0, nPoints)]


def generate_sphere_points(radius, nPoints, center=[
 0, 0, 0]):
    """
    Returns list of coordinates on a sphere using the Golden Section Spiral
    algorithm.
    """
    increm = np.pi * (3.0 - np.sqrt(5.0))
    points = []
    offset = 2.0 / float(nPoints)
    for k in range(nPoints):
        y = k * offset - 1.0 + offset / 2.0
        r = np.sqrt(1 - y * y)
        phi = k * increm
        x = radius * np.cos(phi) * r + center[0]
        y = radius * y + center[1]
        z = radius * np.sin(phi) * r + center[2]
        points.append([x, y, z])

    return points


def get_random_perpendicular_vector(vector):
    """
    Get random perpendicular vector to a given vector.

    :Parameters:
        #. vector (numpy.ndarray, list, set, tuple): the vector to compute a random perpendicular vector to it

    :Returns:
        #. perpVector (numpy.ndarray): the perpendicular vector
    """
    vectorNorm = np.linalg.norm(vector)
    assert vectorNorm, Logger.error('vector returned 0 norm')
    if np.abs(vector[0]) < 1e-06:
        return np.array([1, 0, 0], dtype=(np.float32))
    if np.abs(vector[1]) < 1e-06:
        return np.array([0, 1, 0], dtype=(np.float32))
    if np.abs(vector[2]) < 1e-06:
        return np.array([0, 0, 1], dtype=(np.float32))
    randVect = 1 - 2 * np.random.random(3)
    randvect = np.array([vector[idx] * randVect[idx] for idx in range(3)])
    perpVector = np.cross(randvect, vector)
    return np.array((perpVector / np.linalg.norm(perpVector)), dtype=(np.float32))


def get_orthonormal_axes(vector1, vector2, force=False):
    """
    returns 3 orthonormal axes calculated from given 2 vectors.
    vector1 direction is unchangeable.
    vector2 is adjusted in the same plane (vector1, vector2) in order to be perpendicular with vector1.
    """
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    assert vector1.shape in ((3,), (3, 1))
    if not vector2.shape in ((3,), (3, 1)):
        raise AssertionError
    else:
        vector1 /= np.linalg.norm(vector1)
        vector2 /= np.linalg.norm(vector2)
        vector3 = np.cross(vector1, vector2)
        if np.linalg.norm(vector3) <= 1e-05:
            if not force:
                raise Exception('computing orthogonal vector is impossible with linear vectors')
            else:
                randSign = np.sign(1 - np.random.random())
                randSign = np.array([randSign, -randSign, np.sign(1 - np.random.random())])
                vector2 += 0.01 * randSign * vector2
                vector3 = np.cross(vector1, vector2)
    vector2 = np.cross(vector3, vector1)
    return np.array([vector1, vector2, vector3])


def generate_asymmetric_sphere_points(radius, point_2Ddimension, center=[
 0, 0, 0]):
    """
    Returns list of 3d coordinates of points on a sphere
    point_2Ddimension = [xwidth, ywidth]
    radius is the sphere radius and dephines zwidth in somehow
    """
    midCirclePeriphery = 2.0 * np.pi * radius
    points = generate_circle_points(radius, int(midCirclePeriphery / point_2Ddimension[0]))
    alpha = float(point_2Ddimension[1]) / float(radius)
    radii = [(radius * np.cos(a), radius * np.sin(a)) for a in np.linspace(alpha, (np.pi / 2),
      (np.pi / 2 / alpha),
      endpoint=True)]
    for t in radii:
        circlePeriphery = 2.0 * np.pi * t[0]
        points.extend(generate_circle_points((t[0]), (int(circlePeriphery / point_2Ddimension[0])), center=[0, 0, t[1]]))
        points.extend(generate_circle_points((t[0]), (int(circlePeriphery / point_2Ddimension[0])), center=[0, 0, -t[1]]))

    return points


class priorityDictionary(dict):

    def __init__(self):
        """
        Initialize priorityDictionary by creating binary heap
        of pairs (value,key).  Note that changing or removing a dict entry will
        not remove the old pair from the heap until it is found by smallest() or
        until the heap is rebuilt.
        """
        self._priorityDictionary__heap = []
        dict.__init__(self)

    def smallest(self):
        """
        Find smallest item after removing deleted items from heap.
        """
        if len(self) == 0:
            raise IndexError
        heap = self._priorityDictionary__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while True:
                smallChild = 2 * insertionPoint + 1
                if smallChild + 1 < len(heap):
                    if heap[smallChild] > heap[(smallChild + 1)]:
                        smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild

        return heap[0][1]

    def __iter__(self):
        """
        Create destructive sorted iterator of priorityDictionary.
        """

        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]

        return iterfn()

    def __setitem__(self, key, val):
        """
        Change value stored in dictionary and add corresponding
        pair to heap.  Rebuilds the heap if the number of deleted items grows
        too large, to avoid memory leakage.
        """
        dict.__setitem__(self, key, val)
        heap = self._priorityDictionary__heap
        if len(heap) > 2 * len(self):
            self._priorityDictionary__heap = [(v, k) for k, v in self.iteritems()]
            self._priorityDictionary__heap.sort()
        else:
            newPair = (
             val, key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and newPair < heap[((insertionPoint - 1) // 2)]:
                heap[insertionPoint] = heap[((insertionPoint - 1) // 2)]
                insertionPoint = (insertionPoint - 1) // 2

            heap[insertionPoint] = newPair

    def setdefault(self, key, val):
        """
        Reimplement setdefault to call our customized __setitem__.
        """
        if key not in self:
            self[key] = val
        return self[key]


def Dijkstra(G, start, end=None):
    """
    Find shortest paths from the start vertex to all
    vertices nearer than or equal to the end.

    The input graph G is assumed to have the following
    representation: A vertex can be any object that can
    be used as an index into a dictionary.  G is a
    dictionary, indexed by vertices.  For any vertex v,
    G[v] is itself a dictionary, indexed by the neighbors
    of v.  For any edge v->w, G[v][w] is the length of
    the edge.  This is related to the representation in
    <http://www.python.org/doc/essays/graphs.html>
    where Guido van Rossum suggests representing graphs
    as dictionaries mapping vertices to lists of neighbors,
    however dictionaries of edges have many advantages
    over lists: they can store extra information (here,
    the lengths), they support fast existence tests,
    and they allow easy modification of the graph by edge
    insertion and removal.  Such modifications are not
    needed here but are important in other graph algorithms.
    Since dictionaries obey iterator protocol, a graph
    represented as described here could be handed without
    modification to an algorithm using Guido's representation.

    Of course, G and G[v] need not be Python dict objects;
    they can be any other object that obeys dict protocol,
    for instance a wrapper in which vertices are URLs
    and a call to G[v] loads the web page and finds its links.

    The output is a pair (D,P) where D[v] is the distance
    from start to v and P[v] is the predecessor of v along
    the shortest path from s to v.

    Dijkstra's algorithm is only guaranteed to work correctly
    when all edge lengths are positive. This code does not
    verify this property for all edges (only the edges seen
    before the end vertex is reached), but will correctly
    compute shortest paths even for some graphs with negative
    edges, and will raise an exception if it discovers that
    a negative edge has caused it to make a mistake.
    """
    D = {}
    P = {}
    Q = priorityDictionary()
    Q[start] = 0
    for v in Q:
        D[v] = Q[v]
        if v == end:
            break
        for w in G[v]:
            vwLength = D[v] + G[v][w]
            if w in D:
                if vwLength < D[w]:
                    raise ValueError
                elif w not in Q or vwLength < Q[w]:
                    Q[w] = vwLength
                    P[w] = v

    return (
     D, P)


def shortestPath(G, start, end):
    """
    Find a single shortest path from the given start vertex
    to the given end vertex.
    The input has the same conventions as Dijkstra().
    The output is a list of the vertices in order along
    the shortest path.
    """
    D, P = Dijkstra(G, start, end)
    Path = []
    while True:
        Path.append(end)
        if end == start:
            break
        end = P[end]

    Path.reverse()
    return Path


def generate_crystal_matrix(a, b, c, alpha, beta, gamma):
    """
    Calculation of reciprocal lattice parameters and
    orthogonal matrix of crystal orientation
    Am(3,3) -  3*3 - matrics
    ::

        a*  b*cos(gama*)  c*cos(beta*)
        0   b*sin(gama*) -c*sin(beta*)cosAlpha
        0       0         1/c

    :Parameters:
        #. a (Number): Length of a vector.
        #. b (Number): Length of b vector.
        #. c (Number): Length of c vector.
        #. alpha (Number): Angle between b and c in degrees.
        #. beta (Number): Angle between c and a in degrees.
        #. gamma (Number): Angle between a and b in degrees.

    :Returns:
        #. basis (numpy.ndarray): (3X3) numpy array basis.
        #. rbasis (numpy.ndarray): (3X3) numpy array normalized by volume reciprocal basis.
    """
    alpha = alpha * np.pi / 180
    beta = beta * np.pi / 180
    gamma = gamma * np.pi / 180
    cosAlpha = np.cos(alpha)
    sinAlpha = np.sin(alpha)
    cosBeta = np.cos(beta)
    sinBeta = np.sin(beta)
    cosGamma = np.cos(gamma)
    sinGamma = np.sin(gamma)
    vol = a * b * c * np.sqrt(1.0 - cosAlpha ** 2 - cosBeta ** 2 - cosGamma ** 2 + 2.0 * cosAlpha * cosBeta * cosGamma)
    ar = b * c * sinAlpha / vol
    br = a * c * sinBeta / vol
    cr = a * b * sinGamma / vol
    cosalfar = (cosBeta * cosGamma - cosAlpha) / (sinBeta * sinGamma)
    cosbetar = (cosAlpha * cosGamma - cosBeta) / (sinAlpha * sinGamma)
    cosgamar = (cosAlpha * cosBeta - cosGamma) / (sinAlpha * sinBeta)
    alfar = np.arccos(cosalfar)
    betar = np.arccos(cosbetar)
    gamar = np.arccos(cosgamar)
    rbasis = np.array([[ar, br * np.cos(gamar), cr * np.cos(betar)],
     [
      0.0, br * np.sin(gamar), -cr * np.sin(betar) * cosAlpha],
     [
      0.0, 0.0, 1.0 / c]],
      dtype=float)
    basis = np.linalg.inv(rbasis)
    return (basis, rbasis)


def get_crystal_points(crystalMatrix, xPoints, yPoints, zPoints):
    """
    generates crystal point from a crystalMatrix
    """
    latticePoint = []
    for i in range(xPoints):
        for j in range(yPoints):
            for k in range(zPoints):
                point = [
                 i, j, k]
                latticePoint.append(point * crystalMatrix)

    return latticePoint