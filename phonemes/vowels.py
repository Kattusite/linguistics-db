# Canonical Vowel Order v1.0
# Be sure to check carefully before & after changing this list, as it may have
# unintended consequences, and is used throughout the program in various places
# as the authoritative, canonical list of phonemes.

# (Some) Areas this list affects:
# Generating the clickable phoneme selector GUI elements
# Checking for phoneme membership in language.py
# Creating and comparing phoneme bitstrings
from . import bitstrings

GLYPHS = [
    "a",
    "e",
    "o",
    "i",
    "u",
    "ə",
    "ɨ",
    "ɯ",
    "y",
    "ʌ",
    "ø",
    "ɵ",
    "ʉ"
    # "N/A" # None of the above (remove this and let 0000...000 be implicit)
]

# Order of the list is arbitrary from this line down
# Canonical vowel roundness/height/backness
ROUNDEDNESSES = [
    "any roundedness",
    "rounded",
    "unrounded"
]

HEIGHTS = [
    "any height",
    "high",
    "mid-high",
    "mid",
    "mid-low",
    "low"
]

BACKNESSES = [
    "any backness",
    "front",
    "central",
    "back"
]

CLASS_MATRIX = [
    ROUNDEDNESSES,
    HEIGHTS,
    BACKNESSES
]

# Canonical Vowel Classes
CLASSES = {
    # Height
    "high" : [
        "i",
        "u",
        "ɨ",
        "ɯ",
        "y",
        "ʉ"
    ],
    "mid-high" : [
        "e",
        "o",
        "ø",
        "ɵ"
    ],
    "mid": [
        "ə"
    ],
    "mid-low": [
        "ʌ"
    ],
    "low" : [
        "a"
    ],
    # Backness
    "front": [
        "a",
        "e",
        "i",
        "y",
        "ø",
    ],
    "central": [
        "i",
        "ə",
        "ɵ",
        "ʉ"
    ],
    "back": [
        "o",
        "u",
        "ɯ",
        "ʌ"
    ],

    # Roundedness
    "rounded": [
        "o",
        "u",
        "y",
        "ø",
        "ɵ",
        "ʉ"
    ],
    "unrounded": [
        "a",
        "e",
        "i",
        "ɨ",
        "ɯ",
        "ʌ"
    ]
}

#TODO unify these two functions with the identical ones in the accompanying vowel/consanant file
def getBitstringFromClass(className):
    # If natural class not recognized, return a string of all zeroes
    if className not in CLASSES:
        return "0" * len(GLYPHS)

    classList = CLASSES[className]

    # Otherwise generate the string by iterating through the glpyh list
    bitList = []
    for p in GLYPHS:
        if p in classList:
            bitList.append("1")
        else:
            bitList.append("0")

    return "".join(bitList)

def getBitstringFromClasses(classArr):
    bitstring = ""
    for i, natClass in enumerate(classArr):
        tempBitstring = getBitstringFromClass(natClass)
        if i == 0:
            bitstring = tempBitstring
        else:
            bitstring = bitstrings.AND(bitstring, tempBitstring)
    return bitstring
