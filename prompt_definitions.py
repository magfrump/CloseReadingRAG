#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 11:14:58 2024

@author: magfrump
"""

from langchain_core.prompts import PromptTemplate

class PromptCreator:
    """
        An index of retrievable LangChain PromptTemplates.
        
        Methods:
            get_prompt(self, title): Returns the requested PromptTemplate
    """
    def __init__(self):
        retrieval_grader_prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are {persona} assessing relevance of a retrieved document to
            a user question. If the document contains keywords related to the
            user question, grade it as relevant. It does not need to be a
            stringent test. The goal is to filter out erroneous retrievals. \n
            Give a binary score 'yes' or 'no' score to indicate whether the
            document is relevant to the question.\n
            Provide the binary score as a JSON with a single key 'score' and
            no explanation.
            Here is the retrieved document: \n\n {document} \n\n
            Here is the user question: {question} \n
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>

            """,
            input_variables=["persona", "question", "document"],
        )
        updated_retrieval_grader_prompt = PromptTemplate(template="""
            You are {persona}. I'm sharing with you a document and a question that
            someone has asked.
            
            The document is: {document}
            
            The user's question is: {question}
            
            Please review the document in relation to the question and provide
            your thoughts on its relevance. Be concise but thorough in your
            assessment.
            
            Return a response in the format {{'thoughts': '...',
                                              'relevant_text': '...'}} where:
            
            * 'thoughts' contains a brief summary of your analysis, including
            any key points or insights you think are relevant.
            * 'relevant_text' includes any text from the document that you
            believe is particularly relevant to the question. These should be
            direct quotes from the source text.
            
            Be as generous as possible in what you consider relevant, and feel
            free to include any context or background information that might
            be helpful. If none of the document is relevant, 'relevant_text'
            can be empty.
            """,
            input_variables = ["question", "document"],
        )
        rag_generate_prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are {persona}. 
            Use the following pieces of retrieved context to answer the
            question.
            Provide the response as a JSON with two keys: 'thoughts' which
            contains all steps taken to come to a conclusion, then a second
            key 'answer' containing the answer.
            If you don't know the answer, just say that you don't know. 
            Use three sentences maximum and keep the answer concise.
            <|eot_id|><|start_header_id|>user<|end_header_id|>
            Question: {question} 
            Context: {context} 
            Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["persona", "question", "document"],
        )
        hallucination_grader_prompt = PromptTemplate(
            template=""" <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are {persona} assessing whether an answer is grounded in and
            supported by a set of facts. Give a binary 'yes' or 'no' score to
            indicate whether the answer is grounded in / supported by a set of
            facts. Provide the binary score as a JSON with a single key 'score'
            and no preamble or explanation.
            <|eot_id|><|start_header_id|>user<|end_header_id|>
            Here are the facts:
            \n ------- \n
            {documents} 
            \n ------- \n
            Here is the answer: {generation}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["persona", "generation", "documents"],
        )
        answer_grader_prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are a {persona} assessing whether an answer is useful to resolve a
            question. Give a binary score 'yes' or 'no' to indicate whether the
            answer is useful to resolve a question. Provide the binary score as
            a JSON with a single key 'score' and no preamble or explanation.
             <|eot_id|><|start_header_id|>user<|end_header_id|>
             Here is the answer:
            \n ------- \n
            {generation} 
            \n ------- \n
            Here is the question: {question}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["persona", "generation", "question"],
        )
        question_router_prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are {persona}. Use the vectorstore for questions on belegarth. You do
            not need to be stringent with the keywords in the question related
            to these topics. Otherwise, use web-search. Give a binary choice
            'web_search' or 'vectorstore' based on the question. Return the a
            JSON with a single key 'datasource' and no premable or explanation.
            Question to route: {question}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
            input_variables=["question"],
        )
        improve_question_prompt = PromptTemplate(
            template="""
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are {persona}.
            Provide the response as a JSON with two keys: 'thoughts' which
            contains all steps taken to reason about the question, and
            'updated_question' which contains the full text of the original
            question plus any additional text or clarification that will be
            helpful for researching and writing a fully satisfying answer.
            Question to route: {question}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>
            """,
            input_variables=["persona", "question"]
        )
        structure_question_prompt = PromptTemplate(
            template="""
            <|begin_of_text|><|start_header_id|>system<|end_header_id|> 
            Organize the following text by semantic parts of speech and
            relationship. Provide the response as a JSON with the following
            keys and values:
            'nouns': a list of the noun phrases in the question as text
            'verbs': a list of json objects for each verb in the sentence
                formatted as {'verb': the verb, 'subject': the subject of the
                              verb or '',
                              'object': the object of the verb or ''}
                leaving the 'subject' and 'object' fields as empty strings if
                none exist or as '__to_be_answered__' if they are ambiguous or
                unknown.
            include adjectives and adverbs with the nouns and verbs they
                modify.
            Question to route: {question}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>
            """
        )
        text_relevance_prompt = PromptTemplate(
            template="""
            <|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You are {persona}, with perfectly calibrated predictive
            accuracy. Give a probability estimate that following information
            source will contain information that is directly relevant to the
            given query.
            Provide the response as a JSON with a single key, 'relevance' and
            value the probability that the source will be useful, between 0 and
            1.
            Query to find sources for: {question}
            \n ------- \n
            Source: {text}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>
            """,
            input_variables = ["persona", "question", "text"],
        )
        self._available_prompts = {"retrieval_grader": retrieval_grader_prompt,
                    "new_retrieval_grader": updated_retrieval_grader_prompt,
                    "structure_question": structure_question_prompt,
                    "rag_generate": rag_generate_prompt,
                    "hallucination_grader": hallucination_grader_prompt,
                    "answer_grader": answer_grader_prompt,
                    "question_router": question_router_prompt,
                    "improve_question": improve_question_prompt,
                    "text_relevance": text_relevance_prompt,
                    "rate_note": answer_grader_prompt}

    def get_prompt(self, prompt_title):
        """
        Retrieves a formattable LLM prompt for LangChain use from an index.

        Parameters
        ----------
        prompt_title : string
            Title of the prompt to be retrieved.

        Returns
        -------
        PromptTemplate
            The requested LangChain PromptTemplate.

        """
        if prompt_title in self._available_prompts:
            return self._available_prompts[prompt_title]
        print("No prompt found for title: ",prompt_title)
        return prompt_title
