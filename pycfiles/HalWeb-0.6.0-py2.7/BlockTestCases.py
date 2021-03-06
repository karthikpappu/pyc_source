# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/tests/BlockTestCases.py
# Compiled at: 2011-12-25 05:31:43
"""
Created on Oct 31, 2010

@author: KMihajlov
"""
import unittest, os
from os.path import join as pjoin
from halicea.lib.baseClasses import Block, BlockTypes
from halicea.lib.codeBlocksHelpers import *
import sys
resDir = pjoin(os.path.dirname(__file__), 'resources')

class BlockTestCases(unittest.TestCase):
    """A Test Class for the Block Class"""

    def setUp(self):
        self.bl = Block(None, 'root', blType=BlockTypes.BLOCK)
        self.chld1 = Block(None, 'child1', BlockTypes.LINE)
        self.chld2 = Block(None, 'child2', BlockTypes.BLOCK)
        self.chld3 = Block(None, 'grandchild3', BlockTypes.LINE)
        return

    def test_AddBlock(self):
        self.bl.append(self.chld1)
        self.bl.append(self.chld2)
        self.bl.Children[0].append(self.chld3)
        self.assertTrue(len(self.bl.Children) == 2)
        self.assertEquals(self.bl.Children[0].Name, 'child1')
        self.assertEquals(self.bl.Children[1].Name, 'child2')
        self.assertEquals(self.bl.Children[0].Children[0].Name, 'grandchild3')

    def test_GetChild(self):
        self.test_AddBlock()
        self.assertEqual(self.chld1.Name, self.bl['child1'].Name)

    def test_GetRecursive(self):
        self.test_AddBlock()
        t1 = self.bl['child1.grandchild3']
        self.assertFalse(t1 == None)
        self.assertEquals(t1.Name, 'grandchild3')
        return

    def test_RemoveBlock(self):
        self.test_AddBlock()
        rmb = self.bl.Children[0]
        self.bl.remove(rmb)
        self.assertTrue(len(self.bl.Children) == 1)

    def test_loadFromFile(self):
        m = Block.loadFromFile(pjoin(resDir, 'testBlockTree.html'))
        pybl = Block.loadFromFile(pjoin(resDir, 'testControllerBlocks.txt'), cbl=InPythonBlockLocator())
        self.assertEquals(m['root'].Name, 'root')
        self.assertEquals(m['root.child'].Name, 'child')
        self.assertEquals(pybl['ApplicationControllers'].Name, 'ApplicationControllers')
        locator = GenericCbl(lambda x: x.replace(' ', '').find('{%block') > -1 and strBetween(x.replace(' ', ''), '{%block', '%}') or None, lambda x: x.replace(' ', '').find('{%endblock%}') > -1)
        m = Block.loadFromFile(pjoin(resDir, 'testBlockTree.html'), locator)
        self.assertEquals(m['root'].Name, 'root')
        self.assertEquals(m['root.child'].Name, 'child')

    def test_LinesNumber(self):
        root = Block(None, 'root', blType=BlockTypes.BLOCK)
        for t in range(1, 51):
            root.append(Block.createLineBlock('Line ' + str(t)))

        self.assertEqual(root.LineCount, 50)
        root = Block.loadFromFile(pjoin(resDir, 'testControllerBlocks.txt'))
        self.assertEquals(root.LineCount, 30)
        return

    def test_appendInBlock(self):
        cbl = InPythonBlockLocator()
        m = Block.loadFromFile(pjoin(resDir, 'testBlockTree.html'))
        pybl = Block.loadFromFile(pjoin(resDir, 'testControllerBlocks.txt'), cbl)
        pybl['ApplicationControllers'].append(Block.createEmptyBlock('TestControllers', cbl))
        pybl['ApplicationControllers.TestControllers'].append(Block.createLineBlock('bla bla bla'))
        f = open(pjoin(resDir, 'testControllerBlocks_rez.txt'), 'w')
        f.write(str(pybl))
        f.close()

    def test_Str(self):
        testBlock1 = '\n            {%block root%}\n            {%endblock%}\n            some aditional Text\n            {%block one line %}\n            Text 2\n            Text 3'
        invalidBlock = '\n            test1\n            {%block test %}\n                test1\n                {%block test %}\n            bla bla bla'
        bl1 = Block.loadFromLines(testBlock1.split('\n'), 'main')
        bl2 = Block.loadFromLines(invalidBlock.split('\n'), 'main')
        self.assertEquals(bl1.__str__(), testBlock1)
        self.assertEquals(bl2.__str__(), invalidBlock)
        bl2['test.test'].append(Block.createLineBlock('bla bla bla'))
        self.assertEquals(bl2.__str__(), invalidBlock + '\nbla bla bla')