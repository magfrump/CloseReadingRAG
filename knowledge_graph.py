#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 14:06:13 2024

@author: magfrump
"""

from math import ceil
import json
import time
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
import indexed_info_node as iin

def _split_document(document, chunk_length, chunk_overlap):
    chunks = []
    for i in range(0, len(document)-1, chunk_length - chunk_overlap):
        chunk = document[i:i + chunk_length]
        chunks.append(chunk)
    return chunks

def _summarize(document, summary_size, llm):
    summary_prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are an expert at organizing text. You are indexing a section of
        a document to enable researchers to identify the most relevant sections
        of the document to reference for future questions. Do not assume that
        the text is complete, and focus on identifying what is included rather
        than repeating the details of the text. Provide no preamble or
        explanation, only a concise reference text.
        The text to be summarized is:
            {text}
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """,
        input_variables=["text"],)
    prompt = summary_prompt | llm
    summary = prompt.invoke({"text": document})
    return summary.pretty_repr()

class KnowledgeGraph:
    def __init__(self, input_documents, chunk_length, chunk_overlap, \
                 max_subtopics, source = ""):
        self.chunk_length = chunk_length
        self.chunk_overlap = chunk_overlap
        self.max_subtopics = max_subtopics
        self.subtopics = []
        self.text = ""
        self.source = source
        self.llm = ChatOllama(model="Kale", temperature=0, \
                              num_predict = int(self.chunk_length/self.max_subtopics))
        self._process_input_documents(input_documents, chunk_length, \
                                      chunk_overlap, max_subtopics)
        self.add_descriptions()

    @classmethod
    def from_file(cls, input_directory):
        params = {}
        try:
            with open(input_directory+"kg_meta.json") as f:
                params = json.loads(f.read())
        except:
            raise FileNotFoundError("Could not find metadata file for knowledge graph")
        chunk_length = params["chunk_length"]
        chunk_overlap = params["chunk_overlap"]
        max_subtopics = params["max_subtopics"]
        root_node_name = input_directory+"/"+params["root_node"]+"_kg.txt"
        return cls(chunk_length, chunk_overlap, max_subtopics, root_node_name, params["text"])

    def _process_input_documents(self, input_documents, chunk_length, chunk_overlap, max_subtopics):
        if len(input_documents)==1:
            #print("Single document")
            doc = input_documents[0]
            if len(doc) <= chunk_length:
                #print("short text")
                self.text = input_documents[0]
                return
            if len(doc) > (chunk_length-chunk_overlap)*max_subtopics:
                #print("long text ", len(doc))
                chunks = _split_document(doc, chunk_length, chunk_overlap)
                #print("text of length ", len(doc), "split into ", len(chunks), " chunks")
                #print(chunks)
                self.subtopics.append(KnowledgeGraph(chunks,
                                                     chunk_length,
                                                     chunk_overlap,
                                                     max_subtopics))
                return
            #print("medium text ", len(doc))
            chunks = _split_document(doc, chunk_length, chunk_overlap)
            self.subtopics.extend([KnowledgeGraph([_], chunk_length, \
                                                 chunk_overlap, \
                                                 max_subtopics) for _ in chunks])
            return

        if len(input_documents) > max_subtopics:
            #print("many documents ",len(input_documents))
            docs_per_subtopic = ceil(len(input_documents)/max_subtopics)
            #print(docs_per_subtopic)
            for i in range(0, len(input_documents), docs_per_subtopic):
                self.subtopics.append( \
                                KnowledgeGraph( \
                                    input_documents[i:i+docs_per_subtopic], \
                                    chunk_length, chunk_overlap, max_subtopics))
            return

        #print("few documents")
        for doc in input_documents:
            self.subtopics.append(KnowledgeGraph([doc], chunk_length, \
                                                 chunk_overlap, max_subtopics))

    def add_descriptions(self):
        sub_summary_length = int(self.chunk_length/self.max_subtopics)
        if len(self.text) > 0:
            return self.get_text()
        for subtopic in self.subtopics:
            self.text += _summarize(subtopic.add_descriptions(), sub_summary_length, self.llm)
            self.text += "\nAND\n"
        return self.get_text()

    def write_doc_to_dir(self, directory, prefix="", node_type="DOCUMENT"):
        # writes as indexed_info_node
        node = None
        node_children = []
        node_metadata = iin.NodeMetaData(created=time.time(), \
                                         updated=time.time(), \
                                         source=self.source, \
                                         node_type=node_type)

        # If no subtopics, write a single text node
        if self.subtopics:
            for i in range(len(self.subtopics)):
                subtopic = self.subtopics[i]
                node_children.append( iin.ChildNode(
                    node_reference= directory+"/"+prefix+str(i)+"_kg.json", \
                    node_summary= _summarize(subtopic.get_text(), \
                                int(self.chunk_length/self.max_subtopics), self.llm)))
                self.subtopics[i].write_doc_to_dir(directory, \
                                                   prefix=prefix+str(i), \
                                                   node_type="DOCUMENT_SECTION")
            node = iin.IndexedInfoNode(node_children, node_metadata, "")
        else:
            if node_type=="DOCUMENT":
                # a short document with no subtopics
                node_metadata.node_type = "TEXT_DOCUMENT"
            else:
                node_metadata.node_type = "TEXT"
            node = iin.IndexedInfoNode(node_children, node_metadata, self.text)
        if node:
            node.write_to_file(directory+"/"+prefix+"_kg.json")

    @property
    def num_subtopics(self):
        return len(self.subtopics)

    def get_subtopic(self, index):
        if index < 0 or index >= self.num_subtopics:
            raise IndexError("Index out of range")
        return self.subtopics[index]

    def get_text(self):
        return self.text

    def print(self):
        print(self.text)
        for subtopic in self.subtopics:
            print("\n{")
            subtopic.print()
            print("}")
