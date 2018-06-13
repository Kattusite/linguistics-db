from . import csv_importer, language, const
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS

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
#                             Query Methods                                    #
#                                                                              #
################################################################################

# not yet implemented
