#############################################################################
#       lingdb_client.py
#
#############################################################################

import os, re
from lingdb import LingDB
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS

# Substitute Database objects
# (can be replaced with an actual DB later if the overhead is justified.
# Construct LING_DB
def init_DB():
    global LING_DB
    LING_DB = LingDB(GRAMMAR_FILE, TYPOLOGY_FILE)
    # print(LANG_DB)
    # TODO integrate typology data from TYPOLOGY_FILE

LING_DB = None
init_DB()


def handleQuery(form):
    """Given a form f, decide which type of query has been made, and return a
    list of results corresponding to the languages matching that type of query"""

    # placeholder
    return queryForConsonants(form["consonants"], form["k"], form["mode"])


def queryForConsonants(cons, k, mode):
    # init_DB()
    # return consonants + " " + k
    k = int(k)
    matches = LING_DB.queryContainsConsonants(cons, k, mode)
    num = len(matches)
    glyphs = str(getConsonantGlyphsFromBitstring(cons)).replace("'", "")
    print(cons, k, mode)
    return num;

# Reconstruct the consonant glyphs provided in the given consonant bitstring
def getConsonantGlyphsFromBitstring(consonants):
    # init_DB()
    results = []
    for i, c in enumerate(consonants):
        if c == "1":
            results.append(CONSONANT_GLYPHS[i])
    return results
