# Canonical Consonant Order v1.0
# Be sure to check carefully before & after changing this list, as it may have
# unintended consequences, and is used throughout the program in various places
# as the authoritative, canonical list of phonemes.

# (Some) Areas this list affects:
# Generating the clickable phoneme selector GUI elements
# Checking for phoneme membership in language.py

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
IPA_MANNERS = [
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
IPA_PLACES = [
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
IPA_VOICING = [
    "voiceless",
    "voiced"
]

IPA_HEADERS = {
    "manner":  IPA_MANNERS,
    "place":   IPA_PLACES,
    "voicing": IPA_VOICING
}
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


# =============== HELPER Functions ===============
# Read in IPA data from the given json file
def readIPAFromJson(filename):
    file = open(filename, "r", encoding="utf-8")
    cons_arr = json.load(file)
    return cons_arr

# Create IPA table from given ipa data and headers
def createIPATable(data, headers):
    # Get the number of rows and cols (including headers + doubling for voicing)
    num_rows = len(headers["manner"]) + 1
    num_cols = len(headers["place"]) * 2 + 1
    table = [["" for i in range(num_cols)] for j in range(num_rows)]

    for p in data:
        # Get the target row / column
        row = headers["manner"].index(p["manner"]) + 1
        col = headers["place"].index(p["place"]) * 2
        col += headers["voicing"].index(p["voicing"]) + 1

        table[row][col] = p

    # Add in the headers
    for (i, head) in enumerate(headers["manner"]):
        table[i+1][0] = head

    for (i, head) in enumerate(headers["place"]):
        table[0][2*i+1] = head
        table[0][2*i+2] = head

    return table

# Create a dictionary mapping a given characteristic to all glyphs satisfying it
# arr: a list of phoneme objects
# category: the name of the trait type ("manner", "place", "voicing")
def createTraitDict(arr, category):
    dict = {trait: [cons["glyph"] for cons in arr
                    if cons[category] == trait and cons["producible"]
            ]
            for trait in IPA_HEADERS[category]
    }

# ================= JSON processing ===================
# Get Consonant info from consonants.json
# Consonants.json is generated by gen/ipa-json.js from gen/ipa-consonats.html
cons_arr = readIPAFromJson("phonemes/consonants.json")

# Extract glyphs from json
GLYPHSv2 = [cons["glyph"] for cons in cons_arr if cons["producible"]]

# Reconstruct IPA table
IPA_TABLE = createIPATable(cons_arr, IPA_HEADERS)
# print(IPA_TABLE)

# Extract manners from json (change this to createTraitDict)
MANNER_LISTS = createTraitDict(cons_arr, "manner")
# print(MANNER_LISTS)
CLASSESv2 = {}
# print(GLYPHSv2)



# =============== API functions ==================
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
