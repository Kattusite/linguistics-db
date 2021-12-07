# No imports from project (leaf node in any import tree)
from typing import (
    Dict,
    List,
    Optional,
    Union,
)

"""This file defines constants used throughout the program, primarily relating to
handling different datasets and parsing datasets from the raw Google Forms CSV data.

This file (and with any luck only this file) will need to be updated any
time significant changes are made to the survey questions or format.
"""

##############################################################################
#                            Dataset constants                               #
##############################################################################
# Where is a dataset named {0} located, relative to the project root?
DATASET_PATH = "data/datasets/{0}/{1}"

# Dataset Constants
TEST  = "_test"
TEST2 = "_test2"

F17 = "F17"
S19 = "S19"
S19TEST = "S19test"
F19 = "F19"
F21 = "F21"

# Which named datasets do we have?
# F = Fall, S = spring, XX = year 20XX
datasetNames = [
    TEST,
    TEST2,
    S19TEST,
    F17,
    S19,
    F19,
    F21,
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
SURVEYS = (GRAMMAR, TYPOLOGY)

# Parameter names
KEY = "key"
TYPE = "type"
INDEX = "index"
MAPPING = "mapping"
DICT = "parse_dict"
FAIL_LIST = "fail_list"
# SELECTOR / PARSE_DICT / SOMETHING LIKE THAT

PHONEMES = "phonemes"

# Possible types
STRING = "String"                   # Value will be a string
BOOL = "Bool"                       # Value will be a bool
NUM = "Num"                         # Value will be a number (so far must be int)
LIST = "List"                       # Value will be a list
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
K_NAME                  = "student"  # formerly "name"
K_LANGUAGE              = "name"     # formerly "language"
K_COUNTRY               = "country"
K_LANGUAGE_FAMILY       = "language family"
K_ENDANGERMENT_LEVEL    = "endangerment level"
K_NUM_VOWELS            = "num vowels"
K_NUM_CONSONANTS        = "num consonants"
K_NUM_PHONEMES          = "num phonemes"
K_CONSONANTS            = "consonants"
K_VOWELS                = "vowels"
K_NUM_CONSONANT_PLACES  = "num consonant places" # note diff than orig
K_NUM_CONSONANT_MANNERS = "num consonant manners"
K_VOWEL_TYPES           = "vowel types"
K_CONSONANT_TYPES       = "consonant types"
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
    K_COUNTRY,
    K_LANGUAGE_FAMILY,
    K_NUM_VOWELS,
    K_NUM_CONSONANTS,
    K_NUM_PHONEMES,
    K_CONSONANTS,
    K_VOWELS,
    K_NUM_CONSONANT_PLACES,
    K_NUM_CONSONANT_MANNERS,
    K_VOWEL_TYPES,
    K_CONSONANT_TYPES,
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

D_ENDANGERMENT_LEVELS = {
    "0":    [],
    "1":    [],
    "2":    [],
    "3":    [],
    "4":    [],
    "5":    [],
    "6a":   [],
    "6b":   [],
    "7":    [],
    "8a":   [],
    "8b":   [],
    "9":    [],
    "10":   [],
}

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

D_CONSONANT_TYPES = {
    "uvular / retroflex / pharyngeal":      ["uvular", "retroflex", "pharyngeal"],
    "affricates":                           [],
    "prenasalized":                         [],
    "multi-place / secondary articulation": ["multi-place", "secondary articulation"],
    "geminate":                             ["geminate", "long"],
    "glottalized / non-pulmonic":           ["glottalized", "non-pulmonic", "click", "ejective", "implosive"]
}

D_CONSONANT_TYPES_F21 = {
    "clicks":       [],
    "implosives":   [],
    "ejectives":    [],
    "affricates":   [],
    "labialized":   [],
    "palatalized":  [],
    "velarized":    [],
    "aspirated":    [],
}

D_SYLLABLES = {
    "V":            ["V", "onsetless and codaless"],
    "C onset":      ["CV", "single onset"],
    "CC onset":     ["CCV", "two onset"],
    "CCC onset":    ["CCCV", "three onset"],
    "CCCC onset":   ["CCCCV", "four onset"],
    "CCCCC onset":  ["CCCCCV", "five onset"],
    "CCCCCC+ onset":["CCCCCCV", "CCCCCCV+", "six onset", "six or more onset"],
    "C coda":       ["CVC", "VC", "single coda"], # formerly CVC, not "VC"
    "CC coda":      ["VCC", "two coda"],
    "CCC coda":     ["VCCC", "three coda"],
    "CCCC coda":    ["VCCCC", "four coda"],
    "CCCCC coda":   ["VCCCCC", "five coda"],
    "CCCCCC+ coda": ["VCCCCCC", "VCCCCCC+", "six coda", "six or more coda"],
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

# These are defined as functions that take in arguments and construct the
# right parameters for a given semester.
# This is useful because the survey doesn't change much from semester to semester,
# but the order in which questions are asked might change, so we leave index as
# a parameter.
# NOTE: It's tempting to try to extract the indices from the position
# at which each P_XXX appears in the list for a given semester, but this is
# not possible. Some indices aren't integers (e.g. lists of integers, or None)
# so this scheme wouldn't be flexible enough for our needs.

# These variables shall all be prefixed with a P_ to signify they are
# *P*arameter specifications

ParseDict = Dict[str, List[str]]
FailList = List[str]

class SurveySpecification:
    def __init__(self,
                 key: str,
                 _type: str,
                 index: Union[int, List[int], None] = None, # one-to-one, many-to-one, derived
                 mapping: Optional[str] = None,             # ONE_TO_ONE, MERGE, SPLIT, None
                 _dict: Optional[ParseDict] = None,
                 fail_list: Optional[FailList] = None):
        self.key = key
        self.type = _type
        self.index = index
        self.mapping = mapping
        self.parse_dict = _dict
        self.fail_list = fail_list

# A convenience because I already named them all with P
P = SurveySpecification

# Common question specifications that won't change much
def P_NETID(index=1):
    # replace STRING with a new HASH type?
    return P(K_NETID, STRING, index, ONE_TO_ONE)

def P_NAME(index=2):
    # replace STRING with a new HASH type?
    return P(K_NAME, STRING, index, ONE_TO_ONE)

def P_LANGUAGE(index=3):
    return P(K_LANGUAGE, STRING, index, ONE_TO_ONE)

def P_NUM_CONSONANTS(index=4):
    return P(K_NUM_CONSONANTS, NUM, index, ONE_TO_ONE)

def P_NUM_VOWELS(index=5):
    return P(K_NUM_VOWELS, NUM, index, ONE_TO_ONE)

def P_NUM_PHONEMES(index=6):
    return P(K_NUM_PHONEMES, NUM, index, ONE_TO_ONE)

def P_NUM_CONSONANT_PLACES():
    return P(K_NUM_CONSONANT_PLACES, PLACEHOLDER)

def P_NUM_CONSONANT_MANNERS():
    return P(K_NUM_CONSONANT_MANNERS, PLACEHOLDER)

def P_PHONETIC(index=9):
    return P([K_COMPLEX_CONSONANTS, K_TONE, K_STRESS], BOOL, index, SPLIT)

def P_SYLLABLE(index=10):
    fail_list =  ["CV", "V", "VC"]  # Should not be hardcoded, move to selectors?
    return P(K_SYLLABLES, LIST, index, ONE_TO_ONE, D_SYLLABLES, fail_list)

# New grammar questions as of F19
def P_COUNTRY(index=4):
    return P(K_COUNTRY, STRING, index, ONE_TO_ONE)

def P_LANGUAGE_FAMILY(index=5):
    return P(K_LANGUAGE_FAMILY, STRING, index, ONE_TO_ONE)

# New grammar questions as of F21
def P_ENDANGERMENT_LEVEL(index=6):
    # This question has an "Other" option so it's hard to catch everything a student
    # might enter. Some languages will likely go without data on this one.
    # HACK: The true type of this property is STRING, but defining it as a list
    #       allows me to shoehorn queries for it into the "at least k" framework
    # TODO: If I ever write a proper way to handle queries like:
    #       "has an endangerment level of at least one of the levels [5,6,7]"
    #       this should become a string again and be handled in that new way.
    return P(K_ENDANGERMENT_LEVEL, LIST, index, ONE_TO_ONE, D_ENDANGERMENT_LEVELS)

# Things that will more likely change
# Fall 17 specific data format specification
def P_CONSONANTS_F17(index=7):
    return P(K_CONSONANTS, LIST, index, ONE_TO_ONE, PHONEMES)

def P_VOWELS_F17(index=8):
    return P(K_VOWELS, LIST, index, ONE_TO_ONE, PHONEMES)

# Spring 19 specific format specification
def P_CONSONANTS_S19(index=[7,8]):
    return P(K_CONSONANTS, LIST, index, MERGE, PHONEMES)

def P_VOWELS_S19(index=[9,10]):
    return P(K_VOWELS, LIST, index, MERGE, PHONEMES)

def P_VOWEL_TYPES_S19(index=11):
    fail_list = ["phthong", "vowel"] # Should not be hardcoded, move to selectors?
    return P(K_VOWEL_TYPES, LIST, index, ONE_TO_ONE, D_VOWEL_TYPES, fail_list)

# TODO: Add a default index value
def P_CONSONANT_TYPES_F19(index):
    fail_list = None
    return P(K_CONSONANT_TYPES, LIST, index, ONE_TO_ONE, D_CONSONANT_TYPES, fail_list)

# The possible answers changed from earlier years.
def P_CONSONANT_TYPES_F21(index=12):
    # We really should match everything, so this one is very broad
    fail_list = ['ed', 'es']
    return P(K_CONSONANT_TYPES, LIST, index, ONE_TO_ONE, D_CONSONANT_TYPES_F21, fail_list)

# Typology Parameters Fall 17:
def P_CITATION_F17(index=4):
    return P(K_CITATION, STRING, index, ONE_TO_ONE)

def P_RECOMMEND(index=5):
    return P(K_RECOMMEND, STRING, index, ONE_TO_ONE)

def P_MORPHOLOGICAL_TYPE(index=6):
    return P(K_MORPHOLOGICAL_TYPE, LIST, index, ONE_TO_ONE, D_MORPHOLOGY, None)

def P_WORD_FORMATION(index=7):
    fail_list = ["ion", "change", "root", "isolat"] # XXXat(ion), (isolat)ing
    return P(K_WORD_FORMATION, LIST, index, ONE_TO_ONE, D_WORD_FORMATION_F17, fail_list)

def P_WORD_FORMATION_FREQ(index=8):
    fail_list = ["exclusive", "most", "equal", "prefix", "suffix", "affix", "isolating"]
    return P(K_WORD_FORMATION_FREQ, STRING, index, ONE_TO_ONE, D_WORD_FORMATION_FREQ, fail_list)

def P_WORD_ORDER(index=9):
    fail_list = ["free", "S", "V", "O"]
    return P(K_WORD_ORDER, LIST, index, ONE_TO_ONE, D_WORD_ORDER, fail_list)

def P_HEADEDNESS(index=10):
    fail_list = ["head", "initial", "final", "most", "consistent", "mixed"]
    return P(K_HEADEDNESS, LIST, index, ONE_TO_ONE, D_HEADEDNESS, fail_list)

def P_AGREEMENT(index=11):
    return P(K_AGREEMENT, STRING, index, ONE_TO_ONE, D_AGREEMENT, None)

def P_CASE(index=12):
    return P(K_CASE, STRING, index, ONE_TO_ONE, D_CASE, None)


# Which questions should be read from the CSV files for a given dataset,
# and how is the data stored in the corresponding CSV?
# These specify how to convert between a CSV entry and a JSON entry
# The order in the list determines the order in which the fields will appear
# in the final JSON dataset.
# The .index property of each SurveySpecification determines the order in which
# the fields appear in the input survey CSV.
PARAMS = {
    F17: {
        GRAMMAR: [
            P_LANGUAGE(),
            P_NAME(),
            P_NETID(),
            P_NUM_CONSONANTS(),
            P_NUM_VOWELS(),
            P_NUM_PHONEMES(),
            P_CONSONANTS_F17(),
            P_VOWELS_F17(),
            P_NUM_CONSONANT_PLACES(),
            P_NUM_CONSONANT_MANNERS(),
            P_PHONETIC(9),
            P_SYLLABLE(10)
        ],
        TYPOLOGY: [
            P_LANGUAGE(),
            P_NAME(),
            P_NETID(),
            P_CITATION_F17(4),
            P_RECOMMEND(5),
            P_MORPHOLOGICAL_TYPE(6),
            P_WORD_FORMATION(7),
            P_WORD_FORMATION_FREQ(8),
            P_WORD_ORDER(9),
            P_HEADEDNESS(10),
            P_AGREEMENT(11),
            P_CASE(12)
        ]
    },
    S19: {
        GRAMMAR: [
            P_LANGUAGE(),
            P_NAME(),
            P_NETID(),
            P_NUM_CONSONANTS(),
            P_NUM_VOWELS(),
            P_NUM_PHONEMES(),
            P_CONSONANTS_S19(),
            P_VOWELS_S19(),
            P_NUM_CONSONANT_PLACES(),
            P_NUM_CONSONANT_MANNERS(),
            P_VOWEL_TYPES_S19(),
            P_PHONETIC(12),
            P_SYLLABLE(13)
        ],
        TYPOLOGY: [
            P_LANGUAGE(),
            P_NAME(),
            P_NETID(),
            P_RECOMMEND(4),
            P_MORPHOLOGICAL_TYPE(5),
            P_WORD_FORMATION(6),
            P_WORD_FORMATION_FREQ(7),
            P_WORD_ORDER(8),
            P_HEADEDNESS(9),
            P_AGREEMENT(10),
            P_CASE(11)
        ]
    },
    F19: {
        GRAMMAR: [
            P_LANGUAGE(),
            P_NAME(),
            P_NETID(),
            P_COUNTRY(4),
            P_LANGUAGE_FAMILY(5),
            P_NUM_CONSONANTS(6),
            P_NUM_VOWELS(7),
            P_NUM_PHONEMES(8),
            P_CONSONANTS_S19([9,10]),
            P_CONSONANT_TYPES_F19(11),
            P_VOWELS_S19([12,13]),
            P_VOWEL_TYPES_S19(14),
            P_NUM_CONSONANT_PLACES(),
            P_NUM_CONSONANT_MANNERS(),
            # P_PHONETIC(15), # !!!!
            P_SYLLABLE(15)
        ],
        TYPOLOGY: [
            P_LANGUAGE(),
            P_NAME(),
            P_NETID(),
            P_RECOMMEND(4),
            P_MORPHOLOGICAL_TYPE(5),
            P_WORD_FORMATION(6),
            P_WORD_FORMATION_FREQ(7),
        ]
    },
    F21: {
        GRAMMAR: [
            P_LANGUAGE(),
            P_NAME(),
            P_NETID(),
            P_COUNTRY(4),
            P_LANGUAGE_FAMILY(5),
            P_ENDANGERMENT_LEVEL(6),
            P_NUM_CONSONANTS(7),
            P_NUM_VOWELS(8),
            P_NUM_PHONEMES(9),
            P_CONSONANTS_S19([10,11]),
            P_CONSONANT_TYPES_F21(12),
            P_VOWELS_S19([13,14]),
            P_VOWEL_TYPES_S19(15),
            P_NUM_CONSONANT_PLACES(),
            P_NUM_CONSONANT_MANNERS(),
            P_PHONETIC(16),
            P_SYLLABLE(17)
        ],
        TYPOLOGY: [
            P_LANGUAGE(),
            P_NAME(),
            P_NETID(),
            P_RECOMMEND(4),
            P_MORPHOLOGICAL_TYPE(5),
            P_WORD_FORMATION(6),
            P_WORD_FORMATION_FREQ(7),
            P_WORD_ORDER(8),
            P_HEADEDNESS(9),
        ]
    },
}


##############################################################################
#                          csvtojson constants (old)                         #
##############################################################################
# In general, avoid using these constants. Use the newer parameter definitions
# above.

# Constants across typology/grammar
NETID = 1
NAME  = 2
LANGUAGE = 3
HASH_SIZE = 16
# NOTE: 16 may be too high (not anonymous enough)
# - shorter hashes <=6 or 7 give better anonymity properties, but increase risk of
# - collisions (8 seem too high also)
# - note that anonymity is less critical than guaranteed correctness for this
# application so higher values are OK

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
    "student",          # G_NAME
    "name",             # G_LANGUAGE
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
    "student",
    "name",
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
