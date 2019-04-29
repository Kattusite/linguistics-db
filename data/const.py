# No imports (leaf node in any import tree)

"""This file defines constants used throughout the program, primarily relating to
handling different datasets and parsing datasets from the raw Google Forms CSV data.

This file (and with any luck only this file) will need to be updated any
time significant changes are made to the survey questions or format.
"""

#############################################################################
#                           Return Status Codes
#############################################################################
RET_CODE = "code"   # The key for return codes
PAYLOAD = "payload" # The key for the payload

# What sort of message sort be displayed to the user?
SUCCESS = "success"        # Green message
INFO = "info"              # Blue message
WARN = "warning"              # Yellow message
DANGER = "danger"          # Red message



##############################################################################
#                            Dataset constants                               #
##############################################################################
# Where is a dataset named {0} located, relative to the project root?
DATASET_PATH = "data/datasets/{0}/{1}"

# Dataset Constants
TEST = "_test"
F17 = "F17"
S19 = "S19"
S19TEST = "S19test"


# Which named datasets do we have?
# F = Fall, S = spring, XX = year 20XX
datasetNames = [
    TEST,
    S19TEST,
    F17,
    S19
]



##############################################################################
#                          csvtojson constants                               #
##############################################################################

# Remove the Q_ prefixes once old vars are removed

# Valid types:
# Text:             Read in the field as text, as-is, without additional processing
# Mult. Choice :    Read in the field and split it by INNER_DELIMITER
# Single Choice:    Compare against a list of known choices
# Booleans:         Several binary (yes/no) traits in a single multiple choice question

# Edit: scrap those and make "string", "list", "num", "bool"

# mapping: whether there are several lists contributing to the same data point
# one to one = one question on survey, one key in JSON
# split = one question on survey, many keys in JSON;
# merge = many questions on survey, one key in JSON;

# or alternatively:


# Which surveys are available?
GRAMMAR = "grammar"    # From the "Grammar Work 2" survey
TYPOLOGY = "typology"  # From the final "Typology" survey


# Parameter names
KEY = "key"
TYPE = "type"
INDEX = "index"
MAPPING = "mapping"
DICT = "dict"
FAIL_DICT = "fail dict"
# SELECTOR / PARSE_DICT / SOMETHING LIKE THAT

PHONEMES = "phonemes"

# Possible types
STRING = "string"                   # Value will be a string
BOOL = "bool"                       # Value will be a bool
NUM = "num"                         # Value will be a number (so far must be int)
LIST = "list"                       # Value will be a list
PLACEHOLDER = "placeholder"         # Value will be set by someone else (derived fields like # manners)
# HASH = "hash" # tbd.. maybe can use?

# Possible mappings
ONE_TO_ONE = "one to one"
SPLIT = "split"
MERGE = "merge"

######################################################
#   JSON Keys
######################################################
# These variables shall all be prefixed with K_ to indicate they are *K*eys

# Possible keys for JSON entry for each language

K_NETID                 = "netid"
K_NAME                  = "name"
K_LANGUAGE              = "language"
K_NUM_VOWELS            = "num vowels"
K_NUM_CONSONANTS        = "num consonants"
K_NUM_PHONEMES          = "num phonemes"
K_CONSONANTS            = "consonants"
K_VOWELS                = "vowels"
K_NUM_CONSONANT_PLACES  = "num consonant places" # note diff than orig
K_NUM_CONSONANT_MANNERS = "num consonant manners"
K_VOWEL_TYPES           = "vowel types"
K_3_PLUS_PLACES         = "3+ places"   # deprecated
K_2_PLUS_MANNERS        = "2+ manners"  # deprecated
K_COMPLEX_CONSONANTS    = "complex consonants"
K_TONE                  = "tone"
K_STRESS                = "stress"
K_SYLLABLES             = "syllables"

K_CITATION              = "citation"
K_RECOMMEND             = "recommend"
K_MORPHOLOGICAL_TYPE    = "morphological type"
K_WORD_FORMATION        = "word formation"
K_WORD_FORMATION_FREQ   = "word formation frequency"
K_WORD_ORDER            = "word order"
K_HEADEDNESS            = "headedness"
K_CASE                  = "case"
K_AGREEMENT             = "agreement"

