#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:28:15 2024

@author: magfrump
"""
import json

class LookupIndex:
    """
    Represents a lookup index with subtopics.

    Attributes:
        index_description (str): A brief description of the index.
        docs (list): A list of documents associated with the index.
        subtopics (list): A list of subtopics, each represented by an instance
            of LookupIndex.
        specificity (int): The specificity level of the index.

    Methods:
        add_subtopic(subtopic: 'LookupIndex') -> None: Adds a subtopic to the
            index if it has higher specificity than the current index.
    """
    def __init__(self, index_description: str, docs: list, specificity: int):
        self.index_description = index_description
        self.docs = docs
        self.subtopics = []
        self.specificity = specificity

    def add_subtopic(self, subtopic: 'LookupIndex') -> None:
        if subtopic.specificity > self.specificity:
            self.subtopics.append(subtopic)

def read_index_from_file(filename: str) -> LookupIndex:
    """
    Reads a lookup index from a JSON file.
    
    Args:
        filename (str): The path to the JSON file containing the index data.
    
    Returns:
        LookupIndex: An instance of LookupIndex representing the loaded index.
    """
    with open(filename, 'r') as f:
        data = json.load(f)
        index = LookupIndex(data['index_description'], data['docs'])
        for subtopic in data['subtopics']:
            subtopic_instance = LookupIndex(subtopic['description'],
                                            subtopic['docs'],
                                            specificity=subtopic['specificity'])
            index.add_subtopic(subtopic_instance, subtopic['specificity'])
        return index

def write_index_to_file(index: LookupIndex, filename: str) -> None:
    """
    Writes a lookup index to a JSON file.

    Args:
        index (LookupIndex): The index to be written.
        filename (str): The path to the output JSON file.
    """
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
    """
    Represents a node in the library's index.

    Attributes:
        topic (str): The topic name associated with this node.
        children (dict): A dictionary of child nodes, keyed by their topic names.
        id (int): The unique ID assigned to this node when serialized.
    """
    def __init__(self, topic, children=None):
        self.topic = topic
        self.children = children if children else {}
        self.id = None  # assigned when serialized

def serialize_node(node):
    """
   Serializes a Node instance to a binary format.

   Args:
       node (Node): The node to be serialized.

   Returns:
       bytes: The serialized representation of the node.
   """
    return node.topic.encode('utf-8') + b'\x00' + serialize_children(node.children)

def deserialize_node(data):
    """
    Deserializes a Node instance from a binary format.

    Args:
        data (bytes): The binary data containing the node's topic and children.

    Returns:
        Node: An instance of Node representing the deserialized node.
    """
    topic, children_data = data.split(b'\x00', 1)
    return Node(topic.decode('utf-8'), deserialize_children(children_data))

def create_index(nodes):
    """
    Creates an index mapping topic names to node IDs.
    
    Args:
        nodes (list): A list of Node instances to be indexed.
    
    Returns:
        dict: An index dictionary mapping topic names to node IDs.
    """
    index = {}
    for node in nodes:
        index[node.topic] = node.id
    return index


class Library:
    """
    Represents a library containing nodes and an index.

    Attributes:
        cache (dict): A cache of frequently accessed nodes, keyed by their topic names.
        index (dict): An index mapping topic names to node IDs.
    """
    def __init__(self):
        self.cache = {}  # cache for frequently accessed nodes
        self.index = None  # index mapping topic names to node IDs

    def add_node(self, node):
        """
        Adds a node to the library's index and cache.

        Args:
            node (Node): The node to be added.
        """
        serialized_node = serialize_node(node)
        self.cache[node.topic] = serialized_node
        if not self.index:
            self.index = create_index([node])

    def get_chunk(self, topic):
        """
        Retrieves a chunk of data associated with the given topic.

        Args:
            topic (str): The topic name to retrieve data for.

        Returns:
            Node: An instance of Node representing the retrieved node.
        """
        if topic in self.cache:
            return deserialize_node(self.cache[topic])
        # Load the node from disk lazily
        node_id = self.index.get(topic)
        if node_id is None:
            raise KeyError(f"Topic '{topic}' not found")
        serialized_node = load_node_from_disk(node_id)
        self.cache[topic] = serialized_node
        return deserialize_node(serialized_node)
