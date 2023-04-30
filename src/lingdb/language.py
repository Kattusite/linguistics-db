"""The language module defines a Language and LanguageSet."""

import json

from enum import StrEnum
from typing import (
    TYPE_CHECKING,
    Iterable,
    Iterator,
    List,
    Mapping,
    Required,
    TypedDict,
)
from lingdb.types import DatapointValue, Phoneme

from lingdb.utils import MappedCollection

if TYPE_CHECKING:
    from _typeshed import StrPath
else:
    StrPath = 'StrPath'


class DatapointKey(StrEnum):
    """A DatapointKey represents the name of a single datapoint in a language."""

    # TODO: Some of the JSON keys have spaces and hyphens, etc in them.
    #   Let's replace all of them with underscores for consistency.
    #   This will require updating the CSV to JSON code (const.py?)

    NAME = 'name'

    STUDENT = 'student'
    NETID = 'netid'

    COUNTRY = 'country'
    LANGUAGE_FAMILY = 'language_family'
    ENDANGERMENT_LEVEL = 'endangerment_level'

    NUM_CONSONANTS = 'num_consonants'
    NUM_VOWELS = 'num_vowels'
    NUM_PHONEMES = 'num_phonemes'

    CONSONANTS = 'consonants'
    CONSONANT_TYPES = 'consonant_types'
    VOWELS = 'vowels'
    VOWEL_TYPES = 'vowel_types'

    # Deprecated
    HAS_3_PLUS_PLACES = '3+_consonant_places'
    HAS_2_PLUS_MANNERS = '2+_consonant_manners'

    NUM_CONSONANT_PLACES = 'num_consonant_places'
    NUM_CONSONANT_MANNERS = 'num_consonant_manners'

    COMPLEX_CONSONANTS = 'complex_consonants'
    TONE = 'tone'

    # NOTE: Before F22, STRESS was the only kind of stress -- it indicated "predictable stress".
    #   In F22 a new option was added for "unpredictable stress".
    #   Now STRESS is a derived value, true if either kind of stress appears.
    STRESS = 'stress'
    PREDICTABLE_STRESS = 'predictable_stress'
    UNPREDICTABLE_STRESS = 'unpredictable_stress'

    SYLLABLES = 'syllables'

    RECOMMEND = 'recommend'

    MORPHOLOGICAL_TYPE = 'morphological_type'
    WORD_FORMATION = 'word_formation'
    WORD_FORMATION_FREQUENCY = 'word_formation_frequency'
    AFFIXAL_WORD_FORMATION_FREQUENCY = 'affixal_word_formation_frequency'
    NONAFFIXAL_WORD_FORMATION_FREQUENCY = 'nonaffixal_word_formation_frequency'

    FUNCTIONAL_MORPHOLOGY = 'functional_morphology'
    WORD_ORDER = 'word_order'
    HEADEDNESS = 'headedness'

    AGREEMENT = 'agreement'
    CASE = 'case'


# BUG: We'd like to able to re-use the keys from DatapointKey, but that's not yet supported.
# For now, just copy-paste the above list, and find & replace "\w+ = "
# See https://github.com/python/mypy/issues/4128
#
# BUG: When accessing members of the TypedDict using the StrEnum members as keys,
#   you must attach an extra .value:
#       GOOD:       data[DatapointKey.NAME.value]
#       BAD:        data[DatapointKey.NAME]
# Because we're using a StrEnum, I don't think this should be necessary,
# but if you get rid of it, mypy complains:
#   TypedDict "DatapointDict" has no key "NAME"  [typeddict-item]mypy(error)

DatapointDict = TypedDict('DatapointDict', {
    'name': Required[str],

    'student': Required[str],
    'netid': Required[str],

    'country': str,
    'language_family': str,
    'endangerment_level': str,

    'num_consonants': int,
    'num_vowels': int,
    'num_phonemes': int,

    'consonants': List[Phoneme],
    'consonant_types': List[str],
    'vowels': List[Phoneme],
    'vowel_types': List[str],

    # Deprecated
    '3+_consonant_places': bool,
    '2+_consonant_manners': bool,

    'num_consonant_places': int,
    'num_consonant_manners': int,

    'complex_consonants': bool,
    'tone': bool,

    # NOTE: Before F22, STRESS was the only kind of stress -- it indicated "predictable stress".
    #   In F22 a new option was added for "unpredictable stress".
    #   Now STRESS is a derived value, true if either kind of stress appears.
    'stress': bool,
    'predictable_stress': bool,
    'unpredictable_stress': bool,

    'syllables': List[str],

    'recommend': str,

    'morphological_type': List[str],
    'word_formation': List[str],
    'word_formation_frequency': List[str],
    'affixal_word_formation_frequency': str,
    'nonaffixal_word_formation_frequency': str,

    'functional_morphology': List[str],
    'word_order': List[str],
    'headedness': List[str],

    'agreement': str,
    'case': str,
}, total=False)


