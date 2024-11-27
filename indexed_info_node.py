#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 11:44:50 2024

@author: magfrump

This module contains classes and functions for working with node metadata and
child nodes.

Classes:
    ChildNode: Represents a child node, containing a reference and summary.
    NodeMetaData: Represents metadata for a node, including creation and update
        timestamps, source, and type.
    IndexedInfoNode: Represents an indexed information node, containing
        children, metadata, and text.
"""

from dataclasses import dataclass
import json

@dataclass
class ChildNode:
    """
    Represents a child node, containing a reference and summary.

    Attributes:
        node_reference (str): The reference of the child node.
        node_summary (str): The summary of the child node.
    """
    node_reference: str
    node_summary: str

@dataclass
class NodeMetaData:
    """
    Represents metadata for a node, including creation and update timestamps,
        source, and type.
     
    Attributes:
        created (int): The timestamp when the node was created.
        updated (int): The timestamp when the node was last updated.
        source (str): The source of the node.
        node_type (str): The type of the node.
    """
    created: int
    updated: int
    source: str
    node_type: str

class IndexedInfoNode():
    """
    Represents an indexed information node, containing children, metadata, and text.

    Attributes:
        _children: A tuple of child nodes.
        _meta_data: Metadata for the node.
        _text: The text associated with the node.

    Methods:
        __eq__(self, other): Checks if two IndexedInfoNode instances are equal.
        fromfilename(cls, json_file): Creates an IndexedInfoNode instance from
            a JSON file.
        write_to_file(self, filename): Writes the node's data to a JSON file.
        get_type(self): Returns the type of the node.
        get_text(self): Returns the text associated with the node.
        get_children(self): Returns the children of the node.
        retrieve_child(self, index): Retrieves a child node by its index and
            returns an IndexedInfoNode instance.
    """
    def __init__(self, children, meta_data, text):
        """
        Initializes an IndexedInfoNode instance.

        Args:
            children: A tuple of child nodes.
            meta_data: Metadata for the node.
            text: The text associated with the node.
        """
        # Children are a tuple of (node_name, node_summary)
        self._children = children
        self._meta_data = meta_data
        self._text = text

    def __eq__(self, other):
        """
        Checks if two IndexedInfoNode instances are equal.

        Args:
            other: Another IndexedInfoNode instance to compare with.

        Returns:
            bool: True if the instances are equal, False otherwise.
        """
        return (self._children == other._children
                and self._meta_data == other._meta_data
                and self._text == other._text)

    @classmethod
    def fromfilename(cls, json_file):
        """
        Creates an IndexedInfoNode instance from a JSON file.

        Args:
            json_file: The path to the JSON file.

        Returns:
            IndexedInfoNode: An IndexedInfoNode instance created from the JSON
                file.
        """
        with open(json_file, encoding='utf-8') as jf:
            as_json = json.loads(jf.read())
            children = []
            for child in as_json["children"]:
                children.append(ChildNode(node_reference=child["reference"],
                                          node_summary=child["summary"]))
            metadata = NodeMetaData(created=as_json["created"],
                                    updated = as_json["updated"],
                                    source = as_json["source"],
                                    node_type=as_json["type"])
            text = as_json["text"]
        return cls(children, metadata, text)

    def write_to_file(self, filename):
        """
        Writes the node's data to a JSON file.

        Args:
            filename: The path to the output JSON file.
        """
        as_json = {"children": []}
        for child in self._children:
            as_json["children"].append({"reference":child.node_reference,
                                        "summary":child.node_summary})
        as_json["created"] = self._meta_data.created
        as_json["updated"] = self._meta_data.updated
        as_json["source"] = self._meta_data.source
        as_json["type"] = self._meta_data.node_type
        as_json["text"] = self._text
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(as_json, f)

    @property
    def get_type(self):
        """
        Returns the type of the node.

        Returns:
            str: The type of the node.
        """
        return self._meta_data.node_type

    @property
    def get_text(self):
        """
        Returns the text associated with the node.

        Returns:
            str: The text associated with the node.
        """
        return self._text

    def get_children(self):
        """
        Returns the children of the node.

        Returns:
            tuple: A tuple of child nodes.
        """
        return self._children

    def retrieve_child(self, index):
        """
        Retrieves a child node by its index and returns an IndexedInfoNode
            instance.

        Args:
            index: The index of the child node to retrieve.

        Returns:
            IndexedInfoNode: An IndexedInfoNode instance created from the
                retrieved child node.
        """
        return self.fromfilename(self._children[index].node_reference)
