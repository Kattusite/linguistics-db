from . import csv_importer
from .const import *
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS

class Language:
    """An object storing useful information about a language, and query methods
    to access that information"""

################################################################################
#                             Constructors                                     #
#                                                                              #
################################################################################
    def __init__(self, grammarRow, typologyRow):
        self.grammar = self.createGrammarDictFromRow(grammarRow)
        # TODO implement typology data


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
    def getGrammarAttr(self, query):
        """ Given a query string, return the value associated with that attribute
            if it exists """
        if (query not in G_STR):
            print("Error! Attribute %s does not exist in grammar" % query)
            raise IndexError("Attribute %s not a member of grammar" % query)
        return self.grammar[query]

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



################################################################################
#                             Built-ins                                        #
#                                                                              #
################################################################################
    def __str__(self):
        """Returns a string representation of the language (as json)"""
        return "Language.__str__ not yet implemented"

    def __repr__(self):
        """Returns a string representation of the language (as json)"""
        return __str__(self)

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
