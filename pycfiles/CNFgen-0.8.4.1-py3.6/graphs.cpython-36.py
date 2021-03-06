# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/graphs.py
# Compiled at: 2019-11-25 09:40:17
# Size of source mod 2**32: 33744 bytes
"""Utilities to manage graph formats and graph files in order to build
formulas that are graph based.
"""
__all__ = [
 'supported_formats',
 'readGraph', 'writeGraph',
 'is_dag', 'has_bipartition', 'bipartite_sets',
 'enumerate_vertices', 'enumerate_edges', 'neighbors',
 'bipartite_random_left_regular', 'bipartite_random_regular',
 'dag_complete_binary_tree', 'dag_pyramid']
_graphformats = {'dag':[
  'kthlist', 'gml', 'dot'], 
 'digraph':[
  'kthlist', 'gml', 'dot', 'dimacs'], 
 'simple':[
  'kthlist', 'gml', 'dot', 'dimacs'], 
 'bipartite':[
  'kthlist', 'matrix', 'gml', 'dot']}

def supported_formats():
    """The graph file formats supported by the library."""
    return _graphformats


import sys
from io import StringIO, BytesIO
import io, os, networkx, networkx.algorithms

def has_dot_library():
    """Test the presence of pydot
    """
    try:
        from networkx import nx_pydot
        import pydot
        del pydot
        return True
    except ImportError:
        pass

    return False


if not has_dot_library():
    for k in list(_graphformats.values()):
        try:
            k.remove('dot')
        except ValueError:
            pass

def _process_graph_io_arguments(iofile, graph_type, file_format, multi_edges):
    """Test if the argument for the graph I/O functions make sense"""
    if not isinstance(iofile, io.TextIOBase):
        if not isinstance(iofile, io.IOBase):
            if not isinstance(iofile, StringIO):
                raise ValueError('The IO stream "{}" does not correspond to a file'.format(iofile))
    else:
        if graph_type not in _graphformats:
            raise ValueError('The graph type must be one of ' + list(_graphformats.keys()))
        else:
            if graph_type in frozenset({'dag', 'digraph'}):
                if multi_edges:
                    grtype = networkx.MultiDiGraph
                else:
                    grtype = networkx.DiGraph
            else:
                if graph_type in frozenset({'bipartite', 'simple'}):
                    if multi_edges:
                        grtype = networkx.MultiGraph
                    else:
                        grtype = networkx.Graph
                else:
                    raise RuntimeError('Unchecked graph type argument: {}'.format(graph_type))
    if file_format == 'autodetect':
        try:
            extension = os.path.splitext(iofile.name)[(-1)][1:]
        except AttributeError:
            raise ValueError('Cannot guess a file format from an IO stream with no name. Please specify the format manually.')

        if extension not in _graphformats[graph_type]:
            raise ValueError('Cannot guess a file format for {} graphs from the extension of "{}". Please specify the format manually.'.format(graph_type, iofile.name))
        else:
            file_format = extension
    else:
        if file_format not in _graphformats[graph_type]:
            raise ValueError('For {} graphs we only support these formats: '.format(graph_type) + _graphformats[graph_type])
        return (grtype, file_format)


