#############################################################################
#       lingdb.py
#
#############################################################################

import os, re
from lingdb import LingDB
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS

# File paths
PROJ_ROOT_DIR = "" #BUG this changes dependent on which dir app.py is run from
GRAMMAR_FILE  = "data/anon-grammar.csv"
TYPOLOGY_FILE = "data/anon-typology.csv"

# CSV format
ROW_DELIMITER = "\n"   # delimits rows (might need carriage return?)
COL_DELIMITER = ","    # delimits columns within a row
INNER_DELIMITER = ";"  # delimits lists within a column

PHONEME_DELIMITER = "/" # Used on either side of a phoneme (e.g. /d/ --> d)

# CSV indices
# Indices and human-readable strings for each column of the csv
# NOTE Must be updated every time the csv format changes
#GRAMMAR_HEADERS
TIME            = 0
NETID           = 1
NAME            = 2
LANGUAGE        = 3
NUM_CONSONANTS  = 4
NUM_VOWELS      = 5
NUM_PHONEMES    = 6
CONSONANTS      = 7
VOWELS          = 8
PHONETIC        = 9
SYLLABLE        = 10

#GRAMMAR_HEADERS as string
G_STR = [
    "time",             # TIME
    "netid",            # NETID
    "name",             # NAME
    "language",         # LANGUAGE
    "num_consonants",   # NUM_CONSONANTS
    "num_vowels",       # NUM_VOWELS
    "num_phonemes",     # NUM_PHONEMES
    "consonants",       # CONSONANTS
    "vowels",           # VOWELS
    "phonetic",         # PHONETIC
    "syllable"          # SYLLABLE
]



# Substitute Database objects
# (can be replaced with an actual DB later if the overhead is justified.
LING_DB = None

# Construct LING_DB
def init_DB():
    global LING_DB
    LING_DB = LingDB(GRAMMAR_FILE, TYPOLOGY_FILE)
    # print(LANG_DB)
    # TODO integrate typology data from TYPOLOGY_FILE

def dummy(request):
    return "SOMETHING HAPPENED!"

# Reconstruct the consonant glyphs provided in the given consonant bitstring
def checkConsonants(consonants):
    init_DB()
    results = []
    for i, c in enumerate(consonants):
        if c == "1":
            results.append(CONSONANT_GLYPHS[i])
    return results
