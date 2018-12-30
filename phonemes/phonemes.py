"""Data representing the combination of all consonants and all vowels into a
single place"""

from . import consonants, vowels, metaclasses, utils

# Concatenate the consonants and vowels data
data = consonants.data + vowels.data
GLYPHS = utils.glyphs(data)

# ============ Public Functions ============
def isPhoneme(s):
    """Returns True iff s is a glyph of a phoneme represented in this system"""
    return consonants.isConsonant(s) or vowels.isVowel(s)

def getGlyphsMatching(propertyName, propertyValue):
    """Returns a list of the glyphs of any producible phoneme that satisfies
    el[propertyName] == propertyValue"""
    return utils.getGlyphsMatching(data, propertyName, propertyValue)