def readGraph(input_file, graph_type, file_format='autodetect', multi_edges=False):
    """Read a Graph from file

    The graph are managed using the NetworkX library, and most of the
    input and output formats are the ones supported by it. Plus we
    added support for some more *hackish* formats that are useful
    in applications.

    for the "simple" and "bipartite" types, the graph is actually
    a (Multi)Graph object, while it is a (Multi)DiGraph in case of
    "dag" or "digraph".

    In the case of "dag" type, the graph is guaranteed to be acyclic
    and to pass the ``is_dag`` test. In the case of "bipartite" type,
    the graph is guaranteed to have the two parts labeled and to pass
    the ``has_bipartition`` test.

    Parameters
    -----------
    input_file: str or file-like object
        the input file from which the graph is read. If it is a string
        then the graph is read from a file with that string as
        filename. Otherwise if the input_file is a file object (or
        a text stream), the graph is read from there.

        Input files are assumed to be UTF-8 by default.

    graph_type: string in {"simple","digraph","dag","bipartite"}
        see also :py:func:`cnfformula.graph.supported_formats`

    file_format: string, optional
        The file format that the parser should expect to receive.
        See also :py:func:`cnfformula.graph.supported_formats`. By default
        it tries to autodetect it from the file name extension (when applicable).

    multi_edges: bool,optional
        are multiple edge allowed in the graph? By default this is not allowed.

    Returns
    -------
    a graph object
        one among networkx.DiGraph, networkx.MultiDiGraph,
        networkx.Graph, networkx.MultiGraph object.

    Raises
    ------
    ValueError
        raised when either ``input_file`` is neither a file object
        nor a string, or when ``graph_type`` and ``file_format`` are
        invalid choices.

    IOError
        it is impossible to read the ``input_file``

    See Also
    --------
    writeGraph, is_dag, has_bipartition

    """
    if isinstance(input_file, str):
        with open(input_file, 'r', encoding='utf-8') as (file_handle):
            return readGraph(file_handle, graph_type, file_format, multi_edges)
    else:
        grtype, file_format = _process_graph_io_arguments(input_file, graph_type, file_format, multi_edges)
        if file_format == 'dot':
            G = grtype(networkx.nx_pydot.read_dot(input_file))
        else:
            if file_format == 'gml':
                try:
                    G = grtype(networkx.read_gml(line.encode('ascii') for line in input_file))
                except networkx.NetworkXError as errmsg:
                    raise ValueError('[Parse error in GML input] {} '.format(errmsg))
                except UnicodeEncodeError as errmsg:
                    raise ValueError('[Non-ascii chars in GML file] {} '.format(errmsg))

            else:
                if file_format == 'kthlist':
                    G = _read_graph_kthlist_format(input_file, grtype, bipartition=(graph_type == 'bipartite'))
                else:
                    if file_format == 'dimacs':
                        G = _read_graph_dimacs_format(input_file, grtype)
                    else:
                        if file_format == 'matrix':
                            G = _read_graph_matrix_format(input_file)
                        else:
                            raise RuntimeError('[Internal error] Format {} not implemented'.format(file_format))
        if graph_type == 'dag':
            if not is_dag(G):
                raise ValueError('[Input error] Graph must be acyclic')
        if graph_type == 'bipartite':
            if not has_bipartition(G):
                raise ValueError("[Input error] Graph vertices miss the 'bipartite' 0,1 label.")
    return G


def writeGraph(G, output_file, graph_type, file_format='autodetect'):
    """Write a graph to a file

    Parameters
    -----------
    G : networkx.Graph (or similar)

    output_file: file object
        the output file to which the graph is written. If it is a string
        then the graph is written to a file with that string as
        filename. Otherwise if ``output_file`` is a file object (or
        a text stream), the graph is written there.

        The file is written in UTF-8 by default.

    graph_type: string in {"simple","digraph","dag","bipartite"}
        see also :py:func:`cnfformula.graph.supported_formats`

    file_format: string, optional
        The file format that the parser should expect to receive.
        See also :py:func:`cnfformula.graph.supported_formats`. By default
        it tries to autodetect it from the file name extension (when applicable).

    Returns
    -------
    None

    Raises
    ------
    ValueError
        raised when either ``output_file`` is neither a file object
        nor a string, or when ``graph_type`` and ``file_format`` are
        invalid choices.

    IOError
        it is impossible to write on the ``output_file``

    See Also
    --------
    readGraph

    """
    if isinstance(output_file, str):
        with open(output_file, 'w', encoding='utf-8') as (file_handle):
            return writeGraph(G, file_handle, graph_type, file_format)
    else:
        _, file_format = _process_graph_io_arguments(output_file, graph_type, file_format, False)
        if file_format == 'dot':
            networkx.nx_pydot.write_dot(G, output_file)
        else:
            if file_format == 'gml':
                tempbuffer = io.BytesIO()
                networkx.write_gml(G, tempbuffer)
                print((tempbuffer.getvalue().decode('ascii')), file=output_file)
            else:
                if file_format == 'kthlist':
                    _write_graph_kthlist_format(G, output_file, bipartition=(graph_type == 'bipartite'))
                else:
                    if file_format == 'dimacs':
                        _write_graph_dimacs_format(G, output_file)
                    else:
                        if file_format == 'matrix':
                            _write_graph_matrix_format(G, output_file)
                        else:
                            raise RuntimeError('[Internal error] Format {} not implemented'.format(file_format))


