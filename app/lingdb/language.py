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
#                             Class Constants                                  #
#                                                                              #
################################################################################


################################################################################
#                             Query Methods                                    #
#                                                                              #
################################################################################
    def getGrammarAttr(self, query):
        """ Given a query string, return the value associated with that attribute
            if it exists """
        if (query not in G_NAMES):
            print("Error! Attribute %s does not exist in grammar" % query)
            return None
        return grammar[query]

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

    def containsConsonants(self, bitstring, k, mode=EQ):
        """Returns true if exactly* k of the consonants in bitstring appear
        in this language."""



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