# List of all possible legal keys for a language object.
# Used for validation in language.py
VALID_KEYS = set([
    K_NETID,
    K_NAME,
    K_LANGUAGE,
    K_NUM_VOWELS,
    K_NUM_CONSONANTS,
    K_NUM_PHONEMES,
    K_CONSONANTS,
    K_VOWELS,
    K_NUM_CONSONANT_PLACES,
    K_NUM_CONSONANT_MANNERS,
    K_VOWEL_TYPES,
    K_3_PLUS_PLACES,
    K_2_PLUS_MANNERS,
    K_COMPLEX_CONSONANTS,
    K_TONE,
    K_STRESS,
    K_SYLLABLES,

    K_CITATION,
    K_RECOMMEND,
    K_MORPHOLOGICAL_TYPE,
    K_WORD_FORMATION,
    K_WORD_FORMATION_FREQ,
    K_WORD_ORDER,
    K_HEADEDNESS,
    K_CASE,
    K_AGREEMENT,
])


##################################################
#   PARSEDICT DEFINITIONS
##################################################
# This is where parseDicts (to be used in csvtojson.py) will be defined
# For other types of parsedicts, that are possible referring to derived types
# or data that is *only* relevant for autogen.py and specifying selectors
# for the frontend, they will be defined directly in selectors.py
# To reiterate, these parseDicts are ONLY the ones that will actually need
# to be passed to the parsePhrase() function at some point in csvtojson.py

# These variables shall all be prefixed with D_ to signify they are parse*D*icts

# Grammar parseDicts
D_VOWEL_TYPES = {
    "nasalized":        [],
    "long":             [],
    "voiceless":        [],
    "breathy":          [],
    "creaky":           [],
    "pharyngealized":   [],
    "diphthongs":       [],
    "triphthongs":      []
}

D_SYLLABLES = {
    "V":            ["V", "onsetless and codaless"],
    "C onset":      ["CV", "single onset"],
    "CC onset":     ["CCV", "two onset"],
    "CCC onset":    ["CCCV", "three onset"],
    "CCCC onset":   ["CCCCV", "four onset"],
    "C coda":       ["CVC", "VC", "single coda"], # formerly CVC, not "VC"
    "CC coda":      ["VCC", "two coda"],
    "CCC coda":     ["VCCC", "three coda"],
    "CCCC coda":    ["VCCCC", "four coda"]
}

# Typology parseDicts
D_MORPHOLOGY = {
    "isolating": [],
    "analytic": ["analytic", "not isolating"], # this is a toughie
    "fusional": [],
    "agglutinating": [],
    "polysynthetic": []
}

D_WORD_FORMATION_F17 = {
    "affixation": ["affixation", "prefixation or suffixation"],
    "suffixation": [],
    "prefixation": [],
    "infixation": [],
    "compounding": [],
    "root-and-pattern": [],
    "internal change": [],
    "suppletion": [],
    "stress or tone shift": [],
    "reduplication": [],
    "conversion": [],
    "purely isolating": ["none", "purely isolating"]
}

D_WORD_FORMATION_S19 = {
    # "affixation": ["affixation", "prefixation or suffixation"], # obsolete as of s19
    "suffixation": [],
    "prefixation": [],
    "infixation": [],
    "compounding": [],
    "root-and-pattern": [],
    "internal change": [],
    "suppletion": [],
    "stress or tone shift": [],
    "reduplication": [],
    "conversion": [],
    "purely isolating": ["none", "purely isolating"]
}

# not thoroughly tested
D_WORD_FORMATION_FREQ = {
    "exclusively suffixing": [],
    "mostly suffixing": [],
    "exclusively prefixing": [],
    "mostly prefixing": [],
    "equal prefixing and suffixing": ["prefixing and suffixing"],
    "exclusively non-affixal": [],
    "mostly non-affixal": [],
    "equal affixation and other": ["affixation and other"],
    "mostly isolating": [],
    "exclusively isolating": ["exclusively isolating", "purely isolating"]
}