def is_dag(digraph):
    """Test is a directed graph is acyclic

    if the input graph has a member `topologically_sorted' then assumed that
    there is a member `ordered_vertices' and that it is a topological order.

    Arguments:
    - `digraph`: input graph
    """
    if not isinstance(digraph, (networkx.MultiDiGraph, networkx.DiGraph)):
        return False
    else:
        if hasattr(digraph, 'topologically_sorted'):
            if not hasattr(digraph, 'ordered_vertices'):
                raise AssertionError
            else:
                if not digraph.order() == len(digraph.ordered_vertices):
                    raise AssertionError
                elif not set(digraph.nodes()) == set(digraph.ordered_vertices):
                    raise AssertionError
                assert networkx.algorithms.is_directed_acyclic_graph(digraph)
            return True
        return networkx.algorithms.is_directed_acyclic_graph(digraph)


def has_bipartition(G):
    """Check that the graph is labelled with a bipartition

    NetworkX follows the convention that bipartite graphs have their
    vertices labeled with the bipartition. In particular each vertex
    has the 'bipartite' attribute with is either 0 or 1.

    Parameters
    ----------
    G: networkx.Graph

    """
    try:
        for n in G.nodes():
            if G.nodes[n]['bipartite'] not in (0, 1, '0', '1'):
                return False

    except KeyError:
        return False
    else:
        return True


def bipartite_sets(G):
    Left = sorted([v for v, d in G.nodes(data=True) if d['bipartite'] in (0, '0')])
    Right = sorted([v for v, d in G.nodes(data=True) if d['bipartite'] in (1, '1')])
    return (Left, Right)


def enumerate_vertices(graph):
    """Return the ordered list of vertices of `graph`

    Parameters
    ----------
    graph : input graph
    """
    if hasattr(graph, 'ordered_vertices'):
        if not graph.order() == len(graph.ordered_vertices):
            raise AssertionError
        elif not set(graph.nodes()) == set(graph.ordered_vertices):
            raise AssertionError
        return graph.ordered_vertices
    else:
        setattr(graph, 'ordered_vertices', sorted(graph.nodes()))
        return graph.ordered_vertices


def enumerate_edges(graph):
    """Return the ordered list of edges of `graph`

    Parameters
    ----------
    graph : input graph
    """
    if hasattr(graph, 'ordered_edges'):
        assert set(graph.edges()) == set(graph.ordered_edges)
        return graph.ordered_edges
    else:
        setattr(graph, 'ordered_edges', sorted(graph.edges()))
        return graph.ordered_edges


def neighbors(graph, v):
    """Return the ordered list of neighbors ov a vertex

    Parameters
    ----------
    graph : input graph

    v : vertex
    """
    return sorted(graph.neighbors(v))


