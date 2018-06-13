#############################################################################
#       lingdb.py
#
#############################################################################

import csv, os, re
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS

# File paths
PROJ_ROOT_DIR = ""
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
LANG_DB = None

# Construct LANG_DB
def init_DB():
    global LANG_DB
    LANG_DB = readGrammarData()
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



# Read from grammar data into convenient format
def readGrammarData():

    # Locate the grammar file
    filename = PROJ_ROOT_DIR + GRAMMAR_FILE
    csvfile = open(filename)
    reader = csv.reader(csvfile)

    langDict = {}

    # Read through file line by line
    for i, row in enumerate(reader):
        # Skip header row
        if i == 0:
            continue
        dictEntry = {}

        # For each attribute, get the human readable g_str and associate it
        # with the data from that row of the CSV
        addGIndexToDict(dictEntry, row, LANGUAGE)
        addGIndexToDict(dictEntry, row, NAME)
        addGIndexToDict(dictEntry, row, NETID)
        addGIndexToDict(dictEntry, row, NUM_CONSONANTS)
        addGIndexToDict(dictEntry, row, NUM_VOWELS)
        addGIndexToDict(dictEntry, row, NUM_PHONEMES)
        dictEntry[G_STR[CONSONANTS]] = csvConsonantsToBitstring(row[CONSONANTS])
        dictEntry[G_STR[VOWELS]]     = csvVowelsToBitstring(row[VOWELS])

        # TODO Add phonetic / syllable info

        lang = row[LANGUAGE]
        cons = row[CONSONANTS]
        # print(lang + ": " + csvConsonantsToBitstring(cons))

        # Add this dictionary entry to the temporary database
        # BUG If two students have the same language, it will be overwritten
        # Switch to an array instead of unique-key dict?
        if (dictEntry[G_STR[LANGUAGE]] in langDict):
            print("Error! Language %s was overwritten by a duplicate in the csv"
                  % (dictEntry[G_STR[LANGUAGE]]))
        langDict[dictEntry[G_STR[LANGUAGE]]] = dictEntry;
    return langDict

# Take the gindex'th element of row, and store it as a value in dict d,
# associated with the human-readable grammar heading for that gindex (from G_STR)
def addGIndexToDict(d, row, gindex):
    d[G_STR[gindex]] = row[gindex]

# Given a CSV phoneme string, return a corresponding phoneme bitstring
# That is, a string of 0s and 1s such that a 1 occurs at index i if and only if
# phonemeList[i] is found in csvStr
# phonemeList is a canonical list of the canonical phonemes to be used to create the string
def csvPhonemesToBitstring(csvStr, phonemeList):
    csvStr = csvStr.replace(PHONEME_DELIMITER, "")
    csvList = csvStr.split(INNER_DELIMITER)
    bitList = []

    # Iterate over canonical list and match against csvList
    for phoneme in phonemeList:
        if phoneme in csvList:
            bitList.append("1")
        else:
            bitList.append("0")

    # Construct string from list of matches
    return "".join(bitList)

# Given a csvStr representing a csv formatted list of consonants, return
# the corresponding bitstring of consonants, using CONSONANT_GLYPHS as the
# canonical list
def csvConsonantsToBitstring(csvStr):
    return csvPhonemesToBitstring(csvStr, CONSONANT_GLYPHS)

# Given a csvStr representing a csv formatted list of vowels, return
# the corresponding bitstring of vowels, using VOWEL_GLYPHS as the
# canonical list
def csvVowelsToBitstring(csvStr):
    return csvPhonemesToBitstring(csvStr, VOWEL_GLYPHS)
