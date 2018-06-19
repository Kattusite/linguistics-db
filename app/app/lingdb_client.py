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
    result_arr = []
    for query in queries:
        result_arr.append(handleQuery(queries))

    for result in result_arr:
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
#                              List Query Methods
#############################################################################


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