def _read_graph_kthlist_format(inputfile, graph_class=networkx.DiGraph, bipartition=False):
    """Read a graph from file, in the KTH reverse adjacency lists format.

    If the vertices are listed from to sources to the sinks, then the
    graph is marked as topologically sorted, and any DAG test will be
    answered without running any visit to the graph. Otherwise no
    assumption is made.

    If the file is supposed to represent a bipartite graph (i.e.
    when `bipartition` parameters is true) then each target node of an
    edge will be part of the left side and and each source node will
    be on the right side. Vertices that are never named are considered
    to be isolated vertices on the right side.

    Parameters
    ----------
    inputfile : file object
        file handle of the input

    graph_class: class object
        the graph class to read, one of networkx.DiGraph (default)
        networkx.MultiDiGraph networkx.Graph networkx.MultiGraph

    bipartition : boolean
        enforce that each edge (u,v) is such that u in in the left size

    """
    if graph_class not in [networkx.DiGraph,
     networkx.MultiDiGraph,
     networkx.Graph,
     networkx.MultiGraph]:
        raise ValueError('[Internal error] Attempt to use an unsupported class for graph representation.')
    else:
        G = graph_class()
        G.name = ''
        G.ordered_vertices = []
        topologically_sorted_input = True
        nvertex = -1
        vertex_cnt = -1
        for i, l in enumerate(inputfile.readlines()):
            if l[0] == 'c':
                G.name += l[2:]
                continue
            if len(l.strip()) == 0:
                continue
            if ':' not in l:
                if nvertex >= 0:
                    raise ValueError('[Syntax error] ' + 'Line {} contains a second spec directive.'.format(i))
                nvertex = int(l.strip())
                if nvertex < 0:
                    raise ValueError('[Input error] ' + 'Non negative number of vertices expected at line {}.'.format(i))
                G.add_nodes_from(range(1, nvertex + 1))
                G.ordered_vertices = range(1, nvertex + 1)
            else:
                target, sources = l.split(':')
                target = int(target.strip())
                try:
                    sources = [int(s) for s in sources.split()]
                except ValueError:
                    raise ValueError('[Input error] ' + 'Non integer vertex ID at line {}.'.format(i))

                if len(sources) < 1 or sources[(-1)] != 0:
                    raise ValueError('[Input error] ' + 'Line {} must end with 0.'.format(i))
                if target < 1 or target > nvertex:
                    raise ValueError('[Input error] ' + 'Vertex ID out of range [1,{}] at line {}.'.format(nvertex, i))
                sources.pop()
                if len([x for x in sources if x < 1 or x > nvertex]) > 0:
                    raise ValueError('[Input error] ' + 'Vertex ID out of range [1,{}] at line {}.'.format(nvertex, i))
                for s in sources:
                    if s <= target:
                        topologically_sorted_input = False

                if bipartition:
                    colors = [G.nodes[s]['bipartite'] for s in sources if 'bipartite' in G.nodes[s]]
                    if 'bipartite' in G.nodes[target]:
                        colors += [1 - G.nodes[target]['bipartite']]
                    if len(set(colors)) > 1:
                        raise ValueError('[Input error] ' + 'Greedy bicoloring incompatible with edges in line {}.'.format(i))
                    default_color = 0 if len(colors) == 0 else 1 - colors[0]
                    G.nodes[target]['bipartite'] = default_color
                    for s in sources:
                        G.nodes[s]['bipartite'] = 1 - default_color

                for s in sources:
                    G.add_edge(s, target)

        if bipartition:
            for v in G.ordered_vertices:
                if 'bipartite' not in G.nodes[v]:
                    G.nodes[v]['bipartite'] = 1

        if topologically_sorted_input:
            G.topologically_sorted = True
        if nvertex != G.order():
            raise ValueError('[Input error] ' + '{} vertices expected. Got {} instead.'.format(nvertex, G.order()))
    return G


def _read_graph_dimacs_format(inputfile, graph_class=networkx.Graph):
    """Read a graph simple from file, in the DIMACS edge format.

    Parameters
    ----------
    inputfile : file object
        file handle of the input

    graph_class: class object
        the graph class to read, one of networkx.DiGraph (default)
        networkx.MultiDiGraph networkx.Graph networkx.MultiGraph
    """
    if graph_class not in [networkx.Graph,
     networkx.MultiGraph,
     networkx.DiGraph,
     networkx.MultiDiGraph]:
        raise ValueError('[Internal error] Attempt to use an unsupported class for graph representation.')
    G = graph_class()
    G.name = ''
    n = -1
    m = -1
    m_cnt = 0
    for i, l in enumerate(inputfile.readlines()):
        if l[0] == 'c':
            G.name += l[2:]
        elif l[0] == 'p':
            if n >= 0:
                raise ValueError('[Syntax error] ' + 'Line {} contains a second spec line.'.format(i))
            _, fmt, nstr, mstr = l.split()
            if fmt != 'edge':
                raise ValueError("[Input error] Dimacs 'edge' format expected.")
            n = int(nstr)
            m = int(mstr)
            G.add_nodes_from(range(1, n + 1))
        else:
            if l[0] == 'e':
                m_cnt += 1
                _, v, w = l.split()
                G.add_edge(int(v), int(w))

    if m != m_cnt:
        raise ValueError('[Syntax error] ' + '{} edges were expected.'.format(m))
    return G


