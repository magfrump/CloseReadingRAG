#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 13:46:47 2024

@author: magfrump
"""

import os
import time

from langchain_community.chat_models import ChatOllama
from langgraph.graph import END, StateGraph, START
from langchain_core.runnables.config import RunnableConfig

import node_definitions as nodedef

if __name__ == '__main__':
    t0 = time.time()
    # set global variables. USER_AGENT identifies the process to html requests.
    os.environ["USER_AGENT"] = "FnordFiddler"
    # local llm sets the local llm profile to call using ollama
    local_llm = "Kale"
    llm = ChatOllama(model=local_llm, format="json", temperature = 0)
    print("Established llm at time ",time.time()-t0)

    nodes = nodedef.RagNodes("data/belegarth_kg.json", llm)

    ## Add nodes to workflow
    workflow = StateGraph(nodedef.GraphState)

    # Define the nodes
    # workflow.add_node("websearch", nodes.web_search)  # web search
    workflow.add_node("retrieve", nodes.retrieve)  # retrieve
    workflow.add_node("grade_documents", nodes.grade_documents)  # grade documents
    workflow.add_node("generate", nodes.generate)  # generate
    # workflow.add_node("improve_question", nodes.improve_question)
    print("Created graph nodes at time ",time.time()-t0)

    # Add graph edges
    #workflow.add_edge(START, "improve_question")

    #workflow.add_conditional_edges(
    #    START,
    #    nodes.route_question,
    #    {
    #        "websearch": "websearch",
    #        "vectorstore": "retrieve",
    #    },
    #)

    workflow.add_edge(START, "retrieve")

    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_edge("grade_documents", "generate")
    #workflow.add_conditional_edges(
    #    "grade_documents",
    #    nodes.decide_to_generate,
    #    {
    #        "websearch": "websearch",
    #        "generate": "generate",
    #    },
    #)
    # workflow.add_edge("websearch", "generate")
    workflow.add_edge("generate", END)
    #workflow.add_conditional_edges(
    #    "generate",
    #    nodes.grade_generation_v_documents_and_question,
    #    {
    #        "not supported": "generate",
    #        "useful": END,
    #        "not useful": END #"websearch",
    #    },
    #)
    app = workflow.compile()
    print("Created graph edges at time ",time.time()-t0)
    inputs = {"question": """
              In Belegarth, where is the boundary between the body and arm
              target areas?
              """
              }
    config = RunnableConfig(recursion_limit=5)
    for output in app.stream(inputs, config):
        for key, value in output.items():
            print(f"Finished running: {key}:")
            # print(f"With result: {value}:")
    print(value["generation"])

#if __name__ == '__main__':
    # set global variables. USER_AGENT identifies the process to html requests.
    # os.environ["USER_AGENT"] = "FnordFiddler"
    # local llm sets the local llm profile to call using ollama
    # local_llm = "Kale"
    # llm = ChatOllama(model=local_llm, format="json", temperature = 0)

    # nodes = nodedef.RagNodes("data/belegarth_kg.json", llm)

    ## Add nodes to workflow
    # workflow = StateGraph(nodedef.GraphState)
    # class GraphState(TypedDict):
    #   original_claim: str
    #   responses: List[Response]
    #   persona_index: int
    #   winning_note: str
    #   new_sources: List[str]

    # class Response(TypedDict):
    #   response_content: str
    #   response_sources: List[str]
    #   response_ratings: List[float]

    # Define the nodes
    # workflow.add_node("retrieve", nodes.retrieve)  # retrieve
    # workflow.add_node("grade_documents", nodes.grade_documents)  # grade documents
    # workflow.add_node("generate", nodes.generate)  # generate
    # workflow.add_node("next_note", nodes.next_note)
    # workflow.add_node("increment_persona_or_move_on", nodes.increment_or_move_on)
    # NOT IMPLEMENTED:
    # workflow.add_node("websearch", nodes.web_search)  # web search
    # workflow.add_node("index_info", nodes.index_info)
    # workflow.add_node("rate_notes", nodes.rate_notes)
    # workflow.add_node("pick_winning_note", nodes.pick_winner)

    # Add graph edges

    # workflow.add_edge(START, "retrieve")
    # workflow.add_edge("retrieve", "grade_documents")
    # workflow.add_conditional_edges(
    #   "grade_documents",
    #   nodes.decide_to_generate,
    #   {
    #       "websearch": "websearch",
    #       "generate": "generate"
    #   },
    # )
    # workflow.add_edge("websearch", "index_info")
    # workflow.add_edge("index_info", "retrieve")
    # workflow.add_conditional_edges(
    #    "generate",
    #    nodes.grade_generation_v_documents_and_question,
    #    {
    #        "not supported": "generate",
    #        "useful": "next_note",
    #        "not useful": "websearch",
    #    },
    #)
    # workflow.add_conditional_edges(
    #   "next_note",
    #   "increment_persona_or_move_on",
    #   { "increment_persona": "retrieve", "move_on": "rate_notes" }
    # )
    # workflow.add_conditional_edges(
    #    "rate_notes",
    #    "increment_persona_or_move_on",
    #    {
    #        "increment_persona": "rate_notes",
    #        "move_on": "pick_winning_note",
    #    },
    #)
    # workflow.add_edge("pick_winning_note", END)

    #app = workflow.compile()
    #inputs = {"original_claim": """
    #          In Belegarth, where is the boundary between the body and arm
    #          target areas?
    #          """
    #          }
    #config = RunnableConfig(recursion_limit=5)
    #for output in app.stream(inputs, config):
    #    for key, value in output.items():
    #        print(f"Finished running: {key}:")
    #        # print(f"With result: {value}:")
    #print(value["winning_note"])
