NETID = 1
NAME  = 2
HASH_SIZE = 16

DICT = "dict"
MULTI = "multi"

DATA_PATH = "data/"

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

G_P_3PLUS_PLACES       = 11
G_P_2PLUS_MANNERS      = 12
G_P_COMPLEX_CONSONANTS = 13
G_P_TONE               = 14
G_P_STRESS             = 15

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

# Dictionaries for use in csvtojson.parsePhrase()
# Generally speaking, the format is:
# The keys in the dict (left side) are the values you would like to store in the json
# The values in the lists (right side) are the values in the raw data you would like to
# be replaced by the key on the left
# If the right-hand-side list is [], it is treated as the left-hand-side string itself
SYLLABLE = {
    DICT: {
        "CV":    [],
        "V":     [],
        "CVC":   [],
        "CCV":   [],
        "CCCV":  [],
        "CCCCV": [],
        "VCC":   [],
        "VCCC":  [],
        "VCCCC": []
    },
    MULTI: True
}

MORPHOLOGY = {
    DICT: {
        "isolating": [],
        "analytic": ["analytic", "not isolating"], # this is a toughie
        "fusional": [],
        "agglutinating": [],
        "polysynthetic": []
    },
    MULTI: True
}

WORD_FORMATION = {
    DICT: {
        "affixation": ["affixation", "prefixation or suffixation"],
        "suffixation": [],
        "prefixation": [],
        "infixation": [],
        "compounding": [],
        "root-and-pattern": [],
        "internal change": [],
        "suppleton": [],
        "stress or tone shift": [],
        "reduplication": [],
        "conversion": [],
        "purely isolating": ["none", "purely isolating"]
    },
    MULTI: True
}

FORMATION_FREQ = {
    DICT: {
        "exclusively" : ["exclusive", "purely"],
        "mostly": ["mostly"],
        "equal": ["equal ","even ","mix "]
    },
    MULTI: False
}

FORMATION_MODE = {
    DICT: {
        "prefixing and suffixing":  ["prefixing and suffixing"],
        "affixation and other":     ["affixation and other"],
        "suffixing":                ["suffixing"],
        "prefixing":                ["prefixing"],
        "non-affixal":              ["non-affixal"],
        "isolating":                ["isolating"]
    },
    MULTI: False
}

# The following dict is not tested for parsePhrase. It is simply a collection
# of all legal combinations of the corresponding freq/mode dicts
FORMATION = {
    DICT: {
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
    },
    MULTI: False
}

WORD_ORDER = {
    DICT: {
        "SVO": [],
        "SOV": [],
        "VSO": [],
        "VOS": [],
        "OVS": [],
        "OSV": [],
        "multiple": ["more than one", "multiple", "several"],
        "none":     ["no basic", "none"]
    },
    MULTI: False
}

HEADEDNESS_FREQ = {
    DICT: {
        "consistently": [],
        "mostly": [],
        "mixed": ["mixed", "equal", "roughly equal"]
    },
    MULTI: False
}

HEADEDNESS_MODE = {
    DICT: {
        "head-initial": [],
        "head-final": [],
        "headedness": ["mixed", "equal", "roughly equal"]
    },
    MULTI: False
}

# The following dict is not tested for parsePhrase. It is simply a collection
# of all legal combinations of the corresponding freq/mode dicts
HEADEDNESS = {
    DICT: {
        "consistently head-initial": [],
        "consistently head-final": [],
        "mostly head-initial": [],
        "mostly head-final": [],
        "mixed headedness": []
    },
    MULTI: False
}

CASE_AGREEMENT = {
    DICT: {
        "none": ["doesn't have", "none"],
        "ergative/absolutive": [],
        "nominative/accusative": [],
        "other": ["other", "some other", "other sort"]
    },
    MULTI: False
}