D_WORD_ORDER = {
    "SVO": [],
    "SOV": [],
    "VSO": [],
    "VOS": [],
    "OVS": [],
    "OSV": [],
    # "multiple": ["more than one", "multiple", "several"],
    "free":     ["no basic", "none", "free"]
}

# not thoroughly tested
D_HEADEDNESS = {
    "consistently head-initial": [],
    "consistently head-final": [],
    "mostly head-initial": [],
    "mostly head-final": [],
    "mixed headedness": []
}

D_CASE = {
    "none": ["doesn't have", "none"],
    "ergative/absolutive": [],
    "nominative/accusative": [],
    "other": ["other", "some other", "other sort"]
}

D_AGREEMENT = {
    "none": ["doesn't have", "none"],
    "ergative/absolutive": [],
    "nominative/accusative": [],
    "other": ["other", "some other", "other sort"]
}

##################################################
# PARAMETER SPECIFICATIONS
##################################################
# These are the specifications for parameters that need to be read in and
# converted in csvtojson.py.

# TODO: INDEX isn't actually super useful -- instead pull index from each
# parameter's index in the PARAMS list, because they may change from year to
# year and this should not break the data.

# These variables shall all be prefixed with a P_ to signify they are
# *P*arameter specifications

# Common question specifications that won't change much
P_NETID = {
    KEY:        K_NETID,
    TYPE:       STRING, # HASH?
    INDEX:      1,
    MAPPING:    ONE_TO_ONE
}

P_NAME = {
    KEY:        K_NAME,
    TYPE:       STRING, # HASH?
    INDEX:      2,
    MAPPING:    ONE_TO_ONE
}

P_LANGUAGE = {
    KEY:        K_LANGUAGE,
    TYPE:       STRING,
    INDEX:      3,
    MAPPING:    ONE_TO_ONE
}

P_NUM_CONSONANTS = {
    KEY:        K_NUM_CONSONANTS,
    TYPE:       NUM,
    INDEX:      4,
    MAPPING:    ONE_TO_ONE
}

P_NUM_VOWELS = {
    KEY:        K_NUM_VOWELS,
    TYPE:       NUM,
    INDEX:      5,
    MAPPING:    ONE_TO_ONE
}

P_NUM_PHONEMES = {
    KEY:        K_NUM_PHONEMES,
    TYPE:       NUM,
    INDEX:      6,
    MAPPING:    ONE_TO_ONE
}

P_NUM_CONSONANT_PLACES = {
    KEY:        K_NUM_CONSONANT_PLACES,
    TYPE:       PLACEHOLDER,
}

P_NUM_CONSONANT_MANNERS = {
    KEY:        K_NUM_CONSONANT_MANNERS,
    TYPE:       PLACEHOLDER,
}

# Things that will more likely change
# Fall 17 specific data format specification
P_CONSONANTS_F17 = {
    KEY:        K_CONSONANTS,
    TYPE:       LIST,
    INDEX:      7,
    MAPPING:    ONE_TO_ONE,
    DICT:       PHONEMES
}

P_VOWELS_F17 = {
    KEY:        K_VOWELS,
    TYPE:       LIST,
    INDEX:      8,
    MAPPING:    ONE_TO_ONE,
    DICT:       PHONEMES
}

P_PHONETIC_F17 = {
    KEY:        [K_COMPLEX_CONSONANTS, K_TONE, K_STRESS], # omit 3+ Place, 2+ manner
    TYPE:       BOOL,
    INDEX:      9,
    MAPPING:    SPLIT,
}

P_SYLLABLE_F17 = {
    KEY:        K_SYLLABLES,
    TYPE:       LIST,
    INDEX:      10,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_SYLLABLES,
    FAIL_DICT:  ["CV", "V", "VC"]  # Should not be hardcoded, move to selectors?
}


# Spring 19 specific format specification
P_CONSONANTS_S19 = {
    KEY:        K_CONSONANTS,
    TYPE:       LIST,
    INDEX:      [7, 8],
    MAPPING:    MERGE,
    DICT:       PHONEMES
}

P_VOWELS_S19 = {
    KEY:        K_VOWELS,
    TYPE:       LIST,
    INDEX:      [9, 10],
    MAPPING:    MERGE,
    DICT:       PHONEMES
}

