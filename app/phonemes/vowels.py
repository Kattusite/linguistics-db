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
# (In fact, side note, those are not canonical + complete either, they just summarize
# all of the values we've seen so far, not all possible ones. )

HEIGHTS = [
    "high",
    "near-high",
    "mid-high",
    "mid",
    "mid-low",
    "near-low",
    "low"
]

HEIGHT_REGIONS = [
    "high",
    "mid",
    "low"
]

HEIGHT_OFFSETS = [
    "upper",
    "lower"
]

BACKNESSES = [
    "front",
    "near-front",
    "central",
    "near-back",
    "back"
]

BACKNESS_REGIONS = [
    "front",
    "central",
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

# The actual classes to be used in lboxes (more detailed than in IPA trapezoid)
CLBOX_HEADERS = {
    "height": HEIGHT_REGIONS,
    "offset": HEIGHT_OFFSETS,
    "backness": BACKNESS_REGIONS,
    "roundedness": ROUNDEDNESSES,

    "word order": ["offset", "height", "backness", "roundedness"],
    "axis order": ["offset", "height", "backness", "roundedness"]
}


# ==== General Vowel Data ====

data = ipa_json.readIPAFromJson("phonemes/vowels.json")
GLYPHS = utils.glyphs(data)

# Create dicts mapping all possible property values to the glyphs satisfying
# those properties
# E.g. {"voiced":    ["b", "d", ...],
#       "voiceless": ["p", "t", ...], ...}"""
HEIGHT_DICT             = utils.enumerateProperty(data, "height")
HEIGHT_REGION_DICT      = utils.enumerateProperty(data, "height region")
HEIGHT_OFFSET_DICT      = utils.enumerateProperty(data, "height offset")
BACKNESS_DICT           = utils.enumerateProperty(data, "backness")
BACKNESS_REGION_DICT    = utils.enumerateProperty(data, "backness region")
ROUNDEDNESS_DICT        = utils.enumerateProperty(data, "roundedness")
VOICING_DICT            = utils.enumerateProperty(data, "voicing")

# Combine these dicts together
# MAJOR BUG: CLASSES_DICT expects unique keys,
# but is provided with non-unique keys (e.g. "low" is both a key in height, height region)
# Which I believe leads to loss of data.
# Must ensure that the "right" data is not lost
# e.g. if two key/value pairs exist with a key of "low", one should be a superset of
# the other -- we would like to keep the superset not the subset.
# If I'm lucky then later keys will overwrite earlier ones, but this is not
# something nice to rely on.
CLASSES_DICT = {
    **HEIGHT_DICT,
    **HEIGHT_REGION_DICT,
    **HEIGHT_OFFSET_DICT,
    **BACKNESS_DICT,
    **BACKNESS_REGION_DICT,
    **ROUNDEDNESS_DICT,
    **VOICING_DICT
}

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
