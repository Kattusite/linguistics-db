#
# Important NOTE:
# Function signatures in this file are read by lingdb.__init__.py, so the argument lists
# should directly correspond with possible fields in the query from the frontend
#

from .exceptions import NoLanguageDataError
from data.const import *
from phonemes import vowels, consonants, metaclasses
import json


################################################################################
#                             Constants                                        #
#                                                                              #
################################################################################
# Equality modes TODO move to const or eliminate (possible pass a function)
EQ  = "exactly"       # Match if the number of phoneme matches == target
GEQ = "at least"      # Match if the number of phoneme matches >= target
GT  = "more than"     # Match if the number of phoneme matches  > target
LEQ = "at most"       # Match if the number of phoneme matches <= target
LT  = "less than"     # Match if the number of phoneme matches  < target
NEQ = "not equal to"  # Match if the number of phoneme matches != target
ALL = "all"

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
        if K_LANGUAGE not in jsonObj:
            raise ValueError("Cannot construct a language without a name!")
        self.name = self.data[K_LANGUAGE]


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
        return self.name

    def getAttr(self, attr):
        """Return the attribute of a language with a given name, or raise a
        NoLanguageDataError and return None if that attr does not exist for this
        language. If an illegal attr is provided, raise a KeyError"""
        if attr not in VALID_KEYS:
            raise KeyError("{0} is not a valid key for languages".format(attr))

        if attr not in self.data:
            print("Warning! Requested {0} from Language {1} but no such data exists".format(attr, self.name))
            raise NoLanguageDataError("Language {0} has no data for the {1} attr".format(self.name, attr))
            return None

        return self.data[attr]

    def hasAttr(self, attr):
        """Return true if the language has any data for the requested attr, or
        False if this attr is not represented in this lang"""

        if attr not in VALID_KEYS:
            raise KeyError("{0} is not a valid key for languages".format(attr))

        return (attr in self.data)

    # Deprecated
    def getGrammarAttr(self, key):
        """ Given a query string, return the value associated with that attribute
            if it exists; else raise an error"""
        print("Warning! getGrammarAttr is deprecated. Use getAttr instead.")
        return self.getAttr(key)

    # Deprecated
    def getTypologyAttr(self, key):
        """ Given a query string, return the value associated with that attribute
            if it exists; else raise an error"""
        print("Warning! getTypologyAttr is deprecated. Use getAttr instead.")
        return self.getAttr(key)

    def getConsonants(self):
        """Returns the list of consonants for this language"""
        return self.getAttr(K_CONSONANTS)

    def getVowels(self):
        """Returns the list of vowels for this language"""
        return self.getAttr(K_VOWELS)

    def getPhonemes(self):
        """Returns the list of phonemes for this language"""
        # Should catch NoLanguageDataError ?
        return self.getConsonants() + self.getVowels()

    def getVowelTypes(self):
        """Returns the list of vowel types in this language"""
        return self.getAttr(K_VOWEL_TYPES)


    def getSyllables(self):
        """Returns the list of legal syllables in this language"""
        return self.getAttr(K_SYLLABLES)

    def getMorphologicalTypes(self):
        """Returns the list of morphological types for this language"""
        return self.getAttr(K_MORPHOLOGICAL_TYPE)

    def getWordFormations(self):
        """Returns the list of word formations for this language"""
        return self.getAttr(K_WORD_FORMATION)

    def getWordOrders(self):
        """Returns the list of word orders of this language"""
        return self.getAttr(K_WORD_ORDER)

    def getHeadedness(self):
        """Returns the headedness of this language, as a singleton list for
        hacky reasons"""
        # If it were not a list, it would be less intuitive to use the match
        # methods on it.
        return self.getAttr(K_HEADEDNESS)




