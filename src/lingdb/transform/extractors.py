"""The extractors module defines the abstract Extractor class and some friends."""

from abc import abstractmethod
from typing import (
    Any,
    Dict,
)

from lingdb.language import Language, DatapointKey

from .transformations import MultiplexingTransformation, Transformation


class Extractor(Transformation):
    """An Extractor is a transformer that pulls out a value directly from a Language.

    Extractors generally do not do any "analysis".

    Examples:
        - Language -> list of consonants in that language
        - Language -> name
        - Language -> has stress in that language?
    """

    @abstractmethod
    def __call__(self, language: Language) -> Any:
        """Execute the transformation on the provided Language and return the result."""
        raise NotImplementedError()


################################################################################
#                               Concrete implementations
################################################################################

class Get(Extractor):
    """An Extractor that gets a named field from a language."""

    def __init__(self, attr: str):
        """Initialize a Get Extractor."""
        self.attr = attr

    def __call__(self, language: Language) -> Any:
        """Execute the Get Extractor."""
        return getattr(language, self.attr)


GetName = Get(DatapointKey.NAME)

GetCountry = Get(DatapointKey.COUNTRY)
GetLanguageFamily = Get(DatapointKey.LANGUAGE_FAMILY)
GetEndangerment = Get(DatapointKey.ENDANGERMENT_LEVEL)

GetNumConsonants = Get(DatapointKey.NUM_CONSONANTS)
GetNumVowels = Get(DatapointKey.NUM_VOWELS)
GetNumPhonemes = Get(DatapointKey.NUM_PHONEMES)

GetConsonants = Get(DatapointKey.CONSONANTS)
GetConsonantTypes = Get(DatapointKey.CONSONANT_TYPES)
GetVowels = Get(DatapointKey.VOWELS)
GetVowelTypes = Get(DatapointKey.VOWEL_TYPES)

GetNumConsonantPlaces = Get(DatapointKey.NUM_CONSONANT_PLACES)
GetNumConsonantManners = Get(DatapointKey.NUM_CONSONANT_MANNERS)

HasComplexConsonants = Get(DatapointKey.COMPLEX_CONSONANTS)
HasTone = Get(DatapointKey.TONE)

# HasAnyStress looks up the literal "stress" key in the language.
HasAnyStress = Get(DatapointKey.STRESS)
HasPredictableStress = Get(DatapointKey.PREDICTABLE_STRESS)
HasUnpredictableStress = Get(DatapointKey.UNPREDICTABLE_STRESS)

GetSyllables = Get(DatapointKey.SYLLABLES)

GetRecommend = Get(DatapointKey.RECOMMEND)

GetMorphologicalType = Get(DatapointKey.MORPHOLOGICAL_TYPE)

GetWordFormation = Get(DatapointKey.WORD_FORMATION)

# GetAnyWordFormationFrequency looks up the literal "word_formation_frequency" key in the language.
GetAnyWordFormationFrequency = Get(DatapointKey.WORD_FORMATION_FREQUENCY)
GetAffixalWordFormationFrequency = Get(DatapointKey.AFFIXAL_WORD_FORMATION_FREQUENCY)
GetNonaffixalWordFormationFrequency = Get(DatapointKey.NONAFFIXAL_WORD_FORMATION_FREQUENCY)

GetFunctionalMorphology = Get(DatapointKey.FUNCTIONAL_MORPHOLOGY)
GetWordOrder = Get(DatapointKey.WORD_ORDER)
GetHeadedness = Get(DatapointKey.HEADEDNESS)

GetAgreement = Get(DatapointKey.AGREEMENT)
GetCase = Get(DatapointKey.CASE)


################################################################################
#                             Multiplexing Extractors
################################################################################

MultiplexingExtractor = MultiplexingTransformation[Language, Any]


# HasStress accepts a string ('any', 'predictable', 'unpredictable')
# and then delegates to the appropriate specific extractor above.
class HasStress(MultiplexingExtractor):
    """An Extractor for a specific kind of stress, supplied as an argument."""

    def _extractors(self) -> Dict[str, Extractor]:
        return {
            'any': HasAnyStress,
            'predictable': HasPredictableStress,
            'unpredictable': HasUnpredictableStress,
        }

    def _default_extractor(self) -> Extractor:
        return HasAnyStress


class HasWordFormationFrequency(MultiplexingExtractor):
    """An Extractor for a specific kind of word formation frequency, supplied as an argument."""

    def _extractors(self) -> Dict[str, Extractor]:
        return {
            'any': GetAnyWordFormationFrequency,
            'affixal': GetAffixalWordFormationFrequency,
            'nonaffixal': GetNonaffixalWordFormationFrequency,
        }

    def _default_extractor(self) -> Extractor:
        return GetAnyWordFormationFrequency
