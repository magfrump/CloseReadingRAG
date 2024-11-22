#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:28:15 2024

@author: magfrump
"""
import json

class LookupIndex:
    def __init__(self, index_description: str, docs: list):
        self.index_description = index_description
        self.docs = docs
        self.subtopics = []

    def add_subtopic(self, subtopic: 'LookupIndex') -> None:
        if subtopic.specificity > self.specificity:
            self.subtopics.append(subtopic)
            

def read_index_from_file(filename: str) -> LookupIndex:
    with open(filename, 'r') as f:
        data = json.load(f)
        index = LookupIndex(data['index_description'], data['docs'])
        for subtopic in data['subtopics']:
            subtopic_instance = LookupIndex(subtopic['description'], subtopic['docs'],
specificity=subtopic['specificity'])
            index.add_subtopic(subtopic_instance, subtopic['specificity'])
        return index

def write_index_to_file(index: LookupIndex, filename: str) -> None:
    data = {
        'index_description': index.index_description,
        'docs': index.docs,
        'subtopics': []
    }
    for subtopic in index.subtopics:
        subtopic_data = {
            'description': subtopic.index_description,
            'docs': subtopic.docs,
            'specificity': subtopic.specificity
        }
        data['subtopics'].append(subtopic_data)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        
        
        
class Node:
    def __init__(self, topic, children=None):
        self.topic = topic
        self.children = children if children else {}
        self.id = None  # assigned when serialized

def serialize_node(node):
    # Serialize the node to a binary format (e.g., Protocol Buffers)
    return node.topic.encode('utf-8') + b'\x00' + serialize_children(node.children)

def deserialize_node(data):
    # Deserialize the node from a binary format
    topic, children_data = data.split(b'\x00', 1)
    return Node(topic.decode('utf-8'), deserialize_children(children_data))

def create_index(nodes):
    index = {}
    for node in nodes:
        index[node.topic] = node.id
    return index


class Library:
    def __init__(self):
        self.cache = {}  # cache for frequently accessed nodes
        self.index = None  # index mapping topic names to node IDs

    def add_node(self, node):
        serialized_node = serialize_node(node)
        self.cache[node.topic] = serialized_node
        if not self.index:
            self.index = create_index([node])

    def get_chunk(self, topic):
        if topic in self.cache:
            return deserialize_node(self.cache[topic])
        else:
            # Load the node from disk lazily
            node_id = self.index.get(topic)
            if node_id is None:
                raise KeyError(f"Topic '{topic}' not found")
            serialized_node = load_node_from_disk(node_id)
            self.cache[topic] = serialized_node
            return deserialize_node(serialized_node)