def _read_graph_matrix_format(inputfile):
    """Read a bipartite graph from file, in the adjiacency matrix format.

    This is an example of an adjacency matrix for a bipartite graph
    with 9 vertices on one side and 15 on the another side.

    .. 9 15
       1 1 0 1 0 0 0 1 0 0 0 0 0 0 0
       0 1 1 0 1 0 0 0 1 0 0 0 0 0 0
       0 0 1 1 0 1 0 0 0 1 0 0 0 0 0
       0 0 0 1 1 0 1 0 0 0 1 0 0 0 0
       0 0 0 0 1 1 0 1 0 0 0 1 0 0 0
       0 0 0 0 0 1 1 0 1 0 0 0 1 0 0
       0 0 0 0 0 0 1 1 0 1 0 0 0 1 0
       0 0 0 0 0 0 0 1 1 0 1 0 0 0 1
       1 0 0 0 0 0 0 0 1 1 0 1 0 0 0

    Parameters
    ----------
    inputfile: file object
        the file containing the graph specification

    Returns
    -------
    G : networkx.Graph

    """
    G = networkx.Graph()
    G.name = ''

    def scan_integer(inputfile):
        num_buffer = []
        line_cnt = 0
        while len(num_buffer) == 0:
            line = inputfile.readline()
            if len(line) == 0:
                raise StopIteration
            line_cnt += 1
            tokens = line.split()
            if not len(tokens) == 0:
                if tokens[0][0] == '#':
                    pass
                else:
                    try:
                        num_buffer.extend((int(lit), line_cnt) for lit in tokens)
                    except ValueError:
                        raise ValueError('[Syntax error] ' + 'Line {} contains a non numeric entry.'.format(line_cnt))

                    yield num_buffer.pop(0)

    scanner = scan_integer(inputfile)
    try:
        n = next(scanner)[0]
        m = next(scanner)[0]
        for i in range(1, n + 1):
            G.add_node(i, bipartite=0)

        for i in range(n + 1, n + m + 1):
            G.add_node(i, bipartite=1)

        for i in range(1, n + 1):
            for j in range(n + 1, n + m + 1):
                b, l = next(scanner)
                if b == 1:
                    G.add_edge(i, j)
                else:
                    if b == 0:
                        pass
                    else:
                        raise ValueError('[Input error at line {}] Only 0 or 1 are allowed'.format(l))

    except StopIteration:
        raise ValueError('[Input error] Unexpected end of the matrix')

    try:
        b, l = next(scanner)
        raise ValueError('[Input error at line {}] There are more than {}x{} entries'.format(l, n, m))
    except StopIteration:
        pass

    assert has_bipartition(G)
    return G


def _write_graph_kthlist_format(G, output_file, bipartition=False):
    """Wrire a graph to a file, in the KTH reverse adjacency lists format.

    Parameters
    ----------
    G : graph object

    output_file : file object
        file handle of the output

    bipartition : boolean
        only write the left side adjacency lists. This will enforce
        the bipartition where the file is read again
    """
    print(('c {}'.format(G.name)), file=output_file)
    print(('{}'.format(G.order())), file=output_file)
    indices = {v:i for i, v in enumerate((enumerate_vertices(G)), start=1)}
    if bipartition:
        V, _ = bipartite_sets(G)
    else:
        V = enumerate_vertices(G)
    from io import StringIO
    output = StringIO()
    for v in V:
        if G.is_directed():
            nbors = [indices[w] for w in G.predecessors(v)]
        else:
            nbors = [indices[w] for w in G.adj[v].keys()]
        nbors.sort()
        output.write(str(indices[v]) + ' : ')
        output.write(' '.join([str(i) for i in nbors]))
        output.write(' 0\n')

    print((output.getvalue()), file=output_file)


def _write_graph_dimacs_format(G, output_file):
    """Wrire a graph to a file, in DIMACS format.

    Parameters
    ----------
    G : graph object

    output_file : file object
        file handle of the output
    """
    print(('c {}'.format(G.name).strip()), file=output_file)
    vertices = dict((name, index) for index, name in enumerate(G.nodes(), 1))
    edges = G.edges()
    print(('p edge {} {}'.format(len(vertices), len(edges))), file=output_file)
    for v, w in edges:
        print(('e {} {}'.format(vertices[v], vertices[w])), file=output_file)


def _write_graph_matrix_format(G, output_file):
    """Wrire a graph to a file, in "matrix" format.

    Parameters
    ----------
    G : graph object

    output_file : file object
        file handle of the output
    """
    Left, Right = bipartite_sets(G)
    print(('{} {}'.format(len(Left), len(Right))), file=output_file)
    for u in Left:
        adj_row = []
        for v in Right:
            if G.has_edge(u, v):
                adj_row.append('1')
            else:
                adj_row.append('0')

        print((' '.join(adj_row)), file=output_file)