class Language(Mapping[DatapointKey, DatapointValue]):
    """A Language consists of a collection of Datapoints.

    A Language should be treated as immutable.
    """

    def __init__(self, data: DatapointDict) -> None:
        """Initialize a Language from the provided DatapointDict."""
        # The name, student, and netid are required to uniquely identify the language.
        try:
            self.name = data[DatapointKey.NAME.value]
            self.student = data[DatapointKey.STUDENT.value]
            self.netid = data[DatapointKey.NETID.value]
            # Also reject falsy values (i.e. empty strings or None)
            if not self.name or not self.student or not self.netid:
                raise ValueError('A Language must have a non-empty name, student, and netid.')
        except (KeyError, ValueError) as exc:
            raise ValueError('A Language must be given a name, student, and netid.') from exc

        # NOTE: All the rest of these are defined mostly for better IDE support.
        #   The custom __getattr__ will pick them up regardless of whether they are
        #   defined here, but if they are, they will show up in IDE completions.
        self.recommend = data.get(DatapointKey.RECOMMEND.value)

        self.country = data.get(DatapointKey.COUNTRY.value)
        self.language_family = data.get(DatapointKey.LANGUAGE_FAMILY.value)
        self.endangerment_level = data.get(DatapointKey.ENDANGERMENT_LEVEL.value)

        self.num_consonants = data.get(DatapointKey.NUM_CONSONANTS.value)
        self.num_vowels = data.get(DatapointKey.NUM_VOWELS.value)
        self.num_phonemes = data.get(DatapointKey.NUM_PHONEMES.value)

        self.consonants = data.get(DatapointKey.CONSONANTS.value)
        self.consonant_types = data.get(DatapointKey.CONSONANT_TYPES.value)
        self.vowels = data.get(DatapointKey.VOWELS.value)
        self.vowel_types = data.get(DatapointKey.VOWEL_TYPES.value)

        self.num_consonant_places = data.get(DatapointKey.NUM_CONSONANT_PLACES.value)
        self.num_consonant_manners = data.get(DatapointKey.NUM_CONSONANT_MANNERS.value)

        self.complex_consonants = data.get(DatapointKey.COMPLEX_CONSONANTS.value)
        self.tone = data.get(DatapointKey.TONE.value)
        self.stress = data.get(DatapointKey.STRESS.value)
        self.predictable_stress = data.get(DatapointKey.PREDICTABLE_STRESS.value)
        self.unpredictable_stress = data.get(DatapointKey.UNPREDICTABLE_STRESS.value)

        self.syllables = data.get(DatapointKey.SYLLABLES.value)
        self.morphological_type = data.get(DatapointKey.MORPHOLOGICAL_TYPE.value)

        # pylint: disable=line-too-long
        self.word_formation = data.get(DatapointKey.WORD_FORMATION.value)
        self.word_formation_frequency = data.get(DatapointKey.WORD_FORMATION_FREQUENCY.value)
        self.affixal_word_formation_frequency = data.get(DatapointKey.AFFIXAL_WORD_FORMATION_FREQUENCY.value)  # noqa: E501
        self.nonaffixal_word_formation_frequency = data.get(DatapointKey.NONAFFIXAL_WORD_FORMATION_FREQUENCY.value)  # noqa: E501
        # pylint: enable=line-too-long

        self.functional_morphology = data.get(DatapointKey.FUNCTIONAL_MORPHOLOGY.value)
        self.word_order = data.get(DatapointKey.WORD_ORDER.value)
        self.headedness = data.get(DatapointKey.HEADEDNESS.value)

        self._data = data

    def __iter__(self) -> Iterator[DatapointKey]:
        """Return an iterator over the datapoint keys in this language."""
        for key in self._data.keys():
            yield DatapointKey(key)

    def __len__(self) -> int:
        """Return the number of datapoints in this language."""
        return len(self._data)

    def __getattr__(self, name: DatapointKey) -> DatapointValue:
        """Get the named datapoint value of this Language.

        Raises:
            KeyError if the named datapoint does not exist for this language.
        """
        if name in self._data:
            return self._data[name.value]
        raise AttributeError(f'{self} has no attribute {name!r}')

    def __getitem__(self, name: DatapointKey) -> DatapointValue:
        """Get the named datapoint value of this Language.

        Raises:
            KeyError if the named datapoint does not exist for this language.
        """
        # Similar to __getattr__, but there's no chance of seeing any other entries in __dict__.
        # Raises a KeyError if the field isn't recognized, just like an ordinary dict.
        return self._data[name.value]

    def __hash__(self) -> int:
        """Return a hash of this Language."""
        return hash((self.name, self.student, self.netid))

    def __eq__(self, other: object) -> bool:
        """Return True if this Language is equal to `other`."""
        # TODO: This is a pretty quick and dirty check, but it works for now.
        return hash(self) == hash(other)

    def __str__(self):
        """Return a string representation of this Language."""
        return f'<Language {self.name}>'

    def __repr__(self):
        """Return a string representation of this Language."""
        return f'Language({json.dumps(self._data, indent=4, ensure_ascii=False)})'


class LanguageSet(MappedCollection[str, Language]):
    """A Collection of unique Language objects that supports getting Language objects by name.

    The collection is immutable and must not contain duplicates.
    """

    @classmethod
    def from_json(cls, filename: StrPath) -> 'LanguageSet':
        """Create a new LanguageSet by loading it from a JSON file."""
        with open(filename, 'r', encoding='utf-8') as f:
            languages_data = json.load(f)
        languages = [Language(language_data) for language_data in languages_data]
        return cls(languages)

    def __init__(self, languages: Iterable[Language]):
        """Initialize a LanguageSet from the provided `languages`."""
        # We might get an arbitrary iterable. Convert to a tuple for safety.
        self._languages = tuple(languages)
        self._languages_dict = {language.name: language for language in self._languages}

        super().__init__(self._languages_dict)

        # Forbid duplicate Language entries
        if len(self._languages) != len(self._languages_dict):
            raise ValueError('A LanguageSet may not contain duplicate Language objects')

    def __repr__(self):
        """Return a string representation of this LanguageSet."""
        lang_strs = '\n'.join(f'    {lang!r},' for lang in self._languages)
        return f'LanguageSet(\n{lang_strs}\n)'

    def __str__(self) -> str:
        """Return a string representation of this LanguageSet."""
        lang_strs = ', '.join(str(lang) for lang in self._languages)
        return f'<LanguageSet: {{{lang_strs}}}>'
