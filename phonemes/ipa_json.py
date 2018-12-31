"""A collection of tools to help consonants.py and vowels.py read in their input
data from .json files"""

import json

def readIPAFromJson(filename):
    """Read in IPA data from the specified json file, and return it as an array
    of dictionaries containing the properties of each phoneme"""
    file = open(filename, "r", encoding="utf-8")
    data = json.load(file)
    return data
