#############################################################################
#       lingdb_client.py
#
#############################################################################

import os, re
from lingdb import LingDB
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS
from data import language_data
import phonemes

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
    # TODO Clean this whole section up (add HTML styling + a separate formatter function)
    # langStr = " languages "

    nlStr   = "\n<br>\n"

    uRep = createUnionReply(result_arr, reply_arr, LING_DB)
    iRep = createIntersectionReply(result_arr, reply_arr, LING_DB)
    cRep = createConditionalReply(result_arr, reply_arr, LING_DB)

    # TODO allow AND, OR, etc. to be selected as a request field, not hardcoded
    # TODO also allow for displaying the results of each subquery alone--
    # If I query for A & B & C, also display just A, just B, just C.

    # Merge multiple queries
    if len(reply_arr) > 1:
        # print(len(reply_arr), " queries detected. Merging...")
        return nlStr.join([uRep, iRep, cRep])

    # If only one query, just return a single one.
    return uRep

#############################################################################
#                          Formatted Reply Methods
#############################################################################

def mergeReplies(replies, joinWord):
    """Join together the strings in replies, using joinWord as a semantic separator
    (e.g. "and", "or")"""
    # TODO implement this for more modularity in the createReply functions
    return NotImplemented

def createUnionReply(results, replies, db):
    """Return a string of HTML representing the formatted results to be
    displayed for the given results list and replies list, and containing db,
    assuming the queries are joined together using union (OR)"""
    matches = [x.getLanguage() for x in set.union(*results)]
    num = len(matches)
    den = len(db)
    reply = "".join(["<b>", "</b> or <b>".join(replies), "</b>"])
    frac  = createFractionHTML(num, den)
    return " ".join([frac, reply])

def createIntersectionReply(results, replies, db):
    """Return a string of HTML representing the formatted results to be
    displayed for the given results list and replies list, and containing db,
    assuming the queries are joined together using intersection (AND)"""
    matches = [x.getLanguage() for x in set.intersection(*results)]
    num = len(matches)
    den = len(db)
    reply = "".join(["<b>", "</b> and <b>".join(replies), "</b>"])
    frac  = createFractionHTML(num, den)
    return " ".join([frac, reply])

def createConditionalReply(results, replies, db):
    """Return a string of HTML representing the formatted results to be
    displayed for the given results list and replies list, and containing db,
    assuming the queries are joined together using conditional (R[0] implies R[1,2,3,...])"""
    matches = [x.getLanguage() for x in set.intersection(*results)]
    num = len(matches)
    den = len(results[0])
    ifReply   = "".join([" that <b>", replies[0], "</b> also "])
    thenReply = "".join(["<b>", "</b> and <b>".join(replies[1:]), "</b>"])
    frac  = createFractionHTML(num, den)
    return " ".join([frac, ifReply, thenReply])


def createFractionHTML(num, den):
    float = 0
    if (den != 0):
        float = num / den
    quantifier = floatToQuantifier(float)
    frac = "".join(["<span style='font-size: x-small;'>",
                    "(%d / %d)" % (num, den),
                    "</span>"])
    text = "".join([quantifier, " languages ", frac])
    ret  = "".join(["<span ",
                    "data-toggle='tooltip' ",
                    "title='%d%% of languages matched'" % round(float * 100),
                    ">",
                    text,
                    "</span>"])
    return ret


def floatToQuantifier(float):
    # TODO Cut down on the number of quantifiers -- they are oversaturated and lose some meaning
    """Given a floating point number float in the range 0 to 1, return a quantifier
    string like "all", "nearly all", "few", "no" to represent it"""
    if float < 0 or float > 1:
        raise ValueError("Error: Float %f is not in the range [0,1]!" % float)
    elif float == 0:
        return "No"
    elif float < 0.10:
        return "Hardly any"
    elif float < 0.20:
        return "Few"
    elif float < 0.30:
        return "Not many"
    elif float < 0.40:
        return "Some"
    elif float < 0.55:
        return "A lot of"
    elif float < 0.65:
        return "Many"
    elif float < 0.85:
        return "Most"
    elif float < 1:
        return "Nearly all"
    else:
        return "All"

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
    classArr = query["classes"]
    bitstring = phonemes.consonants.getBitstringFromClasses(classArr)
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsConsonants(bitstring, k, mode)
    return matches

def queryForVowels(query):
    vowels = query["vowels"]
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsVowels(vowels, k, mode)
    return matches

def queryforVowelClasses(query):
    classArr = query["classes"]
    bitstring = phonemes.vowels.getBitstringFromClasses(classArr)
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsVowels(bitstring, k, mode)
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
