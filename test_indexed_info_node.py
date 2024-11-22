#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 13:13:49 2024

@author: magfrump
"""

import unittest
import indexed_info_node as iin
import json

class TextInfoNode(unittest.TestCase):
    def test_write_to_file(self):
        filename = "test.json"
        children = [iin.ChildNode("child1","This is a child node")]
        data = iin.NodeMetaData(0,1,"test","INDEX")
        node = iin.IndexedInfoNode(children, data, "")
        node.write_to_file(filename)
        with open(filename) as f:
            self.assertEqual(json.loads(f.read()),
                             {"children": [{"reference":"child1",
                                            "summary": "This is a child node"}],
                              "text": "",
                              "created":0,
                              "updated":1,
                              "source": "test",
                              "type": "INDEX"})
            
    def test_read_from_file(self):
        filename = "test.json"
        children = [iin.ChildNode("child1","This is a child node")]
        data = iin.NodeMetaData(0,1,"test","INDEX")
        node = iin.IndexedInfoNode(children, data, "")
        raw = {"children": [{"reference":"child1",
                       "summary": "This is a child node"}],
         "text": "",
         "created":0,
         "updated":1,
         "source": "test",
         "type": "INDEX"}
        with open(filename, 'w') as f:
            json.dump(raw, f)
        node2 = iin.IndexedInfoNode.fromfilename(filename)
        self.assertEqual(node, node2)
            

if __name__ == '__main__':
    unittest.main()