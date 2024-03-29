""" The metaclasses module has nothing to do with metaclasses in the Python sense.
In hindsight, this was a terrible name.

We use "metaclasses" to refer to higher-order groupings of phonemes.
The idea is closely related to the linguistics concept of "natural classes",
though we don't (necessarily) stick to the linguistically rigorous definition.
"""

from . import consonants, vowels, phonemes, utils

# ref. https://en.wikipedia.org/wiki/Distinctive_feature
# ref. https://gawron.sdsu.edu/intro/course_core/lectures/phonology.htm
# ref. https://en.wikipedia.org/wiki/Place_of_articulation
# ref. https://essentialsoflinguistics.pressbooks.com/chapter/4-5-natural-classes/

PHONEMES    = phonemes.GLYPHS
VOWELS      = vowels.GLYPHS
CONSONANTS  = consonants.GLYPHS

# Unsure what these are
COMPLEX_CONSONANTS = []

# A superset of sibiliants incl. s, z, ʃ, ʒ, tʃ, dʒ + f, v
STRIDENTS = []

# A subset of stridents incl. s, z, ʃ, ʒ, tʃ, dʒ
SIBILANTS = []

# ====== Place-based classes ========
# ---- Basic places ----
GLOTTALS = consonants.getGlyphsMatching("place", "glottal")

# ---- Complex places ----
# A category including bilabials and labiodentals
LABIALS = []

CORONALS = []

# ====== Manner-based classes =======
# ---- Basic manners ----
NASALS                  = consonants.getGlyphsMatching("manner", "nasal")
LATERAL_APPROXIMANTS    = consonants.getGlyphsMatching("manner", "lateral approximant")
FRICATIVES              = consonants.getGlyphsMatching("manner", "fricative")

# ---- Complex manners ----
# https://en.wikipedia.org/wiki/Rhotic_consonant
RHOTICS = ["r", "ɾ", "ɹ", "ɻ", "ʀ", "ʁ", "ɽ", "ɺ"]

# https://en.wikipedia.org/wiki/Liquid_consonant
LIQUIDS = utils.unique(RHOTICS + LATERAL_APPROXIMANTS)

# https://en.wikipedia.org/wiki/Semivowel
GLIDES = ["j", "ɥ", "ɰ", "w"]

APPROXIMANTS = utils.unique(LATERAL_APPROXIMANTS + RHOTICS + GLIDES)

# ====== Other classes ========
# https://gawron.sdsu.edu/intro/course_core/lectures/phonology.htm
VOICED      = phonemes.getGlyphsMatching("voicing", "voiced")
VOICELESS   = phonemes.getGlyphsMatching("voicing", "voiceless")

SONORANTS   = utils.unique(VOWELS + GLIDES + LIQUIDS + NASALS)
OBSTRUENTS  = utils.subtract(PHONEMES, SONORANTS)

VOCALIC         = utils.unique(VOWELS + GLIDES + GLOTTALS)
CONSONANTALS    = utils.subtract(PHONEMES, VOCALIC)

# The syllabic / nonsyllabic boundary is language specific and not standard.
# Therefore this class is very misleading - maybe it should be removed
SYLLABIC    = utils.unique(VOWELS + LIQUIDS + NASALS)
NONSYLLABIC = utils.subtract(PHONEMES, SYLLABIC)

# NOTE: The continuant / occlusive boundary is disputed
# https://en.wikipedia.org/wiki/Continuant
# https://en.wikipedia.org/wiki/Occlusive
CONTINUANTS = utils.unique(FRICATIVES + VOWELS + APPROXIMANTS)
OCCLUSIVES  = utils.subtract(PHONEMES, CONTINUANTS)

# Dict containing all the lists above
DICT = {
       #"complex consonant":     COMPLEX_CONSONANTS,
       #"stridents":             STRIDENTS,
       #"sibilant":              SIBILANTS,

       # liquids + rhotics
       #"labial":                LABIALS,
       #"coronal":               CORONALS,

        "voiced":               VOICED,
        "voiceless":            VOICELESS,

        "sonorant":             SONORANTS,
        "obstruents":           OBSTRUENTS,

        "consonantal":          CONSONANTALS,
        "vocalic":              VOCALIC,

        "syllabic":             SYLLABIC,
        "nonsyllabic":          NONSYLLABIC,

        "continuant":           CONTINUANTS,
        "noncontinuant":        OCCLUSIVES,
}

# Sort all of the lists stored in DICT to ensure they are in a deterministic order
# (and to avoid polluting the git history with a bunch of meaningless order changes)
DICT = {key : sorted(DICT[key]) for key in DICT}

def getGlyphsFromClass(className):
    return utils.getGlyphsFromClass(phonemes.data, DICT, className)

def getGlyphsFromClasses(classList):
    return utils.getGlyphsFromClasses(phonemes.data, DICT, classList)
