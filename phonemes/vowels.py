from . import ipa_json, utils

# Canonical Vowel Order v2.0
# Be sure to check carefully before & after changing this list, as it may have
# unintended consequences, and is used throughout the program in various places
# as the authoritative, canonical list of phonemes.

# (Some) Areas this list affects:
# Generating the clickable phoneme selector GUI elements
# Checking for phoneme membership in language.py
# Creating and comparing phoneme bitstrings

# === IPA Vowel Orderings ===
# Note that these lists are ONLY used for the ordering of IPA charts, and
# metaclass selectors (ipacbox/clbox in allgen.py)
# It is NOT the canonical list of all possible values - see the DICTs below for those
HEIGHTS = [
    "high",
    "near-high",
    "mid-high",
    "mid",
    "mid-low",
    "near-low",
    "low"
]

BACKNESSES = [
    "front",
    "near-front",
    "central",
    "near-back",
    "back"
]

ROUNDEDNESSES = [
    "unrounded",
    "rounded"
]

HEADERS = {
    "height":   HEIGHTS,
    "backness": BACKNESSES,
    "roundedness": ROUNDEDNESSES,

    "word order": ["height", "backness", "roundedness"],
    "axis order": ["backness", "height", "roundedness"]
}


# ==== General Vowel Data ====

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

def getGlyphsFromClass(className):
    return utils.getGlyphsFromClass(data, CLASSES_DICT, className)

def getGlyphsFromClasses(classList):
    return utils.getGlyphsFromClasses(data, CLASSES_DICT, classList)

def getGlyphsMatching(propertyName, propertyValue):
    """Finds a list of all phonemes from data such that the phoneme's
    property named propertyName has the value specified by propertyValue. Return
    a list of the glyphs of all matching phonemes"""
    return utils.getGlyphsMatching(data, propertyName, propertyValue)
