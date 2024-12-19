#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:26:13 2024

@author: magfrump
"""

import knowledge_graph as kg

def append_to_knowledge_graph(index_node, new_docs):
    """
    Given the index of a knowledge graph and a list of new documents,
    breaks the documents into chunks with summaries and writes these
    to disk.

    Args:
        index_node (str): the filename of the existing knowledge graph
            index.
        new_docs (List[str]): the contents of the new documents to be
            added to the graph.

    Returns:
        str: the filename of the new knowledge graph index.
    """

    parsed_docs = [kg.KnowledgeGraph(new_docs[i], 400, 20, 10, "web doc "+i) \
                    for i in range(len(new_docs))]

    for pardoc in parsed_docs:
        pardoc.write_doc_to_dir("data", pardoc.source)