################################################################################
#                                Match Methods                                 #
#               (What elements of this language fulfill criterion x?)          #
################################################################################

    def match(self, ls, selList, k, mode):
        thisSet = set(ls)
        thatSet = set(selList)
        both = list(thatSet.intersection(thisSet))

        # If number of items in both fails the mode-comparison to k, return []
        if (not compareByMode(len(both), k, mode)):
            return []
        # Prevent [] from being treated as Falsy if it satisfies the compareByMode
        elif both == []:
            return True
        return both

    def matchConsonants(self, selList, k, mode):
        """Returns the consonant glyphs in this language present in selList,
        if the number of matches is at least* (or mode) k"""
        return self.match(self.getConsonants(), selList, k, mode)

    def matchVowels(self, selList, k, mode):
        """Returns the vowel glyphs in this language present in selList,
        if the number of matches is at least* (or mode) k"""
        return self.match(self.getVowels(), selList, k, mode)

    def matchConsonantClasses(self, selList, k, mode):
        """Returns the consonant glyphs in this language that are part of a metaclass in
        selList, if the number of matches is at least* (or mode) k"""
        ls = consonants.getGlyphsFromClasses(selList)
        return self.matchConsonants(ls, k, mode)

    def matchVowelClasses(self, selList, k, mode):
        """Returns the vowel glyphs in this language that are part of a metaclass in
        selList, if the number of matches is at least* (or mode) k"""
        ls = vowels.getGlyphsFromClasses(selList)
        return self.matchVowels(ls, k, mode)

    def matchMetaclasses(self, selList, k, mode):
        """Returns the phoneme glyphs in this language that are part of a metaclass in
        selList, if the number of matches is at least* (or mode) k"""
        # BUG: in utils.py, this might relies on the wrong class dict -
        # also it uses intersection, rather than union. bug?
        ls = metaclasses.getGlyphsFromClasses(selList)
        phonemes = self.getPhonemes()
        return self.match(phonemes, ls, k, mode)

    def matchSyllable(self, selList, k, mode):
        """Returns the syllables in this language that are part of selList, if
        the number of matches is *mode *k"""
        return self.match(self.getSyllables(), selList, k, mode)

    def matchMorphologicalType(self, selList, k, mode):
        """Returns the morphological types in this language that are part of selList,
        if the number of matches is at least* (or mode) k"""
        return self.match(self.getMorphologicalTypes(), selList, k, mode)

    def matchWordFormation(self, selList, k, mode):
        """Return the word formation strategies in this language that are part of selList,
        if the number of matches is at least* (or mode) k"""
        return self.match(self.getWordFormations(), selList, k, mode)

    def matchConsonantArticulation(self, sel, k, mode):
        """Return the number of 'sel' (sel is 'place' or 'manner')
        articulation types in this language, if this number is at least*
        (or mode) k. Else, return False. """

        articulationType = "num consonant %s" % sel # hacky, revise to fix magic string
        num = self.data[articulationType] # hacky and could raise Error, must handle gracefully
        if compareByMode(num, k, mode):
            return tuple([num])
        else:
            return False

    def matchVowelType(self, selList, k, mode):
        """Return the vowel types in this language that are part of selList,
        if the number of matches is *at least (mode) *k"""
        return self.match(self.getVowelTypes(), selList, k, mode)

    def matchPhonemeInventorySize(self, sel, k, mode):
        """Return the phoneme inventory size of type 'sel'
        ("consonants", "vowels", "phonemes") if this number is at least*
        (or mode) k. Else, return False. """

        phonemeInvSize = "num %s" % sel
        num = self.getAttr(phonemeInvSize)
        if compareByMode(num, k, mode):
            return tuple([num])
        else:
            return False


    def matchWordOrder(self, selList, k, mode):
        """Return the word orders in this language that are part of selList, if
        the number of matches is at least* (or mode) k"""
        return self.match(self.getWordOrders(), selList, k, mode)

    def matchHeadedness(self, selList, k, mode):
        """Return the headedness of this language that are part of selList, if
        the number of matches is at least* (or mode) k"""
        return self.match(self.getHeadedness(), selList, k, mode)



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

    def containsConsonants(self, selList, k, mode):
        """Returns true if exactly* k of the consonants in selList appear
        in this language. Use mode (less than, etc) instead of exact equality
        checking"""
        matches = self.matchConsonants(selList, k, mode)
        return compareByMode(len(matches), k, mode)

    def containsVowels(self, selList, k, mode):
        """Returns true if exactly* k of the vowels in selList appear
        in this language. Use mode (less than, etc) instead of exact equality
        checking"""
        matches = self.matchVowels(selList, k, mode)
        return compareByMode(len(matches), k, mode)

    def containsConsonantClasses(self, selList, k, mode):
        matches = self.matchConsonantClasses(selList, k, mode)
        return compareByMode(len(matches), k, mode)

    def containsVowelClasses(self, selList, k, mode):
        matches = self.matchVowelClasses(selList, k, mode)
        return compareByMode(len(matches), k, mode)

    def containsConsonantArticulation(self, sel, k, mode):
        """Returns true if there are exactly* k of the selected articulation types
        in this language"""
        articulationType = "num consonant %s" % sel
        num = self.getAttr(articulationType)
        return compareByMode(num, k, mode)

    # Deprecated
    def containsConsonantPlaces(self):
        """Returns true if the language has 3+ places of consonant articulation"""
        return self.getAttr(K_3_PLUS_PLACES)


    # Deprecated
    def containsConsonantManners(self):
        """Returns true if the language has 2+ manners of consonant articulation"""
        return self.getAttr(K_2_PLUS_MANNERS)


    def containsComplexConsonants(self):
        """Returns true if the language has complex consonants"""
        return self.getAttr(K_COMPLEX_CONSONANTS)
        # return False if NoLanguageDataError ?

    def containsTone(self):
        """Returns true if the language has tone"""
        return self.getAttr(K_TONE)
        # return False if NoLanguageDataError ?

    def containsStress(self):
        """Returns true if the language has stress"""
        return self.getAttr(K_STRESS)
        # return False if NoLanguageDataError ?

    def containsSyllable(self, selList, k, mode):
        """Returns true if *mode *k of the given syllables are legal in this language"""
        matches = self.matchSyllable(selList, k, mode)
        return compareByMode(len(matches), k, mode)

    def hasPhonemeInventorySize(self, sel, k, mode):
        """Returns true if this language has a phoneme inventory with *mode *k of
        the sel phoneme type"""
        matches = self.matchPhonemeInventorySize(selList, k, mode)
        return compareByMode(len(matches), k, mode)

    def hasMorphologicalType(self, selList, k, mode):
        """Returns true if *mode* k of the given morphological types are
        present in this language"""
        matches = self.matchMorphologicalType(selList, k, mode)
        return compareByMode(len(matches), k, mode)

    def hasWordFormation(self, selList, k, mode):
        """Returns true if *mode* k of the given word formation types are
        present in this language"""
        matches = self.matchWordFormation(selList, k , mode)
        return compareByMode(len(matches), k, mode)

    def hasFormationFreq(self, sel):
        """Returns true if sel is the word formation frequency of this language"""
        return sel == self.getAttr(K_WORD_FORMATION_FREQ)

    def hasWordOrder(self, sel):
        """Returns true if sel is the word order of this language"""
        return sel == self.getAttr(K_WORD_ORDER)

    def hasHeadedness(self, sel):
        """Returns true if sel is the headedness of this language"""
        return sel == self.getAttr(K_HEADEDNESS)

    def hasAgreement(self, sel):
        """Returns true if sel is the agreement of this language"""
        return sel == self.getAttr(K_AGREEMENT)

    def hasCase(self, sel):
        """Returns true if sel is the case of this language"""
        return sel == self.getAttr(K_CASE)


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
    elif (mode == ALL):
        return num1 >= num2
    else:
        raise ValueError("Unexpected comparison mode: %s" % mode)
