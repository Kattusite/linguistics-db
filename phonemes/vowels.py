# Canonical Vowel Order v1.0
# Be sure to check carefully before & after changing this list, as it may have
# unintended consequences, and is used throughout the program in various places
# as the authoritative, canonical list of phonemes.

# (Some) Areas this list affects:
# Generating the clickable phoneme selector GUI elements
# Checking for phoneme membership in language.py
# Creating and comparing phoneme bitstrings

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

def isVowel(s):
    """Returns true iff s is a vowel representable in this system"""
    return s in GLYPHS

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
