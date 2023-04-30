"""The extractors module defines the abstract Extractor class and some friends."""

from abc import abstractmethod
from typing import (
    Any,
)

from lingdb.language import Language, DatapointKey

from .transformations import Transformation


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
GetConsonants = Get(DatapointKey.CONSONANTS)
GetNumConsonants = Get(DatapointKey.NUM_CONSONANTS)
GetEndangermentLevel = Get(DatapointKey.ENDANGERMENT_LEVEL)

# Get

# GetName

# GetCountry
# GetLanguageFamily
# GetEndangerment

# GetNumConsonants
# GetNumVowels
# GetNumPhonemes

# GetConsonants
# GetConsonantTypes
# GetVowels
# GetVowelTypes

# GetNumConsonantPlaces
# GetNumConsonantManners

# HasComplexConsonants
# HasTone
# HasStress('any', 'predictable', 'unpredictable')

# GetSyllables

# GetRecommend

# GetMorphologicalType
# GetWordFormation
# GetWordFormationFrequency('any', 'affixal', 'non-affixal')

# GetFunctionalMorphology
# GetWordOrder
# GetHeadedness

# GetAgreement
# GetCase
