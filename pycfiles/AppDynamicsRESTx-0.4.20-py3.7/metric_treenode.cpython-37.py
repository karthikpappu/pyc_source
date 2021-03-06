# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/appd/model/metric_treenode.py
# Compiled at: 2020-03-11 17:54:36
# Size of source mod 2**32: 1700 bytes
"""
Model classes for AppDynamics REST API

.. moduleauthor:: Todd Radel <tradel@appdynamics.com>
"""
from . import JsonObject, JsonList

class MetricTreeNode(JsonObject):
    FIELDS = {'name':'', 
     'type':''}
    NODE_TYPES = ('leaf', 'folder')

    def __init__(self, parent=None, node_name='', node_type=''):
        self.parent, self.name, self.type = parent, node_name, node_type
        self._children = MetricTreeNodes()
        if parent:
            parent._children.append(self)

    @property
    def path(self):
        n = self
        stack = []
        while n:
            stack.insert(0, n.name)
            n = n.parent

        return '|'.join(stack)


class MetricTreeNodes(JsonList):

    def __init__(self, initial_list=None, parent=None):
        super(MetricTreeNodes, self).__init__(MetricTreeNode, initial_list)
        self.parent = parent
        if parent:
            if not isinstance(parent, MetricTreeNode):
                raise TypeError('was expecting a MetricTreeNode')
            for x in self.data:
                x.parent = parent

    def __getitem__(self, i):
        """
        :rtype: MetricTreeNode
        """
        return self.data[i]

    @classmethod
    def from_json(cls, json_list, parent=None):
        return cls(json_list, parent)

    def by_name(self, name):
        """
        Finds a tree node with the matching name.

        :param str name: Variable name to find.
        :return: Metric tree node matching the name.
        :rtype: appd.model.MetricTreeNode
        """
        found = [x for x in self.data if x.name == name]
        try:
            return found[0]
        except IndexError:
            raise KeyError(name)