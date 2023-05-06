"""The language module defines a Language and LanguageSet."""

from collections import defaultdict
import json
import logging

from enum import StrEnum
import string
from typing import (
    TYPE_CHECKING,
    Dict,
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


LOGGER = logging.getLogger(__name__)


class DatapointKey(StrEnum):
    """A DatapointKey represents the name of a single datapoint in a language."""

    # TODO: This duplicates some legacy csv_to_json code.
    #   Let's revise that csv_to_json code to use these constants instead.

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

    def serializable(self):
        """Return a serializable version of this Language."""
        return self._data


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

        # If the language set contains multiple languages by the same name,
        # it might be that multiple students all chose the same language.
        # (For example, "Pipil" appears twice in the F17 data.)

        # In this case, append a unique letter to the end of each language entry:
        #   - ("Pipil", "Pipil") -> ("Pipil A", "Pipil B")

        # TODO: This solution is not very robust.
        #   It does not assign the letters 'A', 'B', in a way that is globally stable;
        #   it's determined solely by the order of the language in the input list.
        #   So if students found some way to change the order of the list,
        #   (or to filter the list to drop one of the duplicates),
        #   it's possible the "A" and "B" labels might switch places or disappear.
        # However, it works well enough if we're working with just a single dataset,
        # which is 99% of the typical use cases.

        # TODO: This approach doesn't modify the languages themselves, which still
        #   display with the exact same name. It only changes their keys in the LanguageSet.
        #   This might lead to confusing results in API calls or the UI.

        # TODO: This wacky 'Language A' / 'Language B' logic is almost entirely useless right now.
        #   The 'A'/'B' name isn't exposed anywhere in the API or UI since the language itself isn't
        #   modified in any way. So this logic would have been equivalent to just modifying
        #   __getitem__ to not return a result (or return a list of results, ...) if there were
        #   multiple languages for that name...
        #   This is starting to look like a werkzeug MultiDict with extra steps.

        self._languages_dict: Dict[str, Language] = {}
        already_seen_languages: Dict[str, List[Language]] = defaultdict(list)

        def register_new_alias(language: Language, letter: str):
            """Register a new alias of `language`, appending `letter` as an identifier."""
            alias_name = f'{language.name} {letter}'

            LOGGER.warning('Aliasing duplicate language %s to %s', language.name, alias_name)

            # Insert this alias
            self._languages_dict[alias_name] = language

            # Weird special case: In theory, the new alias could conflict with a *different*
            #   language whose name was already very similar to this one.
            #   So we add this new alias name to the seen set as well.
            already_seen_languages[alias_name].append(language)

        for language in self._languages:
            other_languages_with_this_name = already_seen_languages[language.name]

            # Special case: If this is the first dupe of a language, pop the original language
            #   (e.g. Pipil) to replace it with an annotated version (e.g. Pipil A).
            #   We must do this before adding e.g. Pipil B if we want to preserve ordering.
            if len(other_languages_with_this_name) == 1:
                orig_language = self._languages_dict.pop(language.name)
                register_new_alias(orig_language, 'A')

            # Now add this new dupe of the language to the dict and seen set.
            if len(other_languages_with_this_name) >= 1:
                letter = string.ascii_uppercase[len(other_languages_with_this_name)]
                register_new_alias(language, letter)

            else:
                # This is the first time we've seen this language -- just add it
                self._languages_dict[language.name] = language
                already_seen_languages[language.name].append(language)

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
