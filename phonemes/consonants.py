# Canonical Consonant Order v1.0
# Be sure to check carefully before & after changing this list, as it may have
# unintended consequences, and is used throughout the program in various places
# as the authoritative, canonical list of phonemes.

# (Some) Areas this list affects:
# Generating the clickable phoneme selector GUI elements
# Checking for phoneme membership in language.py
# Creating and comparing phoneme bitstrings

import json

# NOTE! The order of this list is not arbitrary and strongly affects other
# parts of the program
GLYPHS = [
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

# Order of the list is arbitrary from this line down
# Canonical Consonant Voicings/Places/Manners
VOICINGS = [
    "any voicing",
    "voiced",
    "voiceless"
]

PLACES = [
    "any place",
    "bilabial",
    "labiodental",
    "dental",
    "alveolar",
    "palatal",
    "velar",
    "glottal"
]

MANNERS = [
    "any manner",
    "plosive",
    "fricative",
    "affricate",
    "nasal",
    "liquid",
    "trill",
    "glide"
]

CLASS_MATRIX = [
    VOICINGS,
    PLACES,
    MANNERS
]



# Canonical Consonant Classes
CLASSES = {
    # Place
    "bilabial" : [
        "m",
        "p",
        "b",
    ],
    "labiodental" : [
        "f",
        "v"
    ],
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
    ],
    "glottal": [
        "ʔ",
        "h"
    ],
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
    ],
    "affricate": [
        "ts",
        "dʒ",
        "tʃ"
    ],
    "nasal": [
        "n",
        "m",
        "ŋ",
        "ɲ"
    ],
    "liquid": [
        "l"
    ],
    "trill": [
        "r"
    ],
    "glide": [
        "j",
        "w"
    ],
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

# Reorganizing all the data above into a wordier, more robust format


# IPA row headers (specifies the ordering)
IPA_ROWS = [
    "plosive",
    "aspirated",
    "nasal",
    "trill",
    "tap or flap",
    "fricative",
    "affricate",
    "lateral fricative",
    "approximant",
    "lateral approximant"
]

# IPA col headers (specifies the ordering)
IPA_COLS = [
    "bilabial",
    "labiodental",
    "dental",
    "alveolar",
    "postalveolar",
    "retroflex",
    "palatal",
    "velar",
    "uvular",
    "pharyngeal",
    "glottal"
]

# Specifies left/right ordering of voiced/unvoiced phoneme pairs
IPA_VOICE = [
    "unvoiced",
    "voiced"
]
# IPA chart glyphs (specifies the contents)
# Consider defining each phoneme on its own in the following way:
# t = {
#   "glyph" : "t" # None if not allowed to be selected / unsupported
#   "manner" : "plosive"
#   "place": "alveolar"
#   "voice": "unvoiced"
#   "possible": True # False if should be greyed out
# }
# and then using these definitions to fill in the IPA chart, instead of hardcoding
# This will be 22 data entries per row though.
# Might be worth it in the long run, because it will save the trouble of having
# to hardcode metaclasses -- e.g,
# labials = [c.get("glyph") in consonants if c.get("place") in ["bilabial", "labiodental"]]

IPA = {
    "plosive":              [],
    "aspirated":            [],
    "nasal":                [],
    "trill":                [],
    "tap or flap":          [],
    "fricative":            [],
    "lateral fricative":    [],
    "approximant":          [],
    "lateral approximant":  [],
}


#TODO unify these two functions with the identical ones in the accompanying vowel/consanant file
def getGlyphListFromClass(className):
    # If this is a special bypass class ("Any...") return all ones
    # else If natural class not recognized, return a string of all zeroes
    className = className.lower()
    if "Any ".lower() in className:
        return GLYPHS.copy()
    elif className not in CLASSES:
        raise ValueError("Class " + className + " not recognized as a natural class")
        return []

    classList = CLASSES[className]

    # Otherwise return a copy of the glyphlist for this class
    return classList.copy()

def getGlyphListFromClasses(classList):
    glyphSet = set([])
    for i, natClass in enumerate(classList):
        if i == 0:
            glyphList = getGlyphListFromClass(natClass)
            glyphSet = set(glyphList)
        else:
            glyphList = getGlyphListFromClass(natClass)
            glyphSet = set(glyphList).intersection(glyphSet)
    return list(glyphSet)
