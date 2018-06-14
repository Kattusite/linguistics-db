# CSV format
ROW_DELIMITER = "\n"   # delimits rows (might need carriage return?)
COL_DELIMITER = ","    # delimits columns within a row
INNER_DELIMITER = ";"  # delimits lists within a column

PHONEME_DELIMITER = "/" # Used on either side of a phoneme (e.g. /d/ --> d)

# CSV indices
# Indices and human-readable strings for each column of the csv
# NOTE Must be updated every time the csv format changes
#GRAMMAR_HEADERS
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
G_SYLLABLE        = 10

#GRAMMAR_HEADERS as string
G_STR = [
    "time",             # G_TIME
    "netid",            # G_NETID
    "name",             # G_NAME
    "language",         # G_LANGUAGE
    "num_consonants",   # G_NUM_CONSONANTS
    "num_vowels",       # G_NUM_VOWELS
    "num_phonemes",     # G_NUM_PHONEMES
    "consonants",       # G_CONSONANTS
    "vowels",           # G_VOWELS
    "phonetic",         # G_PHONETIC
    "syllable"          # G_SYLLABLE
]

# Equality modes
EQ  = "EQ"  # Match if the number of phoneme matches == target
GEQ = "GEQ"  # Match if the number of phoneme matches >= target
GT  = "GT"   # Match if the number of phoneme matches  > target
LEQ = "LEQ"  # Match if the number of phoneme matches <= target
LT  = "LT"   # Match if the number of phoneme matches  < target
NEQ = "NEQ"  # Match if the number of phoneme matches != target
