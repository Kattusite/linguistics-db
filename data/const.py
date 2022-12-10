# No imports from project (leaf node in any import tree)
import dataclasses
import enum

from typing import (
    Iterable,
    List,
    Mapping,
    Optional,
    Union,
)

"""This file defines constants used throughout the program, primarily relating to
handling different datasets and parsing datasets from the raw Google Forms CSV data.

This file (and with any luck only this file) will need to be updated any
time significant changes are made to the survey questions or format.
"""

################################################################################
#                            Dataset constants
################################################################################
# Where is a dataset named {0} located, relative to the project root?
DATASET_PATH = "data/datasets/{0}/{1}"

# Dataset Constants
class Datasets(enum.Enum):
    """ Which named datasets do we have?
    F = Fall, S = Spring, XX = year (20XX)
    """

    # Test datasets
    TEST  = "_test"
    TEST2 = "_test2"

    # Semester datasets
    F17 = "F17"
    S19 = "S19"
    S19TEST = "S19test"
    F19 = "F19"
    F21 = "F21"
    F22 = "F22"

    @classmethod
    def names(cls) -> Iterable[str]:
        """ Return an iterable of the names of all known datasets. """
        return [val.value for val in cls.__members__.values()]

# alias for clarity
Semesters = Datasets

# Which surveys are available?
class Surveys(enum.Enum):
    """ Which surveys are available?
    - GRAMMAR: The first survey of the semester (phonology, phonemes, articulation)
    - TYPOLOGY: The second survey of the semester (morphology, word formation)

    NOTE: The names `GRAMMAR` and `TYPOLOGY` are not very descriptive;
        they linger for historical reasons, since the original names of the surveys
        happened to include the words "GRAMMAR" and "TYPOLOGY".
    """
    GRAMMAR = "grammar"    # From the "Grammar Work 2" survey
    TYPOLOGY = "typology"  # From the final "Typology" survey

    @classmethod
    def names(cls) -> Iterable[str]:
        """ Return an iterable of the names of all known surveys. """
        return [val.value for val in cls.__members__.values()]


################################################################################
#                    ValueType and Mappings constants
################################################################################

# Possible value types
class ValueType(enum.Enum):
    """ The data type of a JSON value. """
    # NOTE: We would just use the builtin types `str`, `bool`, etc.
    #   but we serialize these to JSON in some of our API calls

    STRING = "String"
    """ Value will be a str. """

    BOOL = "Bool"
    """ Value will be a bool. """

    NUM = "Num"
    """ Value will be a number. (right now this means only `int). """

    LIST = "List"
    """ Value will be a list. """

    PLACEHOLDER = "placeholder"
    """ Value will be set by someone else (e.g. derived values like "number of manners"). """

    # HASH = "hash" # tbd.. maybe can use?
    # """ Not yet implemented. Value will be a str hash of some underlying str. """

# alias to save typing:
# T for Type
T = ValueType

# Possible mappings
class Mappings(enum.Enum):
    """ The possible mapping relationships from survey questions to JSON values. """
    ONE_TO_ONE = "one to one"
    """ One survey question will fill one JSON field. """

    SPLIT = "split"
    """ One survey question will be split apart to fill many JSON fields. """

    MERGE = "merge"
    """ Many survey questions will be merged to fill a single JSON field. """

# alias to save typing:
# M for Mappings
M = Mappings

################################################################################
#                                JSON Keys
################################################################################

class JsonKey(enum.Enum):
    """ Possible keys in the JSON entry for each language. """
    NETID                 = "netid"
    NAME                  = "student"  # formerly "name"
    LANGUAGE              = "name"     # formerly "language"
    COUNTRY               = "country"
    LANGUAGE_FAMILY       = "language family"
    ENDANGERMENT_LEVEL    = "endangerment level"
    NUM_VOWELS            = "num vowels"
    NUM_CONSONANTS        = "num consonants"
    NUM_PHONEMES          = "num phonemes"
    CONSONANTS            = "consonants"
    VOWELS                = "vowels"
    NUM_CONSONANT_PLACES  = "num consonant places" # note diff than orig
    NUM_CONSONANT_MANNERS = "num consonant manners"
    VOWEL_TYPES           = "vowel types"
    CONSONANT_TYPES       = "consonant types"
    HAS_3_PLUS_PLACES     = "3+ places"   # deprecated
    HAS_2_PLUS_MANNERS    = "2+ manners"  # deprecated
    COMPLEX_CONSONANTS    = "complex consonants"
    TONE                  = "tone"
    # NOTE: Before F22, STRESS was the only kind of stress -- it indicated "predictable stress".
    #   In F22 a new option was added for "unpredictable stress".
    #   Now STRESS is a derived value, true if either kind of stress appears.
    STRESS                = "stress"
    PREDICTABLE_STRESS    = "predictable stress"
    UNPREDICTABLE_STRESS  = "unpredictable stress"
    SYLLABLES             = "syllables"

    CITATION              = "citation"
    RECOMMEND             = "recommend"
    MORPHOLOGICAL_TYPE    = "morphological type"
    WORD_FORMATION        = "word formation"
    WORD_FORMATION_FREQ   = "word formation frequency"
    AFFIXATION_FREQ       = "affixal word formation frequency"
    NON_AFFIXATION_FREQ   = "non-affixal word formation frequency"
    FUNCTIONAL_MORPHOLOGY = "functional morphology"
    WORD_ORDER            = "word order"
    HEADEDNESS            = "headedness"
    CASE                  = "case"
    AGREEMENT             = "agreement"

# alias to save typing
# K for Key
K = JsonKey

################################################################################
#                               FuzzySearchTerms
################################################################################
# This is where FuzzySearchTerms (to be used in `fuzzy_match_phrase`) will be defined.
# Previously these objects were named `parseDicts`.
# There are some similar data structures defined directly in selectors.py;
# the dicts defined in that file possibly refer to derived types, or to some
# data that is *only* relevant for autogen.py and specifying frontend selectors.

# The FuzzySearchTerms below are the ONLY dicts of this kind that will ever
# need to be passed to `fuzzy_match_phrase()`.

Candidate = str
SearchTerm = str

PHONEMES = "phonemes"
""" A special value that can be used in place of a FuzzySearchTerms object.

If this value is passed, we'll assume that the list of possible values is the list
of known phonemes.
"""

# TODO: Should we rename `FuzzySearchTerms` to `FuzzySearchCandidate` to keep it singular?
class FuzzySearchTerms(dict, Mapping[Candidate, List[SearchTerm]]):
    """ A hybrid class, both defining FuzzySearchTerms, and acting as a namespace
    to contain several instances thereof. See docstring of `fuzzy_match_phrase()`. """

    def __init__(self, d: dict):
        super().__init__(d)

    def __or__(self, other: "FuzzySearchTerms"):
        """ Merge this FuzzySearchTerms with another FuzzySearchTerms """
        # Right now I don't have any cases where the keys should overlap.
        # As a sanity check, raise an error if a key would be clobbered.
        conflicting_keys = set(self.keys()).intersection(set(other.keys()))
        if conflicting_keys:
            raise ValueError(f"Cannot merge FuzzySearchTerms with conflicting search terms for candidates: {conflicting_keys}")
        return FuzzySearchTerms({**self, **other})

    def candidates(self) -> Iterable[str]:
        """ Return the possible candidate matches. """
        return self.keys()

    def search_terms(self, candidate: str) -> Iterable[str]:
        """ Return the search terms associated with a particular candidate match. """
        return self[candidate]

# Group all of the named instances of this class under a namespace.
class AllFuzzySearchTerms:
    """ A namespace grouping all named instances of FuzzySearchTerms. """
    # TODO: I think we could achieve this with a single class with a custom
    #   metaclass, but that sounds a lot more finnicky than just using the
    #   second class.
    # Almost nobody besides `AllFuzzySearchTerms` ever refers to `FuzzySearchTerms`
    # by name, so we could almost make it a nested class if we wanted, but that would
    # make it harder to use in type annotations, so we don't do that.

    # For the Grammar survey
    ENDANGERMENT_LEVELS = FuzzySearchTerms({
        "0":    [],
        "1":    [],
        "2":    [],
        "3":    [],
        "4":    [],
        "5":    [],
        "6a":   [],
        "6b":   [],
        "7":    [],
        "8a":   [],
        "8b":   [],
        "9":    [],
        "10":   [],
    })

    VOWEL_TYPES = FuzzySearchTerms({
        "nasalized":        [],
        "long":             [],
        "voiceless":        [],
        "breathy":          [],
        "creaky":           [],
        "pharyngealized":   [],
        "diphthongs":       [],
        "triphthongs":      []
    })

    CONSONANT_TYPES = FuzzySearchTerms({
        "uvular / retroflex / pharyngeal":      ["uvular", "retroflex", "pharyngeal"],
        "affricates":                           [],
        "prenasalized":                         [],
        "multi-place / secondary articulation": ["multi-place", "secondary articulation"],
        "geminate":                             ["geminate", "long"],
        "glottalized / non-pulmonic":           ["glottalized", "non-pulmonic", "click", "ejective", "implosive"]
    })

    CONSONANT_TYPES_F21 = FuzzySearchTerms({
        "clicks":       [],
        "implosives":   [],
        "ejectives":    [],
        "affricates":   [],
        "labialized":   [],
        "palatalized":  [],
        "velarized":    [],
        "aspirated":    [],
    })

    CONSONANT_TYPES_F22 = FuzzySearchTerms({
        "clicks":           [],
        "implosives":       [],
        "ejectives":        [],
        "affricates":       [],
        "labialized":       [],
        "palatalized":      [],
        "velarized":        [],
        "aspirated":        [],
        "glottalized":      [],
        "pharyngealized":   [],
        "pre-nasalized":    [],
    })

    PHONETIC = FuzzySearchTerms({
        K.COMPLEX_CONSONANTS.value:     [],
        K.TONE.value:                   [],
        K.STRESS.value:                 [],
        # Before F22, there was only one "stress" option,
        # and it specifically indicated "predictable stress".
        K.PREDICTABLE_STRESS.value:     ['stress is predictable', 'stress is mostly predictable'],
    })

    PHONETIC_F22 = FuzzySearchTerms({
        K.COMPLEX_CONSONANTS.value:     [],
        K.TONE.value:                   [],
        K.STRESS.value:                 [],
        K.PREDICTABLE_STRESS.value:     ['mostly predictable'],
        K.UNPREDICTABLE_STRESS.value:   ['not predictably'],
    })

    SYLLABLES = FuzzySearchTerms({
        "V":            ["V", "onsetless and codaless"],
        "C onset":      ["CV", "single onset"],
        "CC onset":     ["CCV", "two onset"],
        "CCC onset":    ["CCCV", "three onset"],
        "CCCC onset":   ["CCCCV", "four onset"],
        "CCCCC onset":  ["CCCCCV", "five onset"],
        "CCCCCC+ onset":["CCCCCCV", "CCCCCCV+", "six onset", "six or more onset"],
        "C coda":       ["CVC", "VC", "single coda"], # formerly CVC, not "VC"
        "CC coda":      ["VCC", "two coda"],
        "CCC coda":     ["VCCC", "three coda"],
        "CCCC coda":    ["VCCCC", "four coda"],
        "CCCCC coda":   ["VCCCCC", "five coda"],
        "CCCCCC+ coda": ["VCCCCCC", "VCCCCCC+", "six coda", "six or more coda"],
    })

    # For the Typology survey
    MORPHOLOGY = FuzzySearchTerms({
        "isolating": [],
        "analytic": ["analytic", "not isolating"], # this is a toughie
        "fusional": [],
        "agglutinating": [],
        "polysynthetic": []
    })

    WORD_FORMATION_F17 = FuzzySearchTerms({
        "affixation": ["affixation", "prefixation or suffixation"],
        "suffixation": [],
        "prefixation": [],
        "infixation": [],
        "compounding": [],
        "root-and-pattern": [],
        "internal change": [],
        "suppletion": [],
        "stress or tone shift": [],
        "reduplication": [],
        "conversion": [],
        "purely isolating": ["none", "purely isolating"]
    })

    WORD_FORMATION_S19 = FuzzySearchTerms({
        # "affixation": ["affixation", "prefixation or suffixation"], # obsolete as of s19
        "suffixation": [],
        "prefixation": [],
        "infixation": [],
        "compounding": [],
        "root-and-pattern": [],
        "internal change": [],
        "suppletion": [],
        "stress or tone shift": [],
        "reduplication": [],
        "conversion": [],
        "purely isolating": ["none", "purely isolating"]
    })

    # not thoroughly tested
    WORD_FORMATION_FREQ = FuzzySearchTerms({
        "exclusively suffixing": [],
        "mostly suffixing": [],
        "exclusively prefixing": [],
        "mostly prefixing": [],
        "equal prefixing and suffixing": ["prefixing and suffixing"],
        "exclusively non-affixal": [],
        "mostly non-affixal": [],
        "equal affixation and other": ["affixation and other"],
        "mostly isolating": [],
        "exclusively isolating": ["exclusively isolating", "purely isolating"]
    })

    # Replaced WORD_FORMATION_FREQ in F22
    AFFIXATION_FREQ = FuzzySearchTerms({
        "exclusively suffixing": [],
        "mostly suffixing": [],
        "exclusively prefixing": [],
        "mostly prefixing": [],
        "equal prefixing and suffixing": ["prefixing and suffixing"],
        "little or no affixation": ["no (or VERY little) affixation"],
    })

    # Replaced WORD_FORMATION_FREQ in F22
    NON_AFFIXATION_FREQ = FuzzySearchTerms({
        "exclusively non-affixal": ["all word-formation involves non-affixal"],
        "mostly non-affixal": ["most word-formation involves non-affixal"],
        "equal affixation and other": ["equal mix of affixation and non-affixal"],
        "mostly affixal": ["most word-formation involves affixation"],
        "no non-affixal": ['no non-affixal'],
        "mostly isolating": [],
    })

    # For backwards compatibility, let's still include a "WORD_FORMATION_FREQ" field,
    # derived from the two new survey questions.
    WORD_FORMATION_FREQ_F22 = AFFIXATION_FREQ | NON_AFFIXATION_FREQ

    # New in F22
    FUNCTIONAL_MORPHOLOGY = FuzzySearchTerms({
        "nominalizers": [],
        "verbalizers": [],
        "(in)transitivity": [],
        "associated motion": [],
        "low aspect": [],
        "voice": [],
        "natural gender": [],
        "diminutive / augmentative": [],
        "high aspect": [],
        "tense": [],
        "mood": [],
        "agreement": [],
        "number": ["number (sg, pl, dual)"],
        "grammatical gender": [],
        "definiteness": [],
        "case": [],
        "possessor marking": [],
    })

    WORD_ORDER = FuzzySearchTerms({
        "SVO": [],
        "SOV": [],
        "VSO": [],
        "VOS": [],
        "OVS": [],
        "OSV": [],
        # "multiple": ["more than one", "multiple", "several"],
        "free":     ["no basic", "none", "free"]
    })

    # not thoroughly tested
    HEADEDNESS = FuzzySearchTerms({
        "consistently head-initial": [],
        "consistently head-final": [],
        "mostly head-initial": [],
        "mostly head-final": [],
        "mixed headedness": []
    })

    CASE = FuzzySearchTerms({
        "none": ["doesn't have", "none"],
        "ergative/absolutive": [],
        "nominative/accusative": [],
        "other": ["other", "some other", "other sort"]
    })

    AGREEMENT = FuzzySearchTerms({
        "none": ["doesn't have", "none"],
        "ergative/absolutive": [],
        "nominative/accusative": [],
        "other": ["other", "some other", "other sort"]
    })

# Alias to save typing
# D for "Dict" (a historical name, since a FuzzySearchTerm is an instance of dict)
D = AllFuzzySearchTerms

################################################################################
#                           Survey Specifications
################################################################################

@dataclasses.dataclass
class SurveySpecification:
    """ A SurveySpecification specifies all the information necessary to extract
    responses to one (or many) survey questions into one (or many) JSON values. """

    json_key: Optional[JsonKey]
    """ The JSON key(s) under which the results of this survey question should be stored. """

    value_type: ValueType
    """ The data type of the JSON value(s) which will be extracted from this survey question. """

    index: Optional[Union[int, List[int]]] = None
    """ The index(es) in the survey CSV which will be extracted to fill a JSON value.
    For one-to-one mappings, this is a single int.
    For many-to-one, it is a list of ints.
    For derived values, it is None (no field in the CSV directly includes this info). """

    mapping: Optional[Mappings] = None
    """ The kind of mapping from survey questions to JSON fields
    ONE_TO_ONE: One survey question fills one JSON field.
    MERGE: Many survey questions fill one JSON field.
    SPLIT: One survey question fills many JSON fields.
    None: One or more JSON fields are derived from other data.
    """

    fuzzy_search_terms: Optional[FuzzySearchTerms] = None
    """ A mapping from candidate matches to search terms for that candidate.
    See docstring in `fuzzy_match_phrase()`. """

    poisoned_search_terms: Optional[List[SearchTerm]] = None
    """ A list of search terms which indicate a false negative if matched.
    See docstring in `fuzzy_match_phrase()`. """

# Alias to save typing:
Spec = SurveySpecification

class SurveySpecifications:
    """ A simple namespace to contain `SurveySpecification` producer functions.

    Note that these are defined as functions that take in arguments and construct
    an appropriate SurveySpecification for the given semester.

    This is useful because the survey specifications don't change much from semester
    to semester, but the order in which questions are asked might change, so it's
    handy to leave `index` as a parameter to allow easy re-ordering.

    NOTE: It's tempting to try to infer the indices automatically for a particular
        semester by inspecting the index at which a particular SurveySpecification
        appears in the list of specs for that semester. However, this is impossible.
        Some indices aren't even integers (e.g. lists of integers, or None),
        so this scheme wouldn't be flexible enough for our needs.
    """

    # Common question specifications that won't change much
    @staticmethod
    def NETID(index=1):
        # TODO: replace STRING with a new HASH type?
        return Spec(K.NETID, T.STRING, index, M.ONE_TO_ONE)

    @staticmethod
    def NAME(index=2):
        # TODO: replace STRING with a new HASH type?
        return Spec(K.NAME, T.STRING, index, M.ONE_TO_ONE)

    @staticmethod
    def LANGUAGE(index=3):
        return Spec(K.LANGUAGE, T.STRING, index, M.ONE_TO_ONE)

    @staticmethod
    def NUM_CONSONANTS(index=4):
        return Spec(K.NUM_CONSONANTS, T.NUM, index, M.ONE_TO_ONE)

    @staticmethod
    def NUM_VOWELS(index=5):
        return Spec(K.NUM_VOWELS, T.NUM, index, M.ONE_TO_ONE)

    @staticmethod
    def NUM_PHONEMES(index=6):
        return Spec(K.NUM_PHONEMES, T.NUM, index, M.ONE_TO_ONE)

    @staticmethod
    def NUM_CONSONANT_PLACES():
        return Spec(K.NUM_CONSONANT_PLACES, T.PLACEHOLDER)

    @staticmethod
    def NUM_CONSONANT_MANNERS():
        return Spec(K.NUM_CONSONANT_MANNERS, T.PLACEHOLDER)

    @staticmethod
    def PHONETIC(index=9):
        keys = None
        poisoned_search_terms = ['stress']
        return Spec(keys, T.BOOL, index, M.SPLIT, D.PHONETIC, poisoned_search_terms)

    # F22 adds "unpredictable stress"; previously only "predictable stress" was present.
    @staticmethod
    def PHONETIC_F22(index=9):
        keys = None
        poisoned_search_terms = ['stress']
        return Spec(keys, T.BOOL, index, M.SPLIT, D.PHONETIC_F22, poisoned_search_terms)

    @staticmethod
    def SYLLABLE(index=10):
        poisoned_search_terms =  ["CV", "V", "VC"]  # Should not be hardcoded, move to selectors?
        return Spec(K.SYLLABLES, T.LIST, index, M.ONE_TO_ONE, D.SYLLABLES, poisoned_search_terms)

    # New grammar questions as of F19
    @staticmethod
    def COUNTRY(index=4):
        return Spec(K.COUNTRY, T.STRING, index, M.ONE_TO_ONE)

    @staticmethod
    def LANGUAGE_FAMILY(index=5):
        return Spec(K.LANGUAGE_FAMILY, T.STRING, index, M.ONE_TO_ONE)

    # New grammar questions as of F21
    @staticmethod
    def ENDANGERMENT_LEVEL(index=6):
        # This question has an "Other" option so it's hard to catch everything a student
        # might enter. Some languages will likely go without data on this one.
        # HACK: The true type of this property is T.STRING, but defining it as a list
        #       allows me to shoehorn queries for it into the "at least k" framework
        # TODO: If I ever write a proper way to handle queries like:
        #       "has an endangerment level of at least one of the levels [5,6,7]"
        #       this should become a string again and be handled in that new way.
        return Spec(K.ENDANGERMENT_LEVEL, T.LIST, index, M.ONE_TO_ONE, D.ENDANGERMENT_LEVELS)

    # Things that will more likely change
    # Fall 17 specific data format specification
    @staticmethod
    def CONSONANTS_F17(index=7):
        return Spec(K.CONSONANTS, T.LIST, index, M.ONE_TO_ONE, PHONEMES)

    @staticmethod
    def VOWELS_F17(index=8):
        return Spec(K.VOWELS, T.LIST, index, M.ONE_TO_ONE, PHONEMES)

    # Spring 19 specific format specification
    @staticmethod
    def CONSONANTS_S19(index=(7,8)):
        return Spec(K.CONSONANTS, T.LIST, index, M.MERGE, PHONEMES)

    @staticmethod
    def VOWELS_S19(index=(9,10)):
        return Spec(K.VOWELS, T.LIST, index, M.MERGE, PHONEMES)

    @staticmethod
    def VOWEL_TYPES_S19(index=11):
        poisoned_search_terms = ["phthong", "vowel"] # Should not be hardcoded, move to selectors?
        return Spec(K.VOWEL_TYPES, T.LIST, index, M.ONE_TO_ONE, D.VOWEL_TYPES, poisoned_search_terms)

    # TODO: Add a default index value
    @staticmethod
    def CONSONANT_TYPES_F19(index):
        poisoned_search_terms = None
        return Spec(K.CONSONANT_TYPES, T.LIST, index, M.ONE_TO_ONE, D.CONSONANT_TYPES, poisoned_search_terms)

    # The possible answers changed from earlier years.
    @staticmethod
    def CONSONANT_TYPES_F21(index=12):
        # We really should match everything, so this one is very broad
        poisoned_search_terms = ['ed', 'es']
        return Spec(K.CONSONANT_TYPES, T.LIST, index, M.ONE_TO_ONE, D.CONSONANT_TYPES_F21, poisoned_search_terms)

    # The possible answers changed from earlier years.
    @staticmethod
    def CONSONANT_TYPES_F22(index=12):
        # We really should match everything, so this one is very broad
        poisoned_search_terms = ['ed', 'es']
        return Spec(K.CONSONANT_TYPES, T.LIST, index, M.ONE_TO_ONE, D.CONSONANT_TYPES_F22, poisoned_search_terms)

    # Typology Parameters Fall 17:
    @staticmethod
    def CITATION_F17(index=4):
        return Spec(K.CITATION, T.STRING, index, M.ONE_TO_ONE)

    @staticmethod
    def RECOMMEND(index=5):
        return Spec(K.RECOMMEND, T.STRING, index, M.ONE_TO_ONE)

    @staticmethod
    def MORPHOLOGICAL_TYPE(index=6):
        return Spec(K.MORPHOLOGICAL_TYPE, T.LIST, index, M.ONE_TO_ONE, D.MORPHOLOGY, None)

    @staticmethod
    def WORD_FORMATION(index=7):
        poisoned_search_terms = ["ion", "change", "root", "isolat"] # XXXat(ion), (isolat)ing
        return Spec(K.WORD_FORMATION, T.LIST, index, M.ONE_TO_ONE, D.WORD_FORMATION_F17, poisoned_search_terms)

    @staticmethod
    def WORD_FORMATION_FREQ(index=8):
        poisoned_search_terms = ["exclusive", "most", "equal", "prefix", "suffix", "affix", "isolating"]
        return Spec(K.WORD_FORMATION_FREQ, T.STRING, index, M.ONE_TO_ONE, D.WORD_FORMATION_FREQ, poisoned_search_terms)

    # Build the legacy WORD_FORMATION_FREQ field from the new affixation/non-affixation variants
    # (for backwards compatibility)
    @staticmethod
    def WORD_FORMATION_FREQ_F22(index=(7,8)):
        poisoned_search_terms = ["exclusive", "most", "equal", "prefix", "suffix", "affix", "isolat", "even mix", "none",]
        return Spec(K.WORD_FORMATION_FREQ, T.LIST, index, M.MERGE, D.WORD_FORMATION_FREQ_F22, poisoned_search_terms)

    @staticmethod
    def AFFIXATION_FREQ(index=7):
        poisoned_search_terms = ["affix", "prefix", "suffix", "even mix", "none"]
        return Spec(K.AFFIXATION_FREQ, T.STRING, index, M.ONE_TO_ONE, D.AFFIXATION_FREQ, poisoned_search_terms)

    @staticmethod
    def NON_AFFIXATION_FREQ(index=8):
        poisoned_search_terms = ["formation", "isolat", "affix"]
        return Spec(K.NON_AFFIXATION_FREQ, T.STRING, index, M.ONE_TO_ONE, D.NON_AFFIXATION_FREQ, poisoned_search_terms)

    @staticmethod
    def FUNCTIONAL_MORPHOLOGY(index=9):
        poisoned_search_terms = ["izer", "ive", "ivity", "al", "aspect"]
        return Spec(K.FUNCTIONAL_MORPHOLOGY, T.LIST, index, M.ONE_TO_ONE, D.FUNCTIONAL_MORPHOLOGY, poisoned_search_terms)

    @staticmethod
    def WORD_ORDER(index=9):
        poisoned_search_terms = ["free", "S", "V", "O"]
        return Spec(K.WORD_ORDER, T.LIST, index, M.ONE_TO_ONE, D.WORD_ORDER, poisoned_search_terms)

    @staticmethod
    def HEADEDNESS(index=10):
        poisoned_search_terms = ["head", "initial", "final", "most", "consistent", "mixed"]
        return Spec(K.HEADEDNESS, T.LIST, index, M.ONE_TO_ONE, D.HEADEDNESS, poisoned_search_terms)

    @staticmethod
    def AGREEMENT(index=11):
        return Spec(K.AGREEMENT, T.STRING, index, M.ONE_TO_ONE, D.AGREEMENT, None)

    @staticmethod
    def CASE(index=12):
        return Spec(K.CASE, T.STRING, index, M.ONE_TO_ONE, D.CASE, None)

# Alias to save typing
# P for sPecification
# (no, just kidding... it's P for Parameter, which was the historical name)
P = SurveySpecifications


################################################################################
#                   SurveySpecifications for each Semester
################################################################################

# Which questions should be read from the CSV files for a given dataset,
# and how is the data stored in the corresponding CSV?
# These specify how to convert between a CSV entry and a JSON entry
# The order in the list determines the order in which the fields will appear
# in the final JSON dataset.
# The .index property of each SurveySpecification determines the order in which
# the fields appear in the input survey CSV.
PARAMS = {
    Semesters.F17: {
        Surveys.GRAMMAR: [
            P.LANGUAGE(),
            P.NAME(),
            P.NETID(),
            P.NUM_CONSONANTS(),
            P.NUM_VOWELS(),
            P.NUM_PHONEMES(),
            P.CONSONANTS_F17(),
            P.VOWELS_F17(),
            P.NUM_CONSONANT_PLACES(),
            P.NUM_CONSONANT_MANNERS(),
            P.PHONETIC(9),
            P.SYLLABLE(10)
        ],
        Surveys.TYPOLOGY: [
            P.LANGUAGE(),
            P.NAME(),
            P.NETID(),
            P.CITATION_F17(4),
            P.RECOMMEND(5),
            P.MORPHOLOGICAL_TYPE(6),
            P.WORD_FORMATION(7),
            P.WORD_FORMATION_FREQ(8),
            P.WORD_ORDER(9),
            P.HEADEDNESS(10),
            P.AGREEMENT(11),
            P.CASE(12)
        ]
    },
    Semesters.S19: {
        Surveys.GRAMMAR: [
            P.LANGUAGE(),
            P.NAME(),
            P.NETID(),
            P.NUM_CONSONANTS(),
            P.NUM_VOWELS(),
            P.NUM_PHONEMES(),
            P.CONSONANTS_S19(),
            P.VOWELS_S19(),
            P.NUM_CONSONANT_PLACES(),
            P.NUM_CONSONANT_MANNERS(),
            P.VOWEL_TYPES_S19(),
            P.PHONETIC(12),
            P.SYLLABLE(13)
        ],
        Surveys.TYPOLOGY: [
            P.LANGUAGE(),
            P.NAME(),
            P.NETID(),
            P.RECOMMEND(4),
            P.MORPHOLOGICAL_TYPE(5),
            P.WORD_FORMATION(6),
            P.WORD_FORMATION_FREQ(7),
            P.WORD_ORDER(8),
            P.HEADEDNESS(9),
            P.AGREEMENT(10),
            P.CASE(11)
        ]
    },
    Semesters.F19: {
        Surveys.GRAMMAR: [
            P.LANGUAGE(),
            P.NAME(),
            P.NETID(),
            P.COUNTRY(4),
            P.LANGUAGE_FAMILY(5),
            P.NUM_CONSONANTS(6),
            P.NUM_VOWELS(7),
            P.NUM_PHONEMES(8),
            P.CONSONANTS_S19([9,10]),
            P.CONSONANT_TYPES_F19(11),
            P.VOWELS_S19([12,13]),
            P.VOWEL_TYPES_S19(14),
            P.NUM_CONSONANT_PLACES(),
            P.NUM_CONSONANT_MANNERS(),
            # P.PHONETIC(15), # !!!!
            P.SYLLABLE(15)
        ],
        Surveys.TYPOLOGY: [
            P.LANGUAGE(),
            P.NAME(),
            P.NETID(),
            P.RECOMMEND(4),
            P.MORPHOLOGICAL_TYPE(5),
            P.WORD_FORMATION(6),
            P.WORD_FORMATION_FREQ(7),
        ]
    },
    Semesters.F21: {
        Surveys.GRAMMAR: [
            P.LANGUAGE(),
            P.NAME(),
            P.NETID(),
            P.COUNTRY(4),
            P.LANGUAGE_FAMILY(5),
            P.ENDANGERMENT_LEVEL(6),
            P.NUM_CONSONANTS(7),
            P.NUM_VOWELS(8),
            P.NUM_PHONEMES(9),
            P.CONSONANTS_S19([10,11]),
            P.CONSONANT_TYPES_F21(12),
            P.VOWELS_S19([13,14]),
            P.VOWEL_TYPES_S19(15),
            P.NUM_CONSONANT_PLACES(),
            P.NUM_CONSONANT_MANNERS(),
            P.PHONETIC(16),
            P.SYLLABLE(17)
        ],
        Surveys.TYPOLOGY: [
            P.LANGUAGE(),
            P.NAME(),
            P.NETID(),
            P.RECOMMEND(4),
            P.MORPHOLOGICAL_TYPE(5),
            P.WORD_FORMATION(6),
            P.WORD_FORMATION_FREQ(7),
            P.WORD_ORDER(8),
            P.HEADEDNESS(9),
        ]
    },
    Semesters.F22: {
        Surveys.GRAMMAR: [
            P.LANGUAGE(),
            P.NAME(),
            P.NETID(),
            P.COUNTRY(4),
            P.LANGUAGE_FAMILY(5),
            P.ENDANGERMENT_LEVEL(6),
            P.NUM_CONSONANTS(7),
            P.NUM_VOWELS(8),
            P.NUM_PHONEMES(9),
            P.CONSONANTS_S19([10,11]),
            P.CONSONANT_TYPES_F22(12),
            P.VOWELS_S19([13,14]),
            P.VOWEL_TYPES_S19(15),
            P.NUM_CONSONANT_PLACES(),
            P.NUM_CONSONANT_MANNERS(),
            P.PHONETIC_F22(16),
            P.SYLLABLE(17),
        ],
        Surveys.TYPOLOGY: [
            P.LANGUAGE(),
            P.NAME(),
            P.NETID(),
            # P.PUBLISHER_AND_AUTHOR(4) # I don't actually have a field for this, but it's in the survey.
            P.RECOMMEND(5),
            P.MORPHOLOGICAL_TYPE(6),
            P.WORD_FORMATION(7),
            # Note: In F22, P.WORD_FORMATION_FREQ split into two.
            # We keep a modification of the original for backwards compatibility,
            # so that the "word formation frequency" field still exists.
            # We also keep the two new fields separately to support new queries.
            P.WORD_FORMATION_FREQ_F22([8,9]),
            P.AFFIXATION_FREQ(8),
            P.NON_AFFIXATION_FREQ(9),
            P.FUNCTIONAL_MORPHOLOGY(10),
            P.WORD_ORDER(11),
            P.HEADEDNESS(12),
        ]
    }
}


################################################################################
#                               CSV Formatting
################################################################################

ROW_DELIMITER = "\n"    # delimits rows (might need carriage return?)
COL_DELIMITER = ","     # delimits columns within a row
INNER_DELIMITER = ";"   # delimits lists within a column
PHONEME_DELIMITER = "/" # Used on either side of a phoneme (e.g. /d/ --> d)


################################################################################
#                         Legacy csvtojson constants
################################################################################
# In general, avoid using these constants. Use the newer parameter definitions
# above wherever possible.

# Constants across typology/grammar
NETID = 1
NAME  = 2
LANGUAGE = 3
HASH_SIZE = 16
# NOTE: 16 may be too high (not anonymous enough)
# - shorter hashes <=6 or 7 give better anonymity properties, but increase risk of
# - collisions (8 seem too high also)
# - note that anonymity is less critical than guaranteed correctness for this
# application so higher values are OK
