from . import csv_importer
from data.const import *
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS
import json


################################################################################
#                             Constants                                        #
#                                                                              #
################################################################################
# Equality modes
EQ  = "EQ"  # Match if the number of phoneme matches == target
GEQ = "GEQ"  # Match if the number of phoneme matches >= target
GT  = "GT"   # Match if the number of phoneme matches  > target
LEQ = "LEQ"  # Match if the number of phoneme matches <= target
LT  = "LT"   # Match if the number of phoneme matches  < target
NEQ = "NEQ"  # Match if the number of phoneme matches != target

class Language:
    """An object storing useful information about a language, and query methods
    to access that information"""

################################################################################
#                             Constructors                                     #
#                                                                              #
################################################################################
    def __init__(self, jsonObj):
        """Create a language object storing the info contained in the given json obj"""
        self.data = jsonObj


    # Take the gindex'th element of row, and store it as a value in dict d,
    # associated with the human-readable grammar heading for that gindex (from G_STR)
    def addGIndexToDict(self, d, row, gindex):
        d[G_STR[gindex]] = row[gindex]

    def createGrammarDictFromRow(self, row):
        """Creates a dict from a csv-style row of info about this language's grammar"""
        dictEntry = {}

        # For each attribute, get the human readable g_str and associate it
        # with the data from that row of the CSV
        self.addGIndexToDict(dictEntry, row, G_LANGUAGE)
        self.addGIndexToDict(dictEntry, row, G_NAME)
        self.addGIndexToDict(dictEntry, row, G_NETID)
        self.addGIndexToDict(dictEntry, row, G_NUM_CONSONANTS)
        self.addGIndexToDict(dictEntry, row, G_NUM_VOWELS)
        self.addGIndexToDict(dictEntry, row, G_NUM_PHONEMES)
        dictEntry[G_STR[G_CONSONANTS]] = csv_importer.csvConsonantsToBitstring(row[G_CONSONANTS])
        dictEntry[G_STR[G_VOWELS]]     = csv_importer.csvVowelsToBitstring(row[G_VOWELS])
        # TODO Add phonetic / syllable info
        return dictEntry


################################################################################
#                            Getters                                           #
#                                                                              #
################################################################################
    def getGrammarAttr(self, key):
        """ Given a query string, return the value associated with that attribute
            if it exists """
        if (key not in G_STR):
            print("Error! Attribute %s does not exist in grammar" % key)
            raise IndexError("Attribute %s not a member of grammar" % key)
        return self.data[key]

    def getConsonantBitstring(self):
        """Returns the consonant bitstring for this language"""
        return self.getGrammarAttr(G_STR[G_CONSONANTS])

    def getVowelBitstring(self):
        """Returns the vowel bitstring for this language"""
        return self.getGrammarAttr(G_STR[G_VOWELS])

################################################################################
#                             Query Methods                                    #
#                                                                              #
################################################################################
    def containsConsonant(self, glyph):
        """Returns true if glyph is a valid consonant in this language"""
        if glyph in CONSONANT_GLYPHS:
            index = CONSONANT_GLYPHS.index(glyph)
            return getGrammarAttr(self, G_STR[G_CONS])[index] == "1"
        else:
            return False

    def containsVowel(self, glyph):
        """Returns true if glyph is a valid vowel in this language"""
        if glyph in VOWEL_GLYPHS:
            index = VOWEL_GLYPHS.index(glyph)
            return getGrammarAttr(self, G_STR[G_VOWEL])[index] == "1"
        else:
            return False

    def containsConsonants(self, bitstring, k, mode):
        """Returns true if exactly* k of the consonants in bitstring appear
        in this language. If mode is specified, use mode (less than, etc) instead
        of exact equality checking"""
        template = self.getConsonantBitstring()
        matches = compareBitstrings(template, bitstring)
        return compareByMode(matches, k, mode)


    def containsVowels(self, bitstring, k, mode):
        """Returns true if exactly* k of the vowels in bitstring appear
        in this language. If mode is specified, use mode (less than, etc) instead
        of exact equality checking"""
        template = self.getVowelBitstring()
        matches = compareBitstrings(template, bitstring)
        return compareByMode(matches, k, mode)

    def containsVowelClasses(self, classStr, k, mode):
        return "TBD"

    def containsConsonantPlaces(self):
        """Returns true if the language has 3+ places of consonant articulation"""
        return self.getGrammarAttr(G_STR[G_P_3PLUS_PLACES])

    def containsConsonantManners(self):
        """Returns true if the language has 2+ manners of consonant articulation"""
        return self.getGrammarAttr(G_STR[G_P_2PLUS_MANNERS])

    def containsComplexConsonants(self):
        """Returns true if the language has complex consonants"""
        return self.getGrammarAttr(G_STR[G_P_COMPLEX_CONSONANTS])

    def containsTone(self):
        """Returns true if the language has tone"""
        return self.getGrammarAttr(G_STR[G_P_TONE])

    def containsStress(self):
        """Returns true if the language has stress"""
        return self.getGrammarAttr(G_STR[G_P_STRESS])

    def containsSyllable(self, syllable):
        """Returns true if the given syllable is legal in this language"""
        return "TBD"




################################################################################
#                             Built-ins                                        #
#                                                                              #
################################################################################
    def __str__(self):
        """Returns a string representation of the language (as json)"""
        return json.dumps(self.data, indent=4, ensure_ascii=False)

    def __repr__(self):
        """Returns a string representation of the language (as json)"""
        return self.__str__()

    def __eq__(self, another):
        """Returns true if this language equals another"""
        if type(self) != type(another):
            return False
        return self.data == another.data

    def __hash__(self):
        name  = self.data[G_STR[G_NAME]]
        netid = self.data[G_STR[G_NETID]]
        lang  = self.data[G_STR[G_LANGUAGE]]
        return hash((name, netid, lang))


################################################################################
#                            "Private" Helpers                                 #
#                                                                              #
################################################################################
def compareBitstrings(s1, s2):
    """Given two bitstrings representing the same canonical phoneme set,
    return the number of phonemes shared between the two (the number of 1s
    occurring at the same index)"""
    len1 = len(s1)
    len2 = len(s2)
    if (len1 != len2):
        raise ValueError("An attempt was made to compare phoneme bitstrings" +
                         " of differing lengths!")
    matches = 0
    for i in range(len1):
        if (s1[i]=="1" and s2[i]=="1"):
            matches += 1
    return matches

def compareByMode(num1, num2, mode):
    num1 = int(num1)
    num2 = int(num2)
    """Given two numbers, compare them numerically: num1 MODE num2, replacing
    mode by >=, >, <, <=, !=, == as indicated by the value of mode. Return the
    result of comparison"""
    if (mode == EQ):
        return num1 == num2
    elif (mode == NEQ):
        return num1 != num2
    elif (mode == GT):
        return num1  > num2
    elif (mode == GEQ):
        return num1 >= num2
    elif (mode == LT):
        return num1  < num2
    elif (mode == LEQ):
        return num1 <= num2
