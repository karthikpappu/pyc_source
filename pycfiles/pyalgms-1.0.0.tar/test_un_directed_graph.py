# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/horn/Code/pythonprojects/py_alg_dat/testsuite/test_un_directed_graph.py
# Compiled at: 2016-08-31 21:57:00
__doc__ = '\nTest UnDirectedGraph class.\n'
import unittest, copy
from py_alg_dat import dfs_edge_classification
from py_alg_dat import graph
from py_alg_dat import graph_edge
from py_alg_dat import graph_vertex

class TestUnDirectedGraph(unittest.TestCase):
    """
    Test UnDirectedGraph class.
    """

    def setUp(self):
        self.g_1 = graph.UnDirectedGraph(7)
        self.v_1 = graph_vertex.UnWeightedGraphVertex(self.g_1, 'A')
        self.v_2 = graph_vertex.UnWeightedGraphVertex(self.g_1, 'B')
        self.v_3 = graph_vertex.UnWeightedGraphVertex(self.g_1, 'C')
        self.v_4 = graph_vertex.UnWeightedGraphVertex(self.g_1, 'D')
        self.v_5 = graph_vertex.UnWeightedGraphVertex(self.g_1, 'E')
        self.v_6 = graph_vertex.UnWeightedGraphVertex(self.g_1, 'F')
        self.v_7 = graph_vertex.UnWeightedGraphVertex(self.g_1, 'G')
        self.g_1.add_vertex(self.v_1)
        self.g_1.add_vertex(self.v_2)
        self.g_1.add_vertex(self.v_3)
        self.g_1.add_vertex(self.v_4)
        self.g_1.add_vertex(self.v_5)
        self.g_1.add_vertex(self.v_6)
        self.g_1.add_vertex(self.v_7)
        self.e12 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_1, self.v_2)
        self.e21 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_2, self.v_1)
        self.e14 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_1, self.v_4)
        self.e41 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_4, self.v_1)
        self.e23 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_2, self.v_3)
        self.e32 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_3, self.v_2)
        self.e24 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_2, self.v_4)
        self.e42 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_4, self.v_2)
        self.e25 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_2, self.v_5)
        self.e52 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_5, self.v_2)
        self.e35 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_3, self.v_5)
        self.e53 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_5, self.v_3)
        self.e45 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_4, self.v_5)
        self.e54 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_5, self.v_4)
        self.e46 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_4, self.v_6)
        self.e64 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_6, self.v_4)
        self.e56 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_5, self.v_6)
        self.e65 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_6, self.v_5)
        self.e57 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_5, self.v_7)
        self.e75 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_7, self.v_5)
        self.e67 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_6, self.v_7)
        self.e76 = graph_edge.UnDirectedGraphEdge(self.g_1, self.v_7, self.v_6)
        self.g_1.add_edge(self.v_1, self.v_2)
        self.g_1.add_edge(self.v_1, self.v_4)
        self.g_1.add_edge(self.v_2, self.v_3)
        self.g_1.add_edge(self.v_2, self.v_4)
        self.g_1.add_edge(self.v_2, self.v_5)
        self.g_1.add_edge(self.v_3, self.v_5)
        self.g_1.add_edge(self.v_4, self.v_5)
        self.g_1.add_edge(self.v_4, self.v_6)
        self.g_1.add_edge(self.v_5, self.v_6)
        self.g_1.add_edge(self.v_5, self.v_7)
        self.g_1.add_edge(self.v_6, self.v_7)

    def test_un_directed_graph_copy(self):
        """
        Test operator "copy".
        """
        a_graph = graph.UnDirectedGraph(5)
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        v_5 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_vertex(v_5)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_1, v_3)
        a_graph.add_edge(v_1, v_4)
        a_graph.add_edge(v_1, v_5)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_2, v_4)
        a_graph.add_edge(v_2, v_5)
        a_graph.add_edge(v_3, v_4)
        a_graph.add_edge(v_3, v_5)
        a_graph.add_edge(v_4, v_5)
        ref = copy.copy(a_graph)
        self.assertEqual(a_graph, ref)

    def test_un_directed_graph_len(self):
        """
        Test operator "len".
        """
        self.assertEqual(7, len(self.g_1))

    def test_un_directed_graph_get_item(self):
        """
        Test operator "get_item".
        """
        self.assertEqual(self.g_1.get_vertex_at_index(3), self.g_1[3])

    def test_un_directed_graph_get_number_of_vertices(self):
        """
        Test method "get_number_of_vertices".
        """
        self.assertEqual(7, self.g_1.get_number_of_vertices())

    def test_un_directed_graph_get_number_of_edges(self):
        """
        Test method "get_number_of_edges".
        """
        self.assertEqual(22, self.g_1.get_number_of_edges())

    def test_un_directed_graph_get_vertices(self):
        """
        Test method "get_vertices".
        """
        list1 = []
        list1.append(self.v_1)
        list1.append(self.v_2)
        list1.append(self.v_3)
        list1.append(self.v_4)
        list1.append(self.v_5)
        list1.append(self.v_6)
        list1.append(self.v_7)
        list2 = []
        for i in self.g_1.get_vertices():
            list2.append(i)

        s_list1 = sorted(list1, key=lambda vertex: vertex.vertex_number)
        s_list2 = sorted(list2, key=lambda vertex: vertex.vertex_number)
        self.assertEqual(s_list1, s_list2)

    def test_un_directed_graph_get_edges(self):
        """
        Test method "get_edges".
        """
        list1 = []
        list1.append(self.e12)
        list1.append(self.e21)
        list1.append(self.e14)
        list1.append(self.e41)
        list1.append(self.e23)
        list1.append(self.e32)
        list1.append(self.e24)
        list1.append(self.e42)
        list1.append(self.e25)
        list1.append(self.e52)
        list1.append(self.e35)
        list1.append(self.e53)
        list1.append(self.e45)
        list1.append(self.e54)
        list1.append(self.e46)
        list1.append(self.e64)
        list1.append(self.e56)
        list1.append(self.e65)
        list1.append(self.e57)
        list1.append(self.e75)
        list1.append(self.e67)
        list1.append(self.e76)
        list2 = []
        for i in self.g_1.get_edges():
            list2.append(i)

        s_list1 = sorted(list1, key=lambda edge: (edge.head_vertex, edge.tail_vertex))
        s_list2 = sorted(list2, key=lambda edge: (edge.head_vertex, edge.tail_vertex))
        self.assertEqual(s_list1, s_list2)

    def test_un_directed_graph_get_edge(self):
        """
        Test method "get_edge".
        """
        self.assertEqual(self.e12, self.g_1.get_edge(self.v_1, self.v_2))

    def test_un_directed_graph_is_edge(self):
        """
        Test method "is_edge".
        """
        try:
            self.assertTrue(self.g_1.is_edge(self.v_1, self.v_2))
        except KeyError:
            print 'Exception caught: %s' % str(KeyError)

    def test_un_directed_graph_remove_vertex_v_0(self):
        """
        Test method "remove_vertex".
        """
        a_graph = graph.UnDirectedGraph(5)
        v_0 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(v_0)
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_edge(v_0, v_1)
        a_graph.add_edge(v_0, v_2)
        a_graph.add_edge(v_0, v_3)
        a_graph.add_edge(v_0, v_4)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_1, v_3)
        a_graph.add_edge(v_1, v_4)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_2, v_4)
        a_graph.add_edge(v_3, v_4)
        g_ref = graph.UnDirectedGraph(4)
        v_1_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'B')
        v_2_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'C')
        v_3_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'D')
        v_4_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'E')
        g_ref.add_vertex(v_1_ref)
        g_ref.add_vertex(v_2_ref)
        g_ref.add_vertex(v_3_ref)
        g_ref.add_vertex(v_4_ref)
        g_ref.add_edge(v_1_ref, v_2_ref)
        g_ref.add_edge(v_1_ref, v_3_ref)
        g_ref.add_edge(v_1_ref, v_4_ref)
        g_ref.add_edge(v_2_ref, v_3_ref)
        g_ref.add_edge(v_2_ref, v_4_ref)
        g_ref.add_edge(v_3_ref, v_4_ref)
        a_graph.remove_vertex(v_0)
        self.assertEqual(g_ref, a_graph)

    def test_un_directed_graph_remove_vertex_v_1(self):
        """
        Test method "remove_vertex".
        """
        a_graph = graph.UnDirectedGraph(5)
        v_0 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(v_0)
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_edge(v_0, v_1)
        a_graph.add_edge(v_0, v_2)
        a_graph.add_edge(v_0, v_3)
        a_graph.add_edge(v_0, v_4)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_1, v_3)
        a_graph.add_edge(v_1, v_4)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_2, v_4)
        a_graph.add_edge(v_3, v_4)
        g_ref = graph.UnDirectedGraph(4)
        v_0_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'A')
        v_2_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'C')
        v_3_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'D')
        v_4_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'E')
        g_ref.add_vertex(v_0_ref)
        g_ref.add_vertex(v_2_ref)
        g_ref.add_vertex(v_3_ref)
        g_ref.add_vertex(v_4_ref)
        g_ref.add_edge(v_0_ref, v_2_ref)
        g_ref.add_edge(v_0_ref, v_3_ref)
        g_ref.add_edge(v_0_ref, v_4_ref)
        g_ref.add_edge(v_2_ref, v_3_ref)
        g_ref.add_edge(v_2_ref, v_4_ref)
        g_ref.add_edge(v_3_ref, v_4_ref)
        a_graph.remove_vertex(v_1)
        self.assertEqual(g_ref, a_graph)

    def test_un_directed_graph_remove_vertex_v_2(self):
        """
        Test method "remove_vertex".
        """
        a_graph = graph.UnDirectedGraph(5)
        v_0 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(v_0)
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_edge(v_0, v_1)
        a_graph.add_edge(v_0, v_2)
        a_graph.add_edge(v_0, v_3)
        a_graph.add_edge(v_0, v_4)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_1, v_3)
        a_graph.add_edge(v_1, v_4)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_2, v_4)
        a_graph.add_edge(v_3, v_4)
        g_ref = graph.UnDirectedGraph(4)
        v_0_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'A')
        v_1_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'B')
        v_3_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'D')
        v_4_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'E')
        g_ref.add_vertex(v_0_ref)
        g_ref.add_vertex(v_1_ref)
        g_ref.add_vertex(v_3_ref)
        g_ref.add_vertex(v_4_ref)
        g_ref.add_edge(v_0_ref, v_1_ref)
        g_ref.add_edge(v_0_ref, v_3_ref)
        g_ref.add_edge(v_0_ref, v_4_ref)
        g_ref.add_edge(v_1_ref, v_3_ref)
        g_ref.add_edge(v_1_ref, v_4_ref)
        g_ref.add_edge(v_3_ref, v_4_ref)
        a_graph.remove_vertex(v_2)
        self.assertEqual(g_ref, a_graph)

    def test_un_directed_graph_remove_vertex_v_3(self):
        """
        Test method "remove_vertex".
        """
        a_graph = graph.UnDirectedGraph(5)
        v_0 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(v_0)
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_edge(v_0, v_1)
        a_graph.add_edge(v_0, v_2)
        a_graph.add_edge(v_0, v_3)
        a_graph.add_edge(v_0, v_4)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_1, v_3)
        a_graph.add_edge(v_1, v_4)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_2, v_4)
        a_graph.add_edge(v_3, v_4)
        g_ref = graph.UnDirectedGraph(4)
        v_0_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'A')
        v_1_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'B')
        v_2_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'C')
        v_4_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'E')
        g_ref.add_vertex(v_0_ref)
        g_ref.add_vertex(v_1_ref)
        g_ref.add_vertex(v_2_ref)
        g_ref.add_vertex(v_4_ref)
        g_ref.add_edge(v_0_ref, v_1_ref)
        g_ref.add_edge(v_0_ref, v_2_ref)
        g_ref.add_edge(v_0_ref, v_4_ref)
        g_ref.add_edge(v_1_ref, v_2_ref)
        g_ref.add_edge(v_1_ref, v_4_ref)
        g_ref.add_edge(v_2_ref, v_4_ref)
        a_graph.remove_vertex(v_3)
        self.assertEqual(g_ref, a_graph)

    def test_un_directed_graph_remove_vertex_v_4(self):
        """
        Test method "remove_vertex".
        """
        a_graph = graph.UnDirectedGraph(5)
        v_0 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'E')
        a_graph.add_vertex(v_0)
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_edge(v_0, v_1)
        a_graph.add_edge(v_0, v_2)
        a_graph.add_edge(v_0, v_3)
        a_graph.add_edge(v_0, v_4)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_1, v_3)
        a_graph.add_edge(v_1, v_4)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_2, v_4)
        a_graph.add_edge(v_3, v_4)
        g_ref = graph.UnDirectedGraph(4)
        v_0_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'A')
        v_1_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'B')
        v_2_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'C')
        v_3_ref = graph_vertex.UnWeightedGraphVertex(g_ref, 'D')
        g_ref.add_vertex(v_0_ref)
        g_ref.add_vertex(v_1_ref)
        g_ref.add_vertex(v_2_ref)
        g_ref.add_vertex(v_3_ref)
        g_ref.add_edge(v_0_ref, v_1_ref)
        g_ref.add_edge(v_0_ref, v_2_ref)
        g_ref.add_edge(v_0_ref, v_3_ref)
        g_ref.add_edge(v_1_ref, v_2_ref)
        g_ref.add_edge(v_1_ref, v_3_ref)
        g_ref.add_edge(v_2_ref, v_3_ref)
        a_graph.remove_vertex(v_4)
        self.assertEqual(g_ref, a_graph)

    def test_un_directed_graph_is_directed(self):
        """
        Test method "is_directed".
        """
        self.assertFalse(self.g_1.is_directed())

    def test_un_directed_graph_is_connected(self):
        """
        Test method "is_connected".
        """
        self.assertTrue(self.g_1.is_connected())

    def test_un_directed_graph_is_connected_not(self):
        """
        Test method "is_connected" - inverted.
        """
        a_graph = graph.UnDirectedGraph(4)
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_2, v_1)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_3, v_2)
        a_graph.add_edge(v_1, v_3)
        a_graph.add_edge(v_3, v_1)
        self.assertFalse(a_graph.is_connected())

    def test_un_directed_graph_is_cyclic(self):
        """
        Test method "is_cyclic".
        """
        a_graph = graph.UnDirectedGraph(4)
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_1, v_3)
        self.assertTrue(a_graph.is_cyclic())

    def test_un_directed_graph_is_cyclic_not(self):
        """
        Test method "is_cyclic" - inverted.
        """
        a_graph = graph.UnDirectedGraph(4)
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_2, v_4)
        self.assertFalse(a_graph.is_cyclic())

    def test_un_directed_graph_get_vertex_at_index(self):
        """
        Test method "get_vertex_at_index".
        """
        self.assertEqual(self.v_4, self.g_1.get_vertex_at_index(3))

    def test_un_directed_graph_get_emanating_edges(self):
        """
        Test method "get_emanating_edges".
        """
        ref = []
        res = []
        ref.append(self.e12)
        ref.append(self.e14)
        res = self.g_1.get_emanating_edges(self.v_1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_un_directed_graph_get_incident_edges(self):
        """
        Test method "get_incident_edges".
        """
        ref = []
        res = []
        ref.append(self.e12)
        ref.append(self.e14)
        res = self.g_1.get_incident_edges(self.v_1.get_vertex_number())
        self.assertEqual(ref, res)

    def test_un_directed_graph_has_vertex(self):
        """
        Test method "has_vertex".
        """
        a_graph = graph.UnDirectedGraph(1)
        a_vertex = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        a_graph.add_vertex(a_vertex)
        self.assertTrue(a_graph.has_vertex(a_vertex))

    def test_un_directed_graph_has_vertex_not(self):
        """
        Test method "has_vertex" - inverted.
        """
        a_graph = graph.UnDirectedGraph(1)
        a_vertex = graph_vertex.UnWeightedGraphVertex(a_graph, 'BB')
        self.assertFalse(a_graph.has_vertex(a_vertex))

    def test_un_directed_graph_classify_edges_cyclic(self):
        """
        Test method "classify_edges" - cyclic graph.
        """
        a_graph = graph.UnDirectedGraph(4)
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_1, v_3)
        res = a_graph.classify_edges().get_edges()
        ref = dfs_edge_classification.DFSEdgeClassification(a_graph).get_edges()
        e12 = graph_edge.UnDirectedGraphEdge(a_graph, v_1, v_2)
        e23 = graph_edge.UnDirectedGraphEdge(a_graph, v_2, v_3)
        e13 = graph_edge.UnDirectedGraphEdge(a_graph, v_3, v_1)
        ref[e12] = graph_edge.EdgeClassification.TREE_EDGE
        ref[e23] = graph_edge.EdgeClassification.TREE_EDGE
        ref[e13] = graph_edge.EdgeClassification.BACK_EDGE
        self.assertEqual(res, ref)

    def test_un_directed_graph_classify_edges_acyclic(self):
        """
        Test method "classify_edges" - acyclic graph.
        """
        a_graph = graph.UnDirectedGraph(4)
        v_1 = graph_vertex.UnWeightedGraphVertex(a_graph, 'A')
        v_2 = graph_vertex.UnWeightedGraphVertex(a_graph, 'B')
        v_3 = graph_vertex.UnWeightedGraphVertex(a_graph, 'C')
        v_4 = graph_vertex.UnWeightedGraphVertex(a_graph, 'D')
        a_graph.add_vertex(v_1)
        a_graph.add_vertex(v_2)
        a_graph.add_vertex(v_3)
        a_graph.add_vertex(v_4)
        a_graph.add_edge(v_1, v_2)
        a_graph.add_edge(v_2, v_3)
        a_graph.add_edge(v_2, v_4)
        res = a_graph.classify_edges().get_edges()
        ref = dfs_edge_classification.DFSEdgeClassification(a_graph).get_edges()
        e12 = graph_edge.UnDirectedGraphEdge(a_graph, v_1, v_2)
        e23 = graph_edge.UnDirectedGraphEdge(a_graph, v_2, v_3)
        e24 = graph_edge.UnDirectedGraphEdge(a_graph, v_2, v_4)
        ref[e12] = graph_edge.EdgeClassification.TREE_EDGE
        ref[e23] = graph_edge.EdgeClassification.TREE_EDGE
        ref[e24] = graph_edge.EdgeClassification.TREE_EDGE
        self.assertEqual(res, ref)