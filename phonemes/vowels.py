# Canonical Vowel Order v1.0
# Be sure to check carefully before & after changing this list, as it may have
# unintended consequences, and is used throughout the program in various places
# as the authoritative, canonical list of phonemes.

# (Some) Areas this list affects:
# Generating the clickable phoneme selector GUI elements
# Checking for phoneme membership in language.py
# Creating and comparing phoneme bitstrings
VOWEL_GLYPHS = [
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


# Canonical Vowel Classes
# Order of the list is arbitrary from this line down
VOWEL_CLASSES = {
    # Place
    "high" : [

    ],
    "mid" : [

    ]
    "low" : [

    ],
    # Manner

    # Voicing
    "voiced": [
        "",
    ],
    "voiceless": [
        "",
    ]
}

def getClassBitstring(className):
    # If natural class not recognized, return a string of all zeroes
    if className not in VOWEL_CLASSES:
        return "0" * len(VOWEL_GLYPHS)

    classList = VOWEL_CLASSES[className]

    # Otherwise generate the string by iterating through the glpyh list
    bitList = []
    for p in VOWEL_GLYPHS:
        if p in classList:
            bitList.append("1")
        else:
            bitList.append("0")

    return "".join(bitList)