P_VOWEL_TYPES_S19 = {
    KEY:        K_VOWEL_TYPES,
    TYPE:       LIST,
    INDEX:      11,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_VOWEL_TYPES,
    FAIL_DICT:  ["phthong", "vowel"]
}

P_PHONETIC_S19 = {
    KEY:        [K_COMPLEX_CONSONANTS, K_TONE, K_STRESS],
    TYPE:       BOOL,
    INDEX:      12,
    MAPPING:    SPLIT
}

P_SYLLABLE_S19 = {
    KEY:        K_SYLLABLES,
    TYPE:       LIST,
    INDEX:      13,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_SYLLABLES,
    FAIL_DICT:  ["CV", "V", "VC"]  # Should not be hardcoded, move to selectors?
}


# Typology Parameters:
P_CITATION = {
    KEY:        K_CITATION,
    TYPE:       STRING,
    INDEX:      4,
    MAPPING:    ONE_TO_ONE
}

P_RECOMMEND = {
    KEY:        K_RECOMMEND,
    TYPE:       STRING,
    INDEX:      5,
    MAPPING:    ONE_TO_ONE
}

P_MORPHOLOGICAL_TYPE = {
    KEY:        K_MORPHOLOGICAL_TYPE,
    TYPE:       LIST,
    INDEX:      6,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_MORPHOLOGY,
    FAIL_DICT:  None
}

P_WORD_FORMATION_F17 = {
    KEY:        K_WORD_FORMATION,
    TYPE:       LIST,
    INDEX:      7,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_WORD_FORMATION_F17,
    FAIL_DICT:  ["ion", "change", "root", "isolat"] # XXXat(ion), (isolat)ing
}

P_WORD_FORMATION_S19 = {
    KEY:        K_WORD_FORMATION,
    TYPE:       LIST,
    INDEX:      7,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_WORD_FORMATION_S19,
    FAIL_DICT:  ["ion", "change", "root", "isolat"] # XXXat(ion), (isolat)ing
}

P_WORD_FORMATION_FREQ = {
    KEY:        K_WORD_FORMATION_FREQ,
    TYPE:       STRING,
    INDEX:      8,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_WORD_FORMATION_FREQ, # UNTESTED!!!
    FAIL_DICT:  ["exclusive", "most", "equal", "prefix", "suffix", "affix", "isolating"]
}

P_WORD_ORDER = {
    KEY:        K_WORD_ORDER,
    TYPE:       LIST,
    INDEX:      9,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_WORD_ORDER,
    FAIL_DICT:  ["free", "S", "V", "O"]
}

P_HEADEDNESS = {
    KEY:        K_HEADEDNESS,
    TYPE:       LIST,
    INDEX:      10,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_HEADEDNESS, # UNTESTED!!!
    FAIL_DICT:  ["head", "initial", "final", "most", "consistent", "mixed"]
}

P_AGREEMENT = {
    KEY:        K_AGREEMENT,
    TYPE:       STRING,
    INDEX:      11,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_AGREEMENT,
    FAIL_DICT:  None
}

P_CASE = {
    KEY:        K_CASE,
    TYPE:       STRING,
    INDEX:      12,
    MAPPING:    ONE_TO_ONE,
    DICT:       D_CASE,
    FAIL_DICT:  None
}

