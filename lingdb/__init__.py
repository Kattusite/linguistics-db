from . import csv_importer, language, const
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS
from data.const import *
import json

# LingDB class
class LingDB:
    """An object encapsulating useful lingDB queries and properties. A
    collection of language objects"""

################################################################################
#                             Constructor                                      #
#                                                                              #
################################################################################
    def __init__(self, jsonArr):
        """Create a lingdb from an array of objects (dicts) read from json
        with the format described in data/csvtojson.py"""
        self.data = []
        for jsonObj in jsonArr:
            self.data.append(language.Language(jsonObj))


################################################################################
#                            Getter Methods                                    #
#                                                                              #
################################################################################

    def size(self):
        """Return the number of language entries represented in this db"""
        return len(self.data)

################################################################################
#                             Query Methods                                    #
#                                                                              #
################################################################################

    def queryContainsConsonants(self, bitstring, k, mode):
        """Returns a list of the languages that contain "exactly" k of the
        consonants specified by bitstring, replacing "exactly" with the specified
        mode"""
        results = []
        for lang in self.data:
            if (lang.containsConsonants(bitstring, k, mode)):
                results.append(lang)
        return results

    def queryContainsVowels(self, bitstring, k, mode):
        """Returns a list of the languages that contain "exactly" k of the
        consonants specified by bitstring, replacing "exactly" with the specified
        mode"""
        results = []
        for lang in self.data:
            if (lang.containsVowels(bitstring, k, mode)):
                results.append(lang)
        return results

    def queryContainsConsonantPlaces(self):
        """Returns a list of the languages that contain 3+ places of consonant
        articulation"""
        results = []
        for lang in self.data:
            if(lang.containsConsonantPlaces()):
                results.append(lang)
        return results

    def queryContainsConsonantManners(self):
        results = []
        for lang in self.data:
            if(lang.containsConsonantManners()):
                results.append(lang)
        return results

    def queryContainsComplexConsonants(self):
        results = []
        for lang in self.data:
            if(lang.containsComplexConsonants()):
                results.append(lang)
        return results

    def queryContainsTone(self):
        results = []
        for lang in self.data:
            if(lang.containsTone()):
                results.append(lang)
        return results

    def queryContainsStress(self):
        results = []
        for lang in self.data:
            if(lang.containsStress()):
                results.append(lang)
        return results

    def queryContainsSyllable(self, syllable):
        results = []
        for lang in self.data:
            if(lang.containsSyllable(syllable)):
                results.append(lang)
        return results

################################################################################
#                            Built-ins                                    #
#                                                                              #
################################################################################
    def __repr__(self):
        return __str__(self)

    def __str__(self):
        return json.dumps(self.data)

    def __len__(self):
        return self.size()
