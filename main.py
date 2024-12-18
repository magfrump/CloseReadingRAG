#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 13:46:47 2024

@author: magfrump
"""

import os

from langchain_community.chat_models import ChatOllama
from langgraph.graph import END, StateGraph, START
from langchain_core.runnables.config import RunnableConfig

import node_definitions as nodedef

if __name__ == '__main__':
    # set global variables. USER_AGENT identifies the process to html requests.
    os.environ["USER_AGENT"] = "FnordFiddler"
    # local llm sets the local llm profile to call using ollama
    local_llm = "Kale"
    llm = ChatOllama(model=local_llm, format="json", temperature = 0)

    nodes = nodedef.RagNodes("data/belegarth_kg.json", llm)

    ## Add nodes to workflow
    workflow = StateGraph(nodedef.GraphState)
    # Define the nodes
    workflow.add_node("retrieve", nodes.retrieve)  # retrieve
    workflow.add_node("grade_documents", nodes.grade_documents)  # grade documents
    workflow.add_node("generate", nodes.generate)  # generate
    workflow.add_node("next_note", nodes.next_note)
    # NOT IMPLEMENTED:
    workflow.add_node("websearch", nodes.web_search)  # web search
    workflow.add_node("index_info", nodes.index_info)
    workflow.add_node("rate_notes", nodes.rate_notes)
    workflow.add_node("pick_winning_note", nodes.pick_winner)

    # Add graph edges

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
      "grade_documents",
      nodes.decide_to_generate,
       {
          "websearch": "websearch",
           "generate": "generate"
       },
    )
    workflow.add_edge("websearch", "index_info")
    workflow.add_edge("index_info", "retrieve")
    workflow.add_conditional_edges(
        "generate",
        nodes.grade_generation_v_documents_and_question,
        {
            "not supported": "generate",
            "useful": "next_note",
            "not useful": "websearch",
        },
    )
    workflow.add_conditional_edges(
        "next_note",
        nodes.increment_persona_or_move_on,
        { "increment_persona": "retrieve", "move_on": "rate_notes" }
     )
    workflow.add_conditional_edges(
        "rate_notes",
        nodes.increment_persona_or_move_on,
        {
            "increment_persona": "rate_notes",
            "move_on": "pick_winning_note",
        },
    )
    workflow.add_edge("pick_winning_note", END)

    app = workflow.compile()
    inputs = {"original_claim": """
              In Belegarth, where is the boundary between the body and arm
              target areas?
              """
              }
    config = RunnableConfig(recursion_limit=20)
    for output in app.stream(inputs, config):
        for key, value in output.items():
            print(f"Finished running: {key}:")
            print(f"With result: {value}:")
    print(value["winning_note"])
