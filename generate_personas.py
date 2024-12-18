#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 11:38 2024

@author: magfrump
"""
import json

def generate_personas(num_personas):
    with open("personas.json") as f:
        personas = json.load(f)
    persona_list = personas["personas"]
    print(persona_list)
    if num_personas > len(persona_list):
        print("Too many personas requested, looping.")
        persona_list = persona_list*(num_personas/len(persona_list) + 1)
    return persona_list[:num_personas]