from . import ipa_json, utils

# Canonical Vowel Order v2.0
# Be sure to check carefully before & after changing this list, as it may have
# unintended consequences, and is used throughout the program in various places
# as the authoritative, canonical list of phonemes.

# (Some) Areas this list affects:
# Generating the clickable phoneme selector GUI elements
# Checking for phoneme membership in language.py
# Creating and comparing phoneme bitstrings


data = ipa_json.readIPAFromJson("phonemes/vowels.json")
GLYPHS = utils.glyphs(data)

# Create dicts mapping all possible property values to the glyphs satisfying
# those properties
# E.g. {"voiced":    ["b", "d", ...],
#       "voiceless": ["p", "t", ...], ...}"""
HEIGHT_DICT         = utils.enumerateProperty(data, "height")
BACKNESS_DICT       = utils.enumerateProperty(data, "backness")
ROUNDEDNESS_DICT    = utils.enumerateProperty(data, "roundedness")
VOICING_DICT        = utils.enumerateProperty(data, "voicing")

# Combine these dicts together
CLASSES_DICT = {**HEIGHT_DICT,
                **BACKNESS_DICT,
                **ROUNDEDNESS_DICT,
                **VOICING_DICT}

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

def getGlyphsMatching(propertyName, propertyValue):
    """Finds a list of all phonemes from data such that the phoneme's
    property named propertyName has the value specified by propertyValue. Return
    a list of the glyphs of all matching phonemes"""
    return utils.getGlyphsMatching(data, propertyName, propertyValue)
