# Canonical Consonant Order v1.0
# Be sure to check carefully before & after changing this list, as it may have
# unintended consequences, and is used throughout the program in various places
# as the authoritative, canonical list of phonemes.

# (Some) Areas this list affects:
# Generating the clickable phoneme selector GUI elements
# Checking for phoneme membership in language.py
# Creating and comparing phoneme bitstrings

# NOTE! The order of this list is not arbitrary and strongly affects other
# parts of the program
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

# Canonical Consonant Classes
# Order of the list is arbitrary from this line down
CONSONANT_CLASSES = {
    # Place
    "bilabial" : [
        "m",
        "p",
        "b",
    ],
    "labiodental" : [
        "f",
        "v"
    ]
    "dental" : [
        # Both english "th" belong here but are not contained in 1.0
    ],
    "alveolar": [
        "n",
        "t",
        "d",
        "s",
        "z",
        "ts",
        "r",
        "l"
    ],
    "palatal": [
        "ɲ",
        "j"
    ],
    "velar": [
        "ŋ",
        "k",
        "g",
        "x",
        "w"
    ]
    "glottal": [
        "ʔ",
        "h"
    ]
    # Manner
    "plosive" : [
        "p",
        "t",
        "k",
        "b",
        "d",
        "g",
        "ʔ"
    ],
    "fricative": [
        "f",
        "v",
        "s",
        "z",
        "ʃ",
        "x"
    ]
    "affricate": [
        "ts",
        "dʒ",
        "tʃ"
    ]
    "nasal": [
        "n",
        "m",
        "ŋ",
        "ɲ"
    ]
    "liquid": [
        "l"
    ]
    "trill": [
        "r"
    ]
    "glide": [
        "j",
        "w"
    ]
    # Voicing
    "voiced": [
        "n",
        "t",
        "m",
        "j",
        "l",
        "w",
        "b",
        "d",
        "g",
        "ŋ",
        "r",
        "ɲ",
        "z",
        "dʒ",
        "v"
    ],
    "voiceless": [
        "t",
        "k",
        "s",
        "p",
        "h",
        "ʃ",
        "ʔ",
        "tʃ",
        "f",
        "ts",
        "x"
    ]
}

def getClassBitstring(className):
    # If natural class not recognized, return a string of all zeroes
    if className not in CONSONANT_CLASSES:
        return "0" * len(CONSONANT_GLYPHS)

    classList = CONSONANT_CLASSES[className]

    # Otherwise generate the string by iterating through the glpyh list
    bitList = []
    for p in CONSONANT_GLYPHS:
        if p in classList:
            bitList.append("1")
        else:
            bitList.append("0")

    return "".join(bitList)