def bipartite_random_left_regular(l, r, d, seed=None):
    """Returns a random bipartite graph with constant left degree.

    Each vertex on the left side has `d` neighbors on the right side,
    picked uniformly at random without repetition.

    Each vertex in the graph has an attribute `bipartite` which is 0
    for the vertices on the left side and 1 for the vertices on the
    right side.

    Parameters
    ----------
    l : int
        vertices on the left side
    r : int
        vertices on the right side
    d : int
        degree on the left side.
    seed : hashable object
        seed the random generator

    Returns
    -------
    networkx.Graph

    Raises
    ------
    ValueError
        unless ``l``, ``r`` and ``d`` are non negative.

    """
    import random
    if seed:
        random.seed(seed)
    if l < 0 or r < 0 or d < 0:
        raise ValueError('bipartite_random_left_regular(l,r,d) needs l,r,d >=0.')
    G = networkx.Graph()
    G.name = 'bipartite_random_left_regular({},{},{})'.format(l, r, d)
    L = list(range(0, l))
    R = list(range(l, l + r))
    d = min(r, d)
    for u in L:
        G.add_node(u, bipartite=0)

    for v in R:
        G.add_node(v, bipartite=1)

    for u in L:
        for v in sorted(random.sample(R, d)):
            G.add_edge(u, v)

    return G


def bipartite_shift(N, M, pattern=[]):
    """Returns a bipartite graph where edges are a fixed shifted sequence.

    The graph has :math:`N` vertices on the left (numbered from
    :math:`1` to :math:`N`), and :math:`M` vertices on the right
    (numbered from :math:`1` to :math:`M`),

    The vertex :math:`1` on the left side has edges to vertices
    :math:`v_1`, :math:`v_2`, :math:`v_3`,... (mod :math:`M`).
    Each other vertex :math:`i>1` on the left side has edges
    :math:`i+v_1`, :math:`i+v_2`, :math:`i+v_3`,... with wrap around
    over :math:`[1..M]`.

    Parameters
    ----------
    N : int
        vertices on the left side
    M : int
        vertices on the right side
    pattern : list(int)
        pattern of neighbors

    Returns
    -------
    networkx.Graph

    Raises
    ------
    ValueError
        unless ``N``, ``M`` are non negative and ``pattern`` has vertices outside the range.

    """
    if N < 1 or M < 1:
        raise ValueError('bipartite_shift(N,M,pattern) needs N,M >= 0.')
    if any([x < 1 or x > M for x in pattern]):
        raise ValueError('bipartite_shift(N,M,pattern) needs 1 <= pattern[i] <= M.')
    G = networkx.Graph()
    G.name = 'bipartite_shift_regular({},{},{})'.format(N, M, pattern)
    L = list(range(1, N + 1))
    R = list(range(N + 1, N + M + 1))
    for u in L:
        G.add_node(u, bipartite=0)

    for v in R:
        G.add_node(v, bipartite=1)

    pattern.sort()
    for u in L:
        for i in pattern:
            G.add_edge(u, N + 1 + (i + u - 2) % M)

    return G


