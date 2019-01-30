# ======================== Survey Question Data ===============================
# Each question in the survey or variable being measured should have an object
# of the following form, specifying how that question should be parsed and how
# its data should be stored.
# Fields:
# NAME: Plain english name of this trait. Currently unused
# SELECT_NAME: The text to be displayed in the <select> dropdown
#              (e.g. "Contains consonants: ")
# DICT: See below. A parseDict mapping arbitrary words in the question statement to
#       legal values of the accompanying variable. None if the trait is not list-based
# MULTI: Whether or not multiple selections are allowed. None if trait not list-based
# MODE:  (?) Maybe use this to specify if it is a "Pick K of <x, y,z>" or
#            "Simple boolean" or "Pick one"
# REPLY: A format string containing information on how the results of a query
#        for this field should be described in plain english
#        E.G. "contain at least one of %s" where %s is [p,t,k]
# REPLY_VARS:  Describes what variables are needed to fill the format string
#              E.G. a list of strings, a single string, a mode string, a k-value
# FUNCTION: A function in the language class that is used to query for this trait.
#           e.g. Language.matchConsonants
# BOOL_BODY: Some representation of what content goes in the selector div
#            Currently used only if MODE==BOOLEAN. In this case, BOOL_BODY will be the
#            string that should be included as the body of the HTML selector
# HTML_ID: A string like "syllable selector" used to represent the class and type
#          attribute of HTML elements responsible for handling this trait.
# POPOVER_PREFIX: A string like "h-lbox-selector" used as the class for tables
#                 and cells generated for popovers related to this trait.
# SELECT_WHAT: A string like "phonemes" used in the header of popovers to indicate
#              what the general type of "thing" being selected actually is.


# Format for the DICT: entries...
# Dictionaries for use in csvtojson.parsePhrase()
# Generally speaking, the format is:
# The keys in the dict (left side) are the values you would like to store in the json
# The values in the lists (right side) are the values in the raw data you would like to
# be replaced by the key on the left
# If the right-hand-side list is [], it is treated as the left-hand-side string itself

from phonemes import metaclasses
from lingdb.language import Language

# Dictionary keys
NAME            = "name"
DICT            = "dict"
MULTI           = "multi"
MODE            = "mode"
BOOL_BODY       = "bool body"
REPLY           = "reply"
REPLY_VARS      = "reply vars"
FUNCTION        = "function"
HTML_ID         = "html id"
POPOVER_PREFIX  = "popover prefix"
SELECT_WHAT     = "select what"
SELECT_NAME     = "select name"

# Valid modes
# TODO: Change these names to make sense
PICK_ONE    = "pick one"    # lbox (multi = false)
PICK_CLASS  = "pick class"  # clboxes
PICK_MULTI  = "pick multi"  # lbox (multi = true)
PICK_K      = "pick k"      # pboxes
PICK_K_IPA  = "pick k ipa"  # ipaboxes (displayed inline, not as popover)
BOOLEAN     = "boolean"     # no boxes (true/false only)
NO_QUERY    = "no query"    # placeholder (cannot be submitted as query)

# ===============================
# ========== SELECTORS ==========

# Note: things will misbehave if FUNCTION, MODE not provided
# (even if it seems like they aren't needed, e.g. for placeholder)

# The dummy "selector" that is displayed by default if none are selected
PLACEHOLDER = {
    SELECT_NAME: "Select trait...",
    MODE: NO_QUERY,
    FUNCTION: None,
    HTML_ID: "placeholder-selector",
    BOOL_BODY: "Select a trait from the dropdown menu to start submitting queries!"
}

CONSONANT = {
    SELECT_NAME: "Contains consonant:",
    DICT: None,
    MULTI: None,
    MODE: PICK_K,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchConsonants,
    HTML_ID: "consonant-selector",
    POPOVER_PREFIX: "cbox-popover",
    SELECT_WHAT: "consonants"
}

IPA_CONSONANT = {
    SELECT_NAME: "Contains consonant:",
    DICT: None,
    MULTI: None,
    MODE: PICK_K_IPA,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchConsonants,
    HTML_ID: "ipa-consonant-selector",
    POPOVER_PREFIX: "ipacbox-popover",
    SELECT_WHAT: "consonants"
}

CONSONANT_CLASS = {
    SELECT_NAME: "Contains consonant class:",
    DICT: None,
    MULTI: None,
    MODE: PICK_CLASS,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchConsonantClasses,
    HTML_ID: "consonant-class-selector",
    POPOVER_PREFIX: "ccbox-popover",
    SELECT_WHAT: "natural classes"
}

VOWEL = {
    SELECT_NAME: "Contains vowel:",
    DICT: None,
    MULTI: None,
    MODE: PICK_K,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchVowels,
    HTML_ID: "vowel-selector",
    POPOVER_PREFIX: "vbox-popover",
    SELECT_WHAT: "vowels"
}

IPA_VOWEL = {
    SELECT_NAME: "Contains vowel:",
    DICT: None,
    MULTI: None,
    MODE: PICK_K_IPA,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchVowels,
    HTML_ID: "ipa-vowel-selector",
    POPOVER_PREFIX: "ipavbox-popover",
    SELECT_WHAT: "vowels"
}

VOWEL_CLASS = {
    SELECT_NAME: "Contains vowel class:",
    DICT: None,
    MULTI: None,
    MODE: PICK_CLASS,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchVowelClasses,
    HTML_ID: "vowel-class-selector",
    POPOVER_PREFIX: "vcbox-popover",
    SELECT_WHAT: "natural classes",
}

CONSONANT_PLACES = {
    SELECT_NAME: "Has 3+ consonant places",
    DICT: None,
    MULTI: None,
    MODE: BOOLEAN,
    BOOL_BODY: "3+ Places of Consonant Articulation",
    REPLY: "contain 3+ places of consonant articulation",
    REPLY_VARS: None,
    FUNCTION: Language.containsConsonantPlaces,
    HTML_ID: "consonant-places-selector",
    POPOVER_PREFIX: None,
    SELECT_WHAT: None
}

CONSONANT_MANNERS = {
    SELECT_NAME: "Has 2+ consonant manners",
    DICT: None,
    MULTI: None,
    MODE: BOOLEAN,
    BOOL_BODY: "2+ Manners of Consonant Articulation",
    REPLY: "contain 2+ manners of consonant articulation",
    REPLY_VARS: None,
    FUNCTION: Language.containsConsonantManners,
    HTML_ID: "consonant-manners-selector",
    POPOVER_PREFIX: None,
    SELECT_WHAT: None
}

CONSONANT_ARTICULATION = {
    SELECT_NAME: "Has articulation features:",
    DICT: { "places": [], "manners": [] },
    MULTI: False,
    MODE: PICK_MULTI, # this is a hack - really really need to change all the MODEs
    REPLY: "contain %s %s %s of consonant articulation",
    REPLY_VARS: ["mode", "k", "sel"], # not selList
    FUNCTION: Language.matchConsonantArticulation,
    HTML_ID: "consonant-articulation-selector",
    POPOVER_PREFIX: "ca-lbox-popover",
    SELECT_WHAT: "articulation type"
}

COMPLEX_CONSONANTS = {
    SELECT_NAME: "Has complex consonants",
    DICT: None,
    MULTI: None,
    MODE: BOOLEAN,
    BOOL_BODY: "Complex Consonants",
    REPLY: "contain complex consonants",
    REPLY_VARS: None,
    FUNCTION: Language.containsComplexConsonants,
    HTML_ID: "complex-consonants-selector",
    POPOVER_PREFIX: None,
    SELECT_WHAT: None
}

TONE = {
    SELECT_NAME: "Has tone",
    DICT: None,
    MULTI: None,
    MODE: BOOLEAN,
    BOOL_BODY: 'Tone (Including "Pitch Accent")',
    REPLY: "have tone",
    REPLY_VARS: None,
    FUNCTION: Language.containsComplexConsonants,
    HTML_ID: "tone-selector",
    POPOVER_PREFIX: None,
    SELECT_WHAT: None
}

STRESS = {
    SELECT_NAME: "Has stress",
    DICT: None,
    MULTI: None,
    MODE: BOOLEAN,
    BOOL_BODY: "Predictable Stress",
    REPLY: "have stress",
    REPLY_VARS: None,
    FUNCTION: Language.containsStress,
    HTML_ID: "stress-selector",
    POPOVER_PREFIX: None,
    SELECT_WHAT: None
}

SYLLABLE = {
    SELECT_NAME: "Allows syllable structure:",
    DICT: {
        "V":            ["V"],
        "C onset":      ["CV"],
        "CC onset":     ["CCV"],
        "CCC onset":    ["CCCV"],
        "CCCC onset":   ["CCCCV"],
        "C coda":       ["CVC", "VC"], # formerly CVC, not "VC"
        "CC coda":      ["VCC"],
        "CCC coda":     ["VCCC"],
        "CCCC coda":    ["VCCCC"]
    },
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "use %s %s of the syllable structures %s",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchSyllable,
    HTML_ID: "syllable-selector",
    POPOVER_PREFIX: "s-lbox-popover",
    SELECT_WHAT: "syllables"
}

MORPHOLOGY = {
    SELECT_NAME: "Morphological type:",
    DICT: {
        "isolating": [],
        "analytic": ["analytic", "not isolating"], # this is a toughie
        "fusional": [],
        "agglutinating": [],
        "polysynthetic": []
    },
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "use %s %s of the morphological types %s",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchMorphologicalType,
    HTML_ID: "morphological-selector",
    POPOVER_PREFIX: "m-lbox-popover",
    SELECT_WHAT: "morphological type"
}

WORD_FORMATION = {
    SELECT_NAME: "Word formation strategy:",
    DICT: {
        "affixation": ["affixation", "prefixation or suffixation"],
        "suffixation": [],
        "prefixation": [],
        "infixation": [],
        "compounding": [],
        "root-and-pattern": [],
        "internal change": [],
        "suppleton": [],
        "stress or tone shift": [],
        "reduplication": [],
        "conversion": [],
        "purely isolating": ["none", "purely isolating"]
    },
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "use %s %s of %s to form words",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchWordFormation,
    HTML_ID: "word-formation-selector",
    POPOVER_PREFIX: "wf-lbox-popover",
    SELECT_WHAT: "word formation"
}

# The following two dicts are not meant for use as selectors. They are for
# parsePhrase only
FORMATION_FREQ = {
    DICT: {
        "exclusively" : ["exclusive", "purely"],
        "mostly": ["mostly"],
        "equal": ["equal ","even ","mix "]
    },
    MULTI: False
}

FORMATION_MODE = {
    DICT: {
        "prefixing and suffixing":  ["prefixing and suffixing"],
        "affixation and other":     ["affixation and other"],
        "suffixing":                ["suffixing"],
        "prefixing":                ["prefixing"],
        "non-affixal":              ["non-affixal"],
        "isolating":                ["isolating"]
    },
    MULTI: False
}

# The following dict is not tested for parsePhrase. It is simply a collection
# of all legal combinations of the corresponding freq/mode dicts
FORMATION = {
    SELECT_NAME: "Word formation frequency:",
    DICT: {
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
    },
    MULTI: False,
    MODE: PICK_ONE,
    REPLY: "use %s strategies to form words",
    REPLY_VARS: ["sel"],
    FUNCTION: Language.hasFormationFreq,
    HTML_ID: "formation-freq-selector",
    POPOVER_PREFIX: "ff-lbox-popover",
    SELECT_WHAT: "frequency"
}

WORD_ORDER = {
    SELECT_NAME: "Basic word order:",
    DICT: {
        "SVO": [],
        "SOV": [],
        "VSO": [],
        "VOS": [],
        "OVS": [],
        "OSV": [],
        # "multiple": ["more than one", "multiple", "several"],
        "free":     ["no basic", "none", "free"]
    },
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "have %s %s of %s word orders",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchWordOrder,
    HTML_ID: "word-order-selector",
    POPOVER_PREFIX: "wo-lbox-popover",
    SELECT_WHAT: "word order"
}

# The following two dicts are not meant for use as selectors. They are for
# parsePhrase only
HEADEDNESS_FREQ = {
    DICT: {
        "consistently": [],
        "mostly": [],
        "mixed": ["mixed", "equal", "roughly equal"]
    },
    MULTI: False
}

HEADEDNESS_MODE = {
    DICT: {
        "head-initial": [],
        "head-final": [],
        "headedness": ["mixed", "equal", "roughly equal"]
    },
    MULTI: False
}

# The following dict is not tested for parsePhrase. It is simply a collection
# of all legal combinations of the corresponding freq/mode dicts
HEADEDNESS = {
    SELECT_NAME: "Headedness:",
    DICT: {
        "consistently head-initial": [],
        "consistently head-final": [],
        "mostly head-initial": [],
        "mostly head-final": [],
        "mixed headedness": []
    },
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "are %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchHeadedness,
    HTML_ID: "headedness-selector",
    POPOVER_PREFIX: "h-lbox-popover",
    SELECT_WHAT: "headedness"
}

CASE = {
    SELECT_NAME: "Case:",
    DICT: {
        "none": ["doesn't have", "none"],
        "ergative/absolutive": [],
        "nominative/accusative": [],
        "other": ["other", "some other", "other sort"]
    },
    MULTI: False,
    MODE: PICK_ONE,
    REPLY: "have %s case",
    REPLY_VARS: ["sel"],
    FUNCTION: Language.hasCase,
    HTML_ID: "case-selector",
    POPOVER_PREFIX: "c-lbox-popover",
    SELECT_WHAT: "case"
}

AGREEMENT = {
    SELECT_NAME: "Agreement:",
    DICT: {
        "none": ["doesn't have", "none"],
        "ergative/absolutive": [],
        "nominative/accusative": [],
        "other": ["other", "some other", "other sort"]
    },
    MULTI: False,
    MODE: PICK_ONE,
    REPLY: "have %s agreement",
    REPLY_VARS: ["sel"],
    FUNCTION: Language.hasAgreement,
    HTML_ID: "agreement-selector",
    POPOVER_PREFIX: "a-lbox-popover",
    SELECT_WHAT: "agreement"
}

METACLASS = {
    SELECT_NAME: "Contains metaclass:",
    DICT: metaclasses.DICT,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "have %s %s phoneme that is %s",
    REPLY_VARS: ["mode", "k", "selList"],
    FUNCTION: Language.matchMetaclasses,
    HTML_ID: "metaclass-selector",
    POPOVER_PREFIX: "mc-lbox-popover",
    SELECT_WHAT: "metaclasses"
}

# The order of this list determines the order in which traits will appear in the
# selector dropdown on the site.
SELECTORS = [
    PLACEHOLDER,
    IPA_CONSONANT,
    IPA_VOWEL,
    # CONSONANT,
    # VOWEL,
    METACLASS,
    CONSONANT_CLASS,
    VOWEL_CLASS,
    CONSONANT_ARTICULATION,
    #CONSONANT_PLACES,
    #CONSONANT_MANNERS,
    COMPLEX_CONSONANTS,
    TONE,
    STRESS,
    SYLLABLE,
    MORPHOLOGY,
    WORD_FORMATION,
    FORMATION,
    WORD_ORDER,
    HEADEDNESS,
    CASE,
    AGREEMENT
]

SELECTORS_DICT = { sel[HTML_ID] : sel for sel in SELECTORS }

# function mappings used by lingdb_client.handleQuery()
function_map = { sel[HTML_ID]: sel[FUNCTION] for sel in SELECTORS }
