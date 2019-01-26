#
# Important NOTE:
# Function signatures in this file are read by lingdb.__init__.py, so the argument lists
# should directly correspond with possible fields in the query from the frontend
#

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
        ret = self.getGrammarAttr(G_STR[G_LANGUAGE])
        if ret is None:
            raise ValueError("A language object was created without a name!")
        return ret

    # TODO Merge getGrammarAttr/getTypologyAttr into getAttr or similar
    def getGrammarAttr(self, key):
        """ Given a query string, return the value associated with that attribute
            if it exists; else raise an error"""
        if (key not in G_STR):
            print("Error! Attribute %s does not exist in grammar" % key)
            raise KeyError("Attribute %s not a member of grammar" % key)
        if key not in self.data:
            print("Warning: Requested %s from language %s but it doesn't exist" %
                  (key, self.getLanguage()))
            return None
        return self.data[key]

    def getTypologyAttr(self, key):
        """ Given a query string, return the value associated with that attribute
            if it exists; else raise an error"""
        if (key not in T_STR):
            print("Error! Attribute %s does not exist in typology" % key)
            raise KeyError("Attribute %s not a member of typology" % key)
        if key not in self.data:
            print("Warning: Requested %s from language %s but it doesn't exist" %
                  (key, self.getLanguage()))
            return None
        return self.data[key]

    def getConsonants(self):
        """Returns the list of consonants for this language"""
        ret = self.getGrammarAttr(G_STR[G_CONSONANTS])
        if ret is None:
            ret = []
        return ret

    def getVowels(self):
        """Returns the list of vowels for this language"""
        ret = self.getGrammarAttr(G_STR[G_VOWELS])
        if ret is None:
            ret = []
        return ret

    def getPhonemes(self):
        """Returns the list of phonemes for this language"""
        return self.getConsonants() + self.getVowels()

    def getSyllables(self):
        """Returns the list of legal syllables in this language"""
        ret = self.getGrammarAttr(G_STR[G_SYLLABLES])
        if ret is None:
            ret = []
        return ret

    def getMorphologicalTypes(self):
        """Returns the list of morphological types for this language"""
        ret = self.getTypologyAttr(T_STR[T_MORPHOLOGY])
        if ret is None:
            ret = []
        return ret

    def getWordFormations(self):
        """Returns the list of word formations for this language"""
        ret = self.getTypologyAttr(T_STR[T_WORD_FORMATION])
        if ret is None:
            ret = []
        return ret



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
        print("ls", ls)
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

        articulationType = "consonant %s" % sel
        num = self.getGrammarAttr(articulationType)
        if compareByMode(num, k, mode):
            return tuple([num])
        else:
            return False



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
        articulationType = "consonant %s" % sel
        num = self.getGrammarAttr(articulationType)
        return compareByMode(num, k, mode)

    def containsConsonantPlaces(self):
        """Returns true if the language has 3+ places of consonant articulation"""
        attr = self.getGrammarAttr(G_STR[G_P_3PLUS_PLACES])
        if attr is None:
            return False
        return attr

    def containsConsonantManners(self):
        """Returns true if the language has 2+ manners of consonant articulation"""
        attr = self.getGrammarAttr(G_STR[G_P_2PLUS_MANNERS])
        if attr is None:
            return False
        return attr

    def containsComplexConsonants(self):
        """Returns true if the language has complex consonants"""
        attr = self.getGrammarAttr(G_STR[G_P_COMPLEX_CONSONANTS])
        if attr is None:
            return False
        return attr

    def containsTone(self):
        """Returns true if the language has tone"""
        attr = self.getGrammarAttr(G_STR[G_P_TONE])
        if attr is None:
            return False
        return attr

    def containsStress(self):
        """Returns true if the language has stress"""
        attr = self.getGrammarAttr(G_STR[G_P_STRESS])
        if attr is None:
            return False
        return attr

    def containsSyllable(self, selList, k, mode):
        """Returns true if *mode *k of the given syllables are legal in this language"""
        matches = self.matchSyllable(selList, k, mode)
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
        return sel == self.getTypologyAttr(T_STR[T_FORMATION_FREQ])

    def hasWordOrder(self, sel):
        """Returns true if sel is the word order of this language"""
        return sel == self.getTypologyAttr(T_STR[T_WORD_ORDER])

    def hasHeadedness(self, sel):
        """Returns true if sel is the word formation frequency of this language"""
        return sel == self.getTypologyAttr(T_STR[T_HEADEDNESS])

    def hasAgreement(self, sel):
        """Returns true if sel is the agreement frequency of this language"""
        return sel == self.getTypologyAttr(T_STR[T_AGREEMENT])

    def hasCase(self, sel):
        """Returns true if sel is the case of this language"""
        return sel == self.getTypologyAttr(T_STR[T_CASE])


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
