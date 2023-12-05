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
#              E.G. a list of strings, a single ValueType.STRING, a mode ValueType.STRING, a k-value
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
# PROPERTY: The property of the language to run DB queries against
# TYPE: The type of Query() object to construct

# Format for the DICT: entries...
# Dictionaries for use in csvtojson.parsePhrase()
# Generally speaking, the format is:
# The keys in the dict (left side) are the values you would like to store in the json
# The values in the lists (right side) are the values in the raw data you would like to
# be replaced by the key on the left
# If the right-hand-side list is [], it is treated as the left-hand-side string itself

from phonemes import metaclasses
# from lingdb.language import Language
from .const import (
    D,
    JsonKey,
    ValueType,
)

# Dictionary keys
NAME            = "name"
DICT            = "dict"
MULTI           = "multi"
MODE            = "mode"
BOOL_BODY       = "bool body"
REPLY           = "reply"
REPLY_VARS      = "reply vars"
FUNCTION        = "function"   # deprecated
HTML_ID         = "html id"
POPOVER_PREFIX  = "popover prefix"
SELECT_WHAT     = "select what"
SELECT_NAME     = "select name"
PROPERTY        = "property"        # As required for Query() objects
TYPE            = "type"            # To determine the type of Query() object

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

ENDANGERMENT = {
    SELECT_NAME: "Endangerment level:",
    DICT: D.ENDANGERMENT_LEVELS,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "have an endangerment level that matches %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "endangerment-selector",
    POPOVER_PREFIX: "ebox-popover",
    SELECT_WHAT: "endangerment level",
    PROPERTY: JsonKey.ENDANGERMENT_LEVEL.value,
    TYPE: ValueType.LIST.value,
}

CONSONANT = {
    SELECT_NAME: "Contains consonant:",
    DICT: None,
    MULTI: None,
    MODE: PICK_K,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "consonant-selector",
    POPOVER_PREFIX: "cbox-popover",
    SELECT_WHAT: "consonants",
    PROPERTY: JsonKey.CONSONANTS.value,
    TYPE: ValueType.LIST.value,
}

IPA_CONSONANT = {
    SELECT_NAME: "Contains consonant:",
    DICT: None,
    MULTI: None,
    MODE: PICK_K_IPA,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "ipa-consonant-selector",
    POPOVER_PREFIX: "ipacbox-popover",
    SELECT_WHAT: "consonants",
    PROPERTY: JsonKey.CONSONANTS.value,
    TYPE: ValueType.LIST.value,
}

CONSONANT_CLASS = {
    SELECT_NAME: "Contains consonant class:",
    DICT: None,
    MULTI: None,
    MODE: PICK_CLASS,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "consonant-class-selector",
    POPOVER_PREFIX: "ccbox-popover",
    SELECT_WHAT: "natural classes",
    PROPERTY: JsonKey.CONSONANTS.value,
    TYPE: ValueType.LIST.value,
}

VOWEL = {
    SELECT_NAME: "Contains vowel:",
    DICT: None,
    MULTI: None,
    MODE: PICK_K,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "vowel-selector",
    POPOVER_PREFIX: "vbox-popover",
    SELECT_WHAT: "vowels",
    PROPERTY: JsonKey.VOWELS.value,
    TYPE: ValueType.LIST.value,
}

IPA_VOWEL = {
    SELECT_NAME: "Contains vowel:",
    DICT: None,
    MULTI: None,
    MODE: PICK_K_IPA,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "ipa-vowel-selector",
    POPOVER_PREFIX: "ipavbox-popover",
    SELECT_WHAT: "vowels",
    PROPERTY: JsonKey.VOWELS.value,
    TYPE: ValueType.LIST.value,
}

VOWEL_CLASS = {
    SELECT_NAME: "Contains vowel class:",
    DICT: None,
    MULTI: None,
    MODE: PICK_CLASS,
    REPLY: "contain %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "vowel-class-selector",
    POPOVER_PREFIX: "vcbox-popover",
    SELECT_WHAT: "natural classes",
    PROPERTY: JsonKey.VOWELS.value,
    TYPE: ValueType.LIST.value,
}

CONSONANT_PLACES = {
    SELECT_NAME: "Has 3+ consonant places",
    DICT: None,
    MULTI: None,
    MODE: BOOLEAN,
    BOOL_BODY: "3+ Places of Consonant Articulation",
    REPLY: "contain 3+ places of consonant articulation",
    REPLY_VARS: None,
    HTML_ID: "consonant-places-selector",
    POPOVER_PREFIX: None,
    SELECT_WHAT: None,
    PROPERTY: JsonKey.HAS_3_PLUS_PLACES.value,
    TYPE: ValueType.BOOL.value,
}

CONSONANT_MANNERS = {
    SELECT_NAME: "Has 2+ consonant manners",
    DICT: None,
    MULTI: None,
    MODE: BOOLEAN,
    BOOL_BODY: "2+ Manners of Consonant Articulation",
    REPLY: "contain 2+ manners of consonant articulation",
    REPLY_VARS: None,
    HTML_ID: "consonant-manners-selector",
    POPOVER_PREFIX: None,
    SELECT_WHAT: None,
    PROPERTY: JsonKey.HAS_2_PLUS_MANNERS.value,
    TYPE: ValueType.BOOL.value,
}

CONSONANT_ARTICULATION = {
    SELECT_NAME: "Has articulation features:",
    DICT: { "places": [], "manners": [] },
    MULTI: False,
    MODE: PICK_MULTI, # this is a hack - really really need to change all the MODEs
    REPLY: "contain %s %s %s of consonant articulation",
    REPLY_VARS: ["mode", "k", "sel"], # not selList
    HTML_ID: "consonant-articulation-selector",
    POPOVER_PREFIX: "ca-lbox-popover",
    SELECT_WHAT: "articulation type",
    PROPERTY: "num consonant {value}", # WARNING: This is not currently supported - need some way to decide which to query
    TYPE: ValueType.NUM.value,
}

VOWEL_TYPES = {
    SELECT_NAME: "Vowel types:",
    DICT: D.VOWEL_TYPES,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "have %s %s of %s vowels",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "vowel-type-selector",
    POPOVER_PREFIX: "vt-lbox-popover",
    SELECT_WHAT: "vowel type",
    PROPERTY: JsonKey.VOWEL_TYPES.value,
    TYPE: ValueType.LIST.value,
}

CONSONANT_TYPES = {
    SELECT_NAME: "Consonant types:",
    DICT: D.CONSONANT_TYPES,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "have %s %s of %s consonants",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "consonant-type-selector",
    POPOVER_PREFIX: "ct-lbox-popover",
    SELECT_WHAT: "consonant type",
    PROPERTY: JsonKey.CONSONANT_TYPES.value,
    TYPE: ValueType.LIST.value,
}

CONSONANT_TYPES_F21 = {
    SELECT_NAME: "Consonant types:",
    DICT: D.CONSONANT_TYPES_F21,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "have %s %s of %s consonants",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "consonant-type-selector",
    POPOVER_PREFIX: "ct-lbox-popover",
    SELECT_WHAT: "consonant type",
    PROPERTY: JsonKey.CONSONANT_TYPES.value,
    TYPE: ValueType.LIST.value,
}

CONSONANT_TYPES_F22 = {
    SELECT_NAME: "Consonant types:",
    DICT: D.CONSONANT_TYPES_F22,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "have %s %s of %s consonants",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "consonant-type-selector",
    POPOVER_PREFIX: "ct-lbox-popover",
    SELECT_WHAT: "consonant type",
    PROPERTY: JsonKey.CONSONANT_TYPES.value,
    TYPE: ValueType.LIST.value,
}

PHONEME_INVENTORY_SIZE = {
    SELECT_NAME: "Phoneme inventory size:",
    DICT: { "consonants": [], "vowels": [], "phonemes": [] },
    MULTI: False,
    MODE: PICK_MULTI, # this is a hack - really really need to change all the MODEs
    REPLY: "have a phoneme inventory with %s %s %s",
    REPLY_VARS: ["mode", "k", "sel"], # not selList
    HTML_ID: "phoneme-inventory-size-selector",
    POPOVER_PREFIX: "pi-lbox-popover",
    SELECT_WHAT: "phoneme type",
    PROPERTY: "num {value}", # WARNING: This is not currently supported - need some way to decide which to query
    TYPE: ValueType.NUM.value,
}

COMPLEX_CONSONANTS = {
    SELECT_NAME: "Has complex consonants",
    DICT: None,
    MULTI: None,
    MODE: BOOLEAN,
    BOOL_BODY: "Complex Consonants",
    REPLY: "contain complex consonants",
    REPLY_VARS: None,
    HTML_ID: "complex-consonants-selector",
    POPOVER_PREFIX: None,
    SELECT_WHAT: None,
    PROPERTY: JsonKey.COMPLEX_CONSONANTS.value,
    TYPE: ValueType.BOOL.value,
}

TONE = {
    SELECT_NAME: "Has tone",
    DICT: None,
    MULTI: None,
    MODE: BOOLEAN,
    BOOL_BODY: 'Tone (Including "Pitch Accent")',
    REPLY: "have tone",
    REPLY_VARS: None,
    HTML_ID: "tone-selector",
    POPOVER_PREFIX: None,
    SELECT_WHAT: None,
    PROPERTY: JsonKey.TONE.value,
    TYPE: ValueType.BOOL.value,
}

STRESS = {
    SELECT_NAME: "Has stress",
    DICT: None,
    MULTI: None,
    MODE: BOOLEAN,
    BOOL_BODY: "Predictable Stress",
    REPLY: "have stress",
    REPLY_VARS: None,
    HTML_ID: "stress-selector",
    POPOVER_PREFIX: None,
    SELECT_WHAT: None,
    PROPERTY: JsonKey.STRESS.value,
    TYPE: ValueType.BOOL.value,
}

STRESS_F22 = {
    SELECT_NAME: "Has stress:",
    DICT: {'some': [], 'predictable': [], 'unpredictable': []},
    MULTI: False,
    MODE: PICK_ONE,
    REPLY: "have %s stress",
    REPLY_VARS: ["sel"],
    HTML_ID: "stress-selector",
    POPOVER_PREFIX: "ss-lbox-popover",
    SELECT_WHAT: "predictability",
    # HACK: This is a total hack; nobody else does this.
    # This is a dict mapping from the dropdown item that the user has selected
    # to the property that should be queried in that case.
    PROPERTY: {
        'some': JsonKey.STRESS.value,
        'predictable': JsonKey.PREDICTABLE_STRESS.value,
        'unpredictable': JsonKey.UNPREDICTABLE_STRESS.value,
    },
    TYPE: ValueType.BOOL.value,
}

SYLLABLES = {
    SELECT_NAME: "Allows syllable structure:",
    DICT: D.SYLLABLES,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "use %s %s of the syllable structures %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "syllable-selector",
    POPOVER_PREFIX: "s-lbox-popover",
    SELECT_WHAT: "syllables",
    PROPERTY: JsonKey.SYLLABLES.value,
    TYPE: ValueType.LIST.value,
}

MORPHOLOGY = {
    SELECT_NAME: "Morphological type:",
    DICT: D.MORPHOLOGY,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "use %s %s of the morphological types %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "morphological-selector",
    POPOVER_PREFIX: "m-lbox-popover",
    SELECT_WHAT: "morphological type",
    PROPERTY: JsonKey.MORPHOLOGICAL_TYPE.value,
    TYPE: ValueType.LIST.value,
}

WORD_FORMATION = {
    SELECT_NAME: "Word formation strategy:",
    DICT: D.WORD_FORMATION_S19,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "use %s %s of %s to form words",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "word-formation-selector",
    POPOVER_PREFIX: "wf-lbox-popover",
    SELECT_WHAT: "word formation",
    PROPERTY: JsonKey.WORD_FORMATION.value,
    TYPE: ValueType.LIST.value,
}

WORD_FORMATION_FREQ = {
    SELECT_NAME: "Word formation frequency:",
    DICT: D.WORD_FORMATION_FREQ,
    MULTI: False,
    MODE: PICK_ONE,
    REPLY: "use %s strategies to form words",
    REPLY_VARS: ["sel"],
    HTML_ID: "formation-freq-selector",
    POPOVER_PREFIX: "ff-lbox-popover",
    SELECT_WHAT: "frequency",
    PROPERTY: JsonKey.WORD_FORMATION_FREQ.value,
    TYPE: ValueType.STRING.value,
}

# New in F22, replacing WORD_FORMATION_FREQ
AFFIXATION_FREQ = {
    SELECT_NAME: "Affixation frequency:",
    DICT: D.AFFIXATION_FREQ,
    MULTI: False,
    MODE: PICK_ONE,
    REPLY: "use %s to form words",
    REPLY_VARS: ["sel"],
    HTML_ID: "affixal-freq-selector",
    POPOVER_PREFIX: "af-lbox-popover",
    SELECT_WHAT: "frequency",
    PROPERTY: JsonKey.AFFIXATION_FREQ.value,
    TYPE: ValueType.STRING.value,
}

# New in F22, replacing WORD_FORMATION_FREQ
NON_AFFIXATION_FREQ = {
    # This is the same SELECT_NAME as WORD_FORMATION_FREQ, but the two are different.
    SELECT_NAME: "Word formation frequency:",
    DICT: D.NON_AFFIXATION_FREQ,
    MULTI: False,
    MODE: PICK_ONE,
    REPLY: "use %s strategies to form words",
    REPLY_VARS: ["sel"],
    HTML_ID: "nonaffixal-freq-selector",
    POPOVER_PREFIX: "nf-lbox-popover",
    SELECT_WHAT: "frequency",
    PROPERTY: JsonKey.NON_AFFIXATION_FREQ.value,
    TYPE: ValueType.STRING.value,
}

# New in F22
FUNCTIONAL_MORPHOLOGY = {
    SELECT_NAME: "Functional morphology:",
    DICT: D.FUNCTIONAL_MORPHOLOGY,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "use %s %s of the following functional morphologies: %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "functional-morphology-selector",
    POPOVER_PREFIX: "fm-lbox-popover",
    SELECT_WHAT: "morphology",
    PROPERTY: JsonKey.FUNCTIONAL_MORPHOLOGY.value,
    TYPE: ValueType.LIST.value,
}

# Significant changes to the possible options in F23
FUNCTIONAL_MORPHOLOGY_F23 = {
    SELECT_NAME: "Functional morphology:",
    DICT: D.FUNCTIONAL_MORPHOLOGY_F23,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "use %s %s of the following functional morphologies: %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "functional-morphology-selector",
    POPOVER_PREFIX: "fm-lbox-popover",
    SELECT_WHAT: "morphology",
    PROPERTY: JsonKey.FUNCTIONAL_MORPHOLOGY.value,
    TYPE: ValueType.LIST.value,
}

WORD_ORDER = {
    SELECT_NAME: "Basic word order:",
    DICT: D.WORD_ORDER,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "have %s %s of %s word orders",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "word-order-selector",
    POPOVER_PREFIX: "wo-lbox-popover",
    SELECT_WHAT: "word order",
    PROPERTY: JsonKey.WORD_ORDER.value,
    TYPE: ValueType.LIST.value,
}

# The following two dicts are now deprecated. Remove once sure not needed
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
    DICT: D.HEADEDNESS,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "are %s %s of %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "headedness-selector",
    POPOVER_PREFIX: "h-lbox-popover",
    SELECT_WHAT: "headedness",
    PROPERTY: JsonKey.HEADEDNESS.value,
    TYPE: ValueType.LIST.value,
}

CASE = {
    SELECT_NAME: "Case:",
    DICT: D.CASE,
    MULTI: False,
    MODE: PICK_ONE,
    REPLY: "have %s case",
    REPLY_VARS: ["sel"],
    HTML_ID: "case-selector",
    POPOVER_PREFIX: "c-lbox-popover",
    SELECT_WHAT: "case",
    PROPERTY: JsonKey.CASE.value,
    TYPE: ValueType.STRING.value,
}

AGREEMENT = {
    SELECT_NAME: "Agreement:",
    DICT: D.AGREEMENT,
    MULTI: False,
    MODE: PICK_ONE,
    REPLY: "have %s agreement",
    REPLY_VARS: ["sel"],
    HTML_ID: "agreement-selector",
    POPOVER_PREFIX: "a-lbox-popover",
    SELECT_WHAT: "agreement",
    PROPERTY: JsonKey.AGREEMENT.value,
    TYPE: ValueType.STRING.value,
}

METACLASS = {
    SELECT_NAME: "Contains metaclass:",
    DICT: metaclasses.DICT,
    MULTI: True,
    MODE: PICK_MULTI,
    REPLY: "have %s %s phoneme that is %s",
    REPLY_VARS: ["mode", "k", "selList"],
    HTML_ID: "metaclass-selector",
    POPOVER_PREFIX: "mc-lbox-popover",
    SELECT_WHAT: "metaclasses",
    PROPERTY: [JsonKey.CONSONANTS.value, JsonKey.VOWELS.value], # TODO: This is an inferred type and can't be used normally
    TYPE: ValueType.LIST.value,
}

# The order of this list determines the order in which traits will appear in the
# selector dropdown on the site.
SELECTORS = [
    PLACEHOLDER,
    ENDANGERMENT,
    IPA_CONSONANT,
    IPA_VOWEL,
    # CONSONANT,  # replaced by IPA_CONSONANT
    # VOWEL,      # replaced by IPA_VOWEL
    METACLASS,
    CONSONANT_CLASS,
    VOWEL_CLASS,
    CONSONANT_ARTICULATION,
    VOWEL_TYPES,
    #CONSONANT_TYPES,     # replaced in F21
    #CONSONANT_TYPES_F21, # expanded in F22
    CONSONANT_TYPES_F22,
    #CONSONANT_PLACES,    # replaced by CONSONANT_ARTICULATION
    #CONSONANT_MANNERS,   # replaced by CONSONANT_ARTICULATION
    PHONEME_INVENTORY_SIZE,
    COMPLEX_CONSONANTS,   # not used in F19
    TONE,                 # not used in F19
    # STRESS,             # not used in F19, expanded in F22
    STRESS_F22,
    SYLLABLES,
    MORPHOLOGY,
    WORD_FORMATION,
    # WORD_FORMATION_FREQ,    # replaced in F22 by AFFIXATION_FREQ, NON_AFFIXATION_FREQ
    AFFIXATION_FREQ,
    NON_AFFIXATION_FREQ,
    # FUNCTIONAL_MORPHOLOGY,
    FUNCTIONAL_MORPHOLOGY_F23,
    WORD_ORDER,   # not used in F19
    HEADEDNESS,   # not used in F19
    # CASE,         # not used in F19, F21
    # AGREEMENT     # not used in F19, F21
]

SELECTORS_DICT = { sel[HTML_ID] : sel for sel in SELECTORS }

# function mappings used by lingdb_client.handleQuery()
# function_map = { sel[HTML_ID]: sel[FUNCTION] for sel in SELECTORS }
