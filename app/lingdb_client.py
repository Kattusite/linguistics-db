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
    reply_arr  = []
    for query in queries:
        r = handleQuery(query)
        s = set(r)
        reply_arr.append(query["reply"])
        result_arr.append(s)

    if len(result_arr) == 0:
        print("Error: attempted to handle invalid query")
        return None # Query invalid

    # Combine the results
    # Use the union (OR)
    uList = [x for x in set.union(*result_arr)]
    uLen  = len(uList)
    uStr  = " OR ".join(reply_arr)

    # Use the intersection (AND)
    iList = [x for x in set.intersection(*result_arr)]
    iLen  = len(iList)
    iStr  = " AND ".join(reply_arr)

    # TODO allow AND, OR, etc. to be selected as a request field, not hardcoded
    langStr = " languages "

    # Merge multiple queries
    if len(reply_arr) > 1:
        # print(len(reply_arr), " queries detected. Merging...")
        return str(uLen) + langStr + uStr + "\n<br>\n" + str(iLen) + langStr + iStr

    # If only one query, just return a single one.
    return str(uLen) + langStr + uStr

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
    return matches

def queryForConsonantClasses(query):
    classStr = query["class"]
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsConsonantClasses(classStr, k, mode)
    return matches

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
    return matches

def queryForConsonantPlaces(query):
    matches = LING_DB.queryContainsConsonantPlaces()
    return matches

def queryForConsonantManners(query):
    matches = LING_DB.queryContainsConsonantManners()
    return matches

def queryForComplexConsonants(query):
    matches = LING_DB.queryContainsComplexConsonants()
    return matches

def queryForTone(query):
    matches = LING_DB.queryContainsTone()
    return matches

def queryForStress(query):
    matches = LING_DB.queryContainsStress()
    return matches

def queryForSyllable(query):
    syllable = query["syllable"]
    matches = LING_DB.queryContainsSyllable(syllable)
    return matches

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