def bipartite_random_regular(l, r, d, seed=None):
    """Returns a random bipartite graph with constant degree on both sides.

    The graph is d-regular on the left side and regular on the right
    size, so it must be that d*l / r is an integer number.

    Each vertex in the graph has an attribute `bipartite` which is 0
    for the vertices on the left side and 1 for the vertices on the
    right side.

    Parameters
    ----------
    l : int
       vertices on the left side
    r : int
       vertices on the right side
    d : int
       degree of vertices at the left side
    seed : hashable object
       seed of random generator

    Returns
    -------
    networkx.Graph

    Raises
    ------
    ValueError
        if one among ``l``, ``r`` and ``d`` is negative or
        if ``r`` does not divides `l*d`

    References
    ----------
    [1] http://...

    """
    import random
    if seed:
        random.seed(seed)
    if l < 0 or r < 0 or d < 0:
        raise ValueError('bipartite_random_regular(l,r,d) needs l,r,d >=0.')
    else:
        if l * d % r != 0:
            raise ValueError('bipartite_random_regular(l,r,d) needs r to divid l*d.')
        G = networkx.Graph()
        G.name = 'bipartite_random_regular({},{},{})'.format(l, r, d)
        L = list(range(0, l))
        R = list(range(l, l + r))
        for u in L:
            G.add_node(u, bipartite=0)

        for v in R:
            G.add_node(v, bipartite=1)

        A = L * d
        B = R * (l * d // r)
        assert len(B) == l * d
    for i in range(l * d):
        for retries in range(3 * d * d):
            ea = random.randint(i, l * d - 1)
            eb = random.randint(i, l * d - 1)
            if not G.has_edge(A[ea], B[eb]):
                G.add_edge(A[ea], B[eb])
                A[i], A[ea] = A[ea], A[i]
                B[i], B[eb] = B[eb], B[i]
                break
        else:
            failure = True
            for ea in range(i, l * d):
                for eb in range(i, l * d):
                    if not G.has_edge(A[ea], B[eb]):
                        failure = False
                        break

                if not failure:
                    break

            if failure:
                return bipartite_random_regular(l, r, d)

    return G


def dag_pyramid(height):
    """Generates the pyramid DAG

    Parameters
    ----------
    height : int
        the height of the tree

    Returns
    -------
    networkx.DiGraph
    """
    D = networkx.DiGraph()
    D.name = 'Pyramid of height {}'.format(height)
    D.ordered_vertices = []
    X = [[('x_{{{},{}}}'.format(h, i), h, i) for i in range(height - h + 1)] for h in range(height + 1)]
    for layer in X:
        for name, h, i in layer:
            D.add_node(name, rank=(h, i))
            D.ordered_vertices.append(name)

    for h in range(1, len(X)):
        for i in range(len(X[h])):
            D.add_edge(X[(h - 1)][i][0], X[h][i][0])
            D.add_edge(X[(h - 1)][(i + 1)][0], X[h][i][0])

    return D


def dag_complete_binary_tree(height):
    """Generates the complete binary tree DAG

    Parameters
    ----------
    height : int
        the height of the tree

    Returns
    -------
    networkx.DiGraph
    """
    D = networkx.DiGraph()
    D.name = 'Complete binary tree of height {}'.format(height)
    D.ordered_vertices = []
    vert = ['v_{}'.format(i) for i in range(1, 2 * 2 ** height)]
    for w in vert:
        D.add_node(w)
        D.ordered_vertices.append(w)

    N = len(vert) - 1
    for i in range(len(vert) // 2):
        D.add_edge(vert[(N - 2 * i - 1)], vert[(N - i)])
        D.add_edge(vert[(N - 2 * i - 2)], vert[(N - i)])

    return D


def sample_missing_edges(G, m, seed=None):
    """Sample m pairs of missing edges in G

    If :math:`G` is not complete and has at least :math:`m` missing edges, :math:`m` of them are sampled.

    Parameters
    ----------
    G : networkx.Graph
        a graph with at least :math:`m` missing edges
    m : int
       the number of missing edges to sample
    seed : hashable object
       seed of random generator

    Returns
    -------
    list of edges

    Raises
    ------
    ValueError
        if :math:`G` doesn't have :math:`m` missing edges
    RuntimeError
        Sampling failure in the sparse case

    """
    import random
    if seed:
        random.seed(seed)
    else:
        from networkx import non_edges
        if m < 0:
            raise ValueError('You can only sample a non negative number of edges.')
        total_number_of_edges = None
        if has_bipartition(G):
            Left, Right = bipartite_sets(G)
            total_number_of_edges = len(Left) * len(Right)

            def edge_sampler():
                u = random.sample(Left, 1)[0]
                v = random.sample(Right, 1)[0]
                return (u, v)

            def available_edges():
                return [(u, v) for u in Left if not G.has_edge(u, v) for v in Right]

        else:
            total_number_of_edges = G.order() * (G.order() - 1) / 2

        def edge_sampler():
            return random.sample(G.nodes(), 2)

        def available_edges():
            return list(non_edges(G))

    number_avaiable_edges = total_number_of_edges - G.number_of_edges()
    if number_avaiable_edges < m:
        raise ValueError('The graph does not have {} missing edges to sample.'.format(m))
    if G.number_of_edges() + m >= total_number_of_edges / 2:
        return random.sample(available_edges(), m)
    missing_edges = set()
    for _ in range(100 * m):
        if len(missing_edges) >= m:
            break
        u, v = edge_sampler()
        if (u, v) not in missing_edges and (
         v, u) not in missing_edges and not G.has_edge(u, v):
            missing_edges.add((u, v))

    if len(missing_edges) >= m:
        return missing_edges
    raise RuntimeError('Improbable failure at sampling missing edges in a sparse graph.')