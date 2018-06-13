#############################################################################
#       lingdb.py
#
#############################################################################

import csv, os, re

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

# should be declared externally and included (also used in pbox-gen.py)
CONSONANT_GLYPHS = [
  "n",
  "t",
  "m",
  "k",
  "j",
  "s",
  "p",
  "l",
  "w",
  "h",
  "b",
  "d",
  "g",
  "ŋ",
  "ʃ",
  "ʔ",
  "tʃ",
  "f",
  "r",
  "ɲ",
  "z",
  "ts",
  "dʒ",
  "x",
  "v"
]

def dummy(request):
    return "SOMETHING HAPPENED!"

# Reconstruct the consonant glyphs provided in the given consonant bitstring
def checkConsonants(consonants):
    readGrammarData()
    results = []
    for i, c in enumerate(consonants):
        if c == "1":
            results.append(CONSONANT_GLYPHS[i])
    return results



# Read from grammar data into convenient format
def readGrammarData():
    # Change directory to project root.
    # os.chdir(PROJ_ROOT_DIR)
    print(os.getcwd())

    # Locate the grammar file
    filename = PROJ_ROOT_DIR + GRAMMAR_FILE
    csvfile = open(filename)
    reader = csv.reader(csvfile)

    # Read through file line by line
    for i, row in enumerate(reader):
        # Skip header row
        if i == 0:
            continue
        lang = row[LANGUAGE]
        cons = row[CONSONANTS]
        print(lang + ": " + csvConsonantsToBitstring(cons))

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