# Which questions should be read from the CSV files for a given dataset,
# and how is the data stored in the corresponding CSV?
# These specify how to convert between a CSV entry and a JSON entry
PARAMS = {
    F17: {
        GRAMMAR: [
            P_LANGUAGE,
            P_NAME,
            P_NETID,
            P_NUM_CONSONANTS,
            P_NUM_VOWELS,
            P_NUM_PHONEMES,
            P_CONSONANTS_F17,
            P_VOWELS_F17,
            P_NUM_CONSONANT_PLACES,
            P_NUM_CONSONANT_MANNERS,
            P_PHONETIC_F17,
            P_SYLLABLE_F17
        ],
        TYPOLOGY: [
            P_LANGUAGE,
            P_NAME,
            P_NETID,
            P_CITATION,
            P_RECOMMEND,
            P_MORPHOLOGICAL_TYPE,
            P_WORD_FORMATION_F17,
            P_WORD_FORMATION_FREQ,
            P_WORD_ORDER,
            P_HEADEDNESS,
            P_AGREEMENT,
            P_CASE
        ]
    },
    S19: {
        GRAMMAR: [
            P_LANGUAGE,
            P_NAME,
            P_NETID,
            P_NUM_CONSONANTS,
            P_NUM_VOWELS,
            P_NUM_PHONEMES,
            P_CONSONANTS_S19,
            P_VOWELS_S19,
            P_NUM_CONSONANT_PLACES,
            P_NUM_CONSONANT_MANNERS,
            P_VOWEL_TYPES_S19,
            P_PHONETIC_S19,
            P_SYLLABLE_S19
        ],
        TYPOLOGY: [ # Not yet updated for S19
            P_LANGUAGE,
            P_NAME,
            P_NETID,
            # P_CITATION, # obsolete in s19
            P_RECOMMEND,
            P_MORPHOLOGICAL_TYPE,
            P_WORD_FORMATION_S19,
            P_WORD_FORMATION_FREQ,
            P_WORD_ORDER,
            P_HEADEDNESS,
            P_AGREEMENT,
            P_CASE
        ]
    }
}


##############################################################################
#                          csvtojson constants (old)                         #
##############################################################################
# Constants across typology/grammar
NETID = 1
NAME  = 2
HASH_SIZE = 16

# CSV format
ROW_DELIMITER = "\n"    # delimits rows (might need carriage return?)
COL_DELIMITER = ","     # delimits columns within a row
INNER_DELIMITER = ";"   # delimits lists within a column
PHONEME_DELIMITER = "/" # Used on either side of a phoneme (e.g. /d/ --> d)

# The indices into the G_STR array corresponding to each attribute's name
G_TIME            = 0
G_NETID           = 1
G_NAME            = 2
G_LANGUAGE        = 3
G_NUM_CONSONANTS  = 4
G_NUM_VOWELS      = 5
G_NUM_PHONEMES    = 6
G_CONSONANTS      = 7
G_VOWELS          = 8
G_PHONETIC        = 9
G_SYLLABLES       = 10

#G_P_3PLUS_PLACES       = 11
#G_P_2PLUS_MANNERS      = 12
G_P_COMPLEX_CONSONANTS = 13
G_P_TONE               = 14
G_P_STRESS             = 15

G_NUM_PLACES  = 16
G_NUM_MANNERS = 17

#The strings to be added as fields in the JSON blob
G_STR = [
    "time",             # G_TIME
    "netid",            # G_NETID
    "name",             # G_NAME
    "language",         # G_LANGUAGE
    "num consonants",   # G_NUM_CONSONANTS
    "num vowels",       # G_NUM_VOWELS
    "num phonemes",     # G_NUM_PHONEMES
    "consonants",       # G_CONSONANTS
    "vowels",           # G_VOWELS
    "phonetic",         # G_PHONETIC
    "syllables",        # G_SYLLABLE
    "3+ places",
    "2+ manners",
    "complex consonants",
    "tone",
    "stress",
    "consonant places",
    "consonant manners"
]

# The strings to be searched for in the raw CSV data for phonetic properties
G_P_STR = [
    "three places of articulation",
    "two manners of articulation",
    "complex consonants",
    "tone",
    "stress"
]

T_TIME            = 0
T_NETID           = 1
T_NAME            = 2
T_LANGUAGE        = 3
T_CITATION        = 4
T_RECOMMEND       = 5
T_MORPHOLOGY      = 6
T_WORD_FORMATION  = 7
T_FORMATION_FREQ  = 8
T_WORD_ORDER      = 9
T_HEADEDNESS      = 10
T_AGREEMENT       = 11
T_CASE            = 12

#GRAMMAR_HEADERS as string
T_STR = [
    "time",
    "netid",
    "name",
    "language",
    "citation",
    "recommend",
    "morphological type",
    "word formation",
    "word formation frequency",
    "word order",
    "headedness",
    "agreement",
    "case"
]
