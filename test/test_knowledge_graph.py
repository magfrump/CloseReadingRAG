#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 13:54:33 2024

@author: magfrump
"""

import unittest
import knowledge_graph as kg


class TestKnowledgeGraph(unittest.TestCase):
    #def setUp(self):
    #    self._kg = knowledge_graph.KnowledgeGraph()
        
    def test_basic_graph(self):
        input_documents = ["here's a big old sentence for you to split up lol"]
        chunk_length = 10
        chunk_overlap = 2
        graph = kg.KnowledgeGraph(input_documents, chunk_length, chunk_overlap, max_subtopics=10)
        #graph.print()
        self.assertEqual(graph.num_subtopics, 6)
        self.assertEqual(graph.get_subtopic(0).get_text(), "here's a b")
        self.assertEqual(graph.get_subtopic(1).get_text(), " big old s")
        self.assertEqual(graph.get_subtopic(2).get_text(), " sentence ")
        self.assertEqual(graph.get_subtopic(3).get_text(), "e for you ")
        self.assertEqual(graph.get_subtopic(4).get_text(), "u to split")
        self.assertEqual(graph.get_subtopic(5).get_text(), "it up lol")

    def test_deep_graph(self):
        input_documents = ["here's a big old sentence for you to split up lol"]
        print("FNORD 2")
        graph = kg.KnowledgeGraph(input_documents, chunk_length=9, chunk_overlap=2, max_subtopics=5)
        #graph.print()
        
        self.assertEqual(graph.num_subtopics, 1)
        self.assertEqual(graph.get_subtopic(0).num_subtopics, 4)
        self.assertEqual(graph.get_subtopic(0).get_subtopic(0).num_subtopics, 2)
        self.assertEqual(graph.get_subtopic(0).get_subtopic(0).get_subtopic(0).get_text(), "here's a ")
        self.assertEqual(graph.get_subtopic(0).get_subtopic(0).get_subtopic(1).get_text(), "a big old")
        self.assertEqual(graph.get_subtopic(0).get_subtopic(1).num_subtopics, 2)
        self.assertEqual(graph.get_subtopic(0).get_subtopic(1).get_subtopic(0).get_text(), "ld senten")
        self.assertEqual(graph.get_subtopic(0).get_subtopic(1).get_subtopic(1).get_text(), "ence for ")
        self.assertEqual(graph.get_subtopic(0).get_subtopic(2).num_subtopics, 2)
        self.assertEqual(graph.get_subtopic(0).get_subtopic(2).get_subtopic(0).get_text(), "r you to ")
        self.assertEqual(graph.get_subtopic(0).get_subtopic(2).get_subtopic(1).get_text(), "o split u")
        self.assertEqual(graph.get_subtopic(0).get_subtopic(3).get_text(), " up lol")

    def test_bigger_document(self):
        input_documents = []
        with open('test/test_text_1.txt', 'r') as file:
            input_documents.append(file.read())
        with open('test/test_text_2.txt', 'r') as file:
            input_documents.append(file.read())
        
        graph = kg.KnowledgeGraph(input_documents, chunk_length = 4000, chunk_overlap = 20, max_subtopics = 10)
        graph.print()

if __name__ == '__main__':
    unittest.main()
