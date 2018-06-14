from . import csv_importer, language, const
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS
from .const import *

# LingDB class
class LingDB:
    """An object encapsulating useful lingDB queries and properties. A
    collection of language objects"""

################################################################################
#                             Constructor                                      #
#                                                                              #
################################################################################
    def __init__(self, grammarCSV, typologyCSV):
        self.grammarData = csv_importer.readGrammarData(grammarCSV)
        # self.typologyDict = csv_importer.readTypologyData(typologyCSV)
        self.typologyData = {"data":"not yet implemented"}


################################################################################
#                            Getter Methods                                    #
#                                                                              #
################################################################################

    def size(self):
        return len(self.grammarData)

################################################################################
#                             Query Methods                                    #
#                                                                              #
################################################################################

    def queryContainsConsonants(self, bitstring, k, mode):
        """Returns a list of the languages that contain "exactly" k of the
        consonants specified by bitstring, replacing "exactly" with the specified
        mode"""
        results = []
        for lang in self.grammarData:
            if (lang.containsConsonants(bitstring, k, mode)):
                results.append(lang)
        return results

    def queryContainsVowels(self, bitstring, k, mode=EQ):
        """Returns a list of the languages that contain "exactly" k of the
        consonants specified by bitstring, replacing "exactly" with the specified
        mode"""
        results = []
        for lang in self.grammarData:
            if (lang.containsVowels(bitstring, k, mode)):
                results.add(lang)
        return results
