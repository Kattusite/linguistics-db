

DATA_PATH = "data/"

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
