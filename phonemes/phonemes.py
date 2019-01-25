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

class Phoneme:
    """A class defining a phoneme object, including several functions for
    constructing them and extracting information"""

    # This is currently just a sketch of an idea... It needs some serious
    # design consideration to work out nicely. 

    def __init__(self, data):
        self.created = True
        return self

    @classmethod
    def from_json(cls, json):
        return cls(json)
