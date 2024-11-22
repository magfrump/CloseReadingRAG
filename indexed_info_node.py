#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 11:44:50 2024

@author: magfrump
"""

from dataclasses import dataclass
from enum import Enum
import json

@dataclass
class ChildNode:
    node_reference: str
    node_summary: str
    
@dataclass
class NodeMetaData:
    created: int
    updated: int
    source: str
    node_type: str

class IndexedInfoNode():
    def __init__(self, children, meta_data, text):
        # Children are a tuple of (node_name, node_summary)
        self._children = children
        self._meta_data = meta_data
        self._text = text
        
    def __eq__(self, other):
        return (self._children == other._children
                and self._meta_data == other._meta_data
                and self._text == other._text)
        
        
    @classmethod
    def fromfilename(cls, json_file):
        with open(json_file) as jf:
            as_json = json.loads(jf.read())
            children = []
            for child in as_json["children"]:
                children.append(ChildNode(node_reference=child["reference"], node_summary=child["summary"]))
            metadata = NodeMetaData(created=as_json["created"],
                                    updated = as_json["updated"],
                                    source = as_json["source"],
                                    node_type=as_json["type"])
            text = as_json["text"]
        return cls(children, metadata, text)
        
    def write_to_file(self, filename):
        as_json = {"children": []}
        for child in self._children:
            as_json["children"].append({"reference":child.node_reference,
                                        "summary":child.node_summary})
        as_json["created"] = self._meta_data.created
        as_json["updated"] = self._meta_data.updated
        as_json["source"] = self._meta_data.source
        as_json["type"] = self._meta_data.node_type
        as_json["text"] = self._text
        with open(filename, 'w') as f:
            json.dump(as_json, f)
            
    @property
    def get_type(self):
        return self._meta_data.node_type
    
    @property
    def get_text(self):
        return self._text
    
    def get_children(self):
        return self._children
    
    def retrieve_child(self, index):
        return self.from_filename(self._children[index].node_reference)