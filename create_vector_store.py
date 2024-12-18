#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:26:13 2024

@author: magfrump
"""
import time
from langchain_community.document_loaders import WebBaseLoader
import knowledge_graph as kg

# def create_vector_store():
#     urls = [
#         # "https://www.magfrump.net",
#         "https://www.belegarth.com/rules",
#         # "https://en.wikipedia.org/wiki/List_of_common_misconceptions",
#         # "https://www.library.illinois.edu/infosci/research/guides/dewey/",
#     ]
#     docs = [WebBaseLoader(url).load() for url in urls]
#     docs_list = [item for sublist in docs for item in sublist]
#     text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=2000, chunk_overlap=100
#     )
#     doc_splits = text_splitter.split_documents(docs_list)
#     print(len(doc_splits))
#     for d in doc_splits:
#         print(d.page_content[:20], "\n\n")
#     # Add to vectorDB
#     vectorstore = Chroma.from_documents(
#         documents=doc_splits,
#         collection_name="general-chroma",
#         embedding=NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local"),
#     )
#     return vectorstore.as_retriever()

urls = [
    # "https://www.magfrump.net",
     "https://www.belegarth.com/rules",
    # "https://en.wikipedia.org/wiki/List_of_common_misconceptions",
    # "https://www.library.illinois.edu/infosci/research/guides/dewey/",
]
t0 = time.time()
docs = [WebBaseLoader(url).load() for url in urls]
print("Loaded web page at time: ", time.time()-t0)
docs_list = [item for sublist in docs for item in sublist]

parsed_docs = [kg.KnowledgeGraph([docs_list[i].page_content],
                                 800, 20, 10, urls[i])
               for i in range(len(docs_list))]
print("\n\nParsed docs at time: ", time.time()-t0)

for pardoc in parsed_docs:
    pardoc.write_doc_to_dir("data", "belegarth")
print("\n\nWrote parsed doc to disk at time: ",time.time()-t0)
# text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#     chunk_size=4000, chunk_overlap=100
# )
# doc_splits = text_splitter.split_documents(docs_list)
# embedder = NomicEmbeddings(model="nomic-embed-text-v1.5", inference_mode="local")
# embeddings = embedder.embed_documents([_.page_content for _ in doc_splits])

# for i in range(len(doc_splits)):
#     print("CONTENT-------------")
#     print(doc_splits[i].page_content[:20])
#     print("EMBEDDING-----------")
#     print(np.round(embeddings[i],2))
