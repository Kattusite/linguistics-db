#############################################################################
#       lingdb_client.py
#
#############################################################################

import os, re
from lingdb import LingDB
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS
from data import language_data

# Substitute Database objects
# (can be replaced with an actual DB later if the overhead is justified.
# Construct LING_DB
def init_DB():
    global LING_DB
    LING_DB = LingDB(language_data)
    # print(LING_DB)
    # TODO integrate typology data from TYPOLOGY_FILE

LING_DB = None
init_DB()


def handleQuery(query):
    """Given a query dict, decide which type of query has been made, and return a
    list of results corresponding to the languages matching that type of query"""

    trait = query["trait"]

    function_map = {
        "consonant-selector":           queryForConsonants,
        "consonant-class-selector":     queryForConsonantClasses,
        "vowel-selector":               queryForVowels,
        "vowel-class-selector":         queryforVowelClasses,
        "consonant-places":             queryForConsonantPlaces,
        "consonant-manners":            queryForConsonantManners,
        "complex-consonant":            queryForComplexConsonants,
        "tone-selector":                queryForTone,
        "stress-selector":              queryForStress,
        "syllable-selector":            queryForSyllable
    }

    result = function_map[trait](query)
    return result

def handleQueries(queries):
    """Process multiple queries and direct them as appropriate, according to the
    trait each one represents."""
    # Can be cleaned up with comprehensions
    result_arr = []
    for query in queries:
        result_arr.append(handleQuery(queries))

    if len(result_arr) == 0:
        print("Error: attempted to handle invalid query")
        return None # Query invalid

    prev = result_arr[0]
    for result in result_arr:
        # union the results (one at a time???)
        pass



    return result_arr[0] # placeholder



#############################################################################
#                                Query Methods
#############################################################################
def queryForConsonants(query):
    # init_DB()
    # return consonants + " " + k
    cons = query["consonants"]
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsConsonants(cons, k, mode)
    num = len(matches)
    # glyphs = str(getConsonantGlyphsFromBitstring(cons)).replace("'", "") # debug
    # print(cons, k, mode)
    return num

def queryForConsonantClasses(query):
    classStr = query["class"]
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsConsonantClasses(classStr, k, mode)
    num = len(matches)
    return num

def queryForVowels(query):
    vowels = query["vowels"]
    k = int(query["k"])
    mode = query["mode"]
    return "TBD"

def queryforVowelClasses(query):
    classStr = query["class"]
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsVowelClasses(classStr, k, mode)
    num = len(matches)
    return num

def queryForConsonantPlaces(query):
    matches = LING_DB.queryContainsConsonantPlaces()
    num = len(matches)
    return num

def queryForConsonantManners(query):
    matches = LING_DB.queryContainsConsonantManners()
    num = len(matches)
    return num

def queryForComplexConsonants(query):
    matches = LING_DB.queryContainsComplexConsonants()
    num = len(matches)
    return num

def queryForTone(query):
    matches = LING_DB.queryContainsTone()
    num = len(matches)
    return num

def queryForStress(query):
    matches = LING_DB.queryContainsStress()
    num = len(matches)
    return num

def queryForSyllable(query):
    syllable = query["syllable"]
    matches = LING_DB.queryContainsSyllable(syllable)
    num = len(matches)
    return num

#############################################################################
#                              Combine Query Methods
#############################################################################
# TODO Make these methods members of the LingDB class to make them more sensible
# (and possibly override __and__, __or__, etc)
def intersection(a, b):
    """Given language lists a,b, return a new list c containing the
    intersection of the two lists (x in c exactly once iff x in a AND x in b)"""
    setA = set(a)
    setB = set(b)
    intersection = setA.intersection(setB)
    return list(intersection)

def union(a, b):
    """Given language lists a,b, return a new list c containing the
    union of the two lists (x in a OR x in b iff x in c exactly once)"""
    setA = set(a)
    setB = set(b)
    union = setA.union(setB)
    return list(union)

def implication(a, b):
    """Given language lists a, b, return a new list c containing the elements
    arising from the relationship if a then b (will sort out details later)"""
    # I Don't actually think this differs from intersection--maybe edge cases?
    # Like not in a AND not in B? think about it some more
    return NotImplemented

#############################################################################
#                                Helper Methods
#############################################################################
# Reconstruct the consonant glyphs provided in the given consonant bitstring
def getConsonantGlyphsFromBitstring(consonants):
    # init_DB()
    results = []
    for i, c in enumerate(consonants):
        if c == "1":
            results.append(CONSONANT_GLYPHS[i])
    return results
