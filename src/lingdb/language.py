"""The language module defines a Language and LanguageSet."""

import json

from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    List,
    Optional,
)

from lingdb.utils import MappedCollection

if TYPE_CHECKING:
    from _typeshed import StrPath
else:
    StrPath = 'StrPath'


class Phoneme(str):
    """A Phoneme represents a phoneme in a natural language, plus the glyph used to write it."""


class Datapoint:
    """A single named property of a language."""

    def __init__(self, key: str, value: Any) -> None:
        """Initialize a Datapoint."""
        self.key = key
        self.value = value

        self.type = type(value)
        """The type of this datapoint's value.

        One of:
            PRIMITIVE = str | int | float | bool
            COLLECTION = List[PRIMITIVE]
            TYPES = PRIMITIVE | COLLECTION
        """

    # TODO: This feels like a bridge too far.


# TODO: Language is not currently immutable.
#   It should be a dataclass.
class Language:
    """A Language consists of a collection of Datapoints.

    A Language should be treated as immutable.
    """

    def __init__(
        self,
        data: Dict,
    ) -> None:
        """Initialize a Language from the provided data."""
        name: Optional[str] = data.get('name')

        # Everything will be very painful later on if we allow languages not to have a name.
        if not name:
            raise ValueError('A Language must be given a name')

        self.name: str = name

        self.student: Optional[str] = data.get('student')
        self.netid: Optional[str] = data.get('netid')
        self.recommend: Optional[str] = data.get('recommend')

        self.country: Optional[str] = data.get('country')
        self.language_family: Optional[str] = data.get('language family')
        self.endangerment_level: Optional[str] = data.get('endangerment level')

        self.num_consonants: Optional[int] = data.get('num consonants')
        self.num_vowels: Optional[int] = data.get('num vowels')
        self.num_phonemes: Optional[str] = data.get('num phonemes')

        self.consonants: Optional[List[Phoneme]] = data.get('consonants')
        self.consonant_types: Optional[List[str]] = data.get('consonant types')
        self.vowels: Optional[List[Phoneme]] = data.get('vowels')
        self.vowel_types: Optional[List[Phoneme]] = data.get('vowel types')

        self.num_consonant_places: Optional[int] = data.get('num consonant places')
        self.num_consonant_manners: Optional[int] = data.get('num consonant manners')

        self.complex_consonants: Optional[bool] = data.get('complex consonants')
        self.tone: Optional[bool] = data.get('tone')
        self.stress: Optional[bool] = data.get('stress')
        self.predictable_stress: Optional[bool] = data.get('predictable stress')
        self.unpredictable_stress: Optional[bool] = data.get('unpredictable stress')

        self.syllables: Optional[List[str]] = data.get('syllables')
        self.morphological_type: Optional[List[str]] = data.get('morphological type')

        self.word_formation: Optional[List[str]] = data.get('word formation')
        self.word_formation_frequency: Optional[List[str]] = data.get('word formation frequency')
        self.affixal_word_formation_frequency: Optional[str] = data.get(
            'affixal word formation frequency')
        self.nonaffixal_word_formation_frequency: Optional[str] = data.get(
            'non-affixal word formation frequency')

        self.functional_morphology: Optional[List[str]] = data.get('functional morphology')
        self.word_order: Optional[List[str]] = data.get('word order')
        self.headedness: Optional[List[str]] = data.get('headedness')

        self._data = data

    def __getattr__(self, name: str) -> Any:
        """Get the named attribute of this Language."""
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'{self} has no attribute {name!r}')

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
