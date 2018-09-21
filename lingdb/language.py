#
# Important NOTE:
# Function signatures in this file are read by lingdb.__init__.py, so the argument lists
# should directly correspond with possible fields in the query from the frontend
#

from data.const import *
from phonemes import vowels, consonants
import json


################################################################################
#                             Constants                                        #
#                                                                              #
################################################################################
# Equality modes TODO move to const or eliminate (possible pass a function)
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
    def getLanguage(self):
        """ Return the name of this language"""
        return self.getGrammarAttr(G_STR[G_LANGUAGE])

    def getGrammarAttr(self, key):
        """ Given a query string, return the value associated with that attribute
            if it exists; else raise an error"""
        if (key not in G_STR):
            print("Error! Attribute %s does not exist in grammar" % key)
            raise IndexError("Attribute %s not a member of grammar" % key)
        return self.data[key]

    def getConsonants(self):
        """Returns the list of consonants for this language"""
        return self.getGrammarAttr(G_STR[G_CONSONANTS])

    def getVowels(self):
        """Returns the list of vowels for this language"""
        return self.getGrammarAttr(G_STR[G_VOWELS])

################################################################################
#                                Match Methods                                 #
#               (What elements of this language fulfill criterion x?)          #
################################################################################
    def matchConsonants(self, glyphList):
        """Returns the consonant glyphs in this language present in glyphList"""
        thisSet = set(self.getConsonants())
        thatSet = set(glyphList)
        return list(thatSet.intersection(thisSet))

    def matchVowels(self, glyphList):
        """Returns the vowel glyphs in this language present in glyphList"""
        thisSet = set(self.getVowels())
        thatSet = set(glyphList)
        return list(thatSet.intersection(thisSet))

    def matchConsonantClasses(self, classList):
        """Returns the consonant glyphs in this language that are part of a metaclass in
        classList"""
        thisSet = set(self.getConsonants())
        thatSet = consonants.getGlyphListFromClasses(classList)
        return list(thatSet.intersection(thisSet))

    def matchVowelClasses(self, classList):
        """Returns the vowel glyphs in this language that are part of a metaclass in
        classList"""
        thisSet = set(self.getVowels())
        thatSet = vowels.getGlyphListFromClasses(classList)
        return list(thatSet.intersection(thisSet))



################################################################################
#                             Contains Methods                                 #
#                      (Does this language contain x?)                         #
################################################################################
    def containsConsonant(self, glyph):
        """Returns true if glyph is a valid consonant in this language"""
        return glyph in self.getConsonants()

    def containsVowel(self, glyph):
        """Returns true if glyph is a valid vowel in this language"""
        return glyph in self.getVowels()

    def containsConsonants(self, glyphList, k, mode):
        """Returns true if exactly* k of the consonants in glyphList appear
        in this language. Use mode (less than, etc) instead of exact equality
        checking"""
        matches = self.matchConsonants(glyphList)
        return compareByMode(len(matches), k, mode)


    def containsVowels(self, bitstring, k, mode):
        """Returns true if exactly* k of the vowels in bitstring appear
        in this language. Use mode (less than, etc) instead of exact equality
        checking"""
        matches = self.matchVowels(glyphList)
        return compareByMode(len(matches), k, mode)

    def containsConsonantClasses(self, classList, k, mode):
        return NotImplemented

    def containsVowelClasses(self, classList, k, mode):
        return NotImplemented

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
        return NotImplemented




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
