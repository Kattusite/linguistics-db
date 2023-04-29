"""The language module defines a Language and LanguageSet."""

import json
from typing import Any, Dict, Iterable, List, Optional


class Phoneme(str):
    pass

class Datapoint:
    """A single named property of a language."""

    def __init__(self, key: str, value: Any) -> None:
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


class Language:
    """A Language consists of a collection of Datapoints."""

    def __init__(
        self,
        data: Dict,
    ) -> None:
        self.name: Optional[str] = data.get('name')
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
        self.affixal_word_formation_frequency: Optional[str] = data.get('affixal word formation frequency')
        self.nonaffixal_word_formation_frequency: Optional[str] = data.get('non-affixal word formation frequency')

        self.functional_morphology: Optional[List[str]] = data.get('functional morphology')
        self.word_order: Optional[List[str]] = data.get('word order')
        self.headedness: Optional[List[str]] = data.get('headedness')

        self._data = data

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'{self} has no attribute {name!r}')

    def __hash__(self) -> int:
        return hash((self.name, self.student, self.netid))

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other)

    def __str__(self):
        return f'<Language {self.name}>'

    def __repr__(self):
        return f'Language({json.dumps(self._data, indent=4, ensure_ascii=False)})'



class LanguageSet:
    """A collection of several Language objects."""

    @classmethod
    def from_json(cls, filename: str) -> 'Language':
        """Create a new Language"""
        with open(filename, 'r', encoding='utf-8') as f:
            languages_data = json.load(f)
        languages = [Language(language_data) for language_data in languages_data]
        return cls(languages)

    def __init__(self, languages: Iterable[Language]):
        self._languages = set(languages)

    def __repr__(self):
        lang_strs = '\n'.join(f'    {lang!r},' for lang in self._languages)
        return f'LanguageSet(\n{lang_strs}\n)'

    def __str__(self) -> str:
        lang_strs = ', '.join(str(lang) for lang in self._languages)
        return f'<LanguageSet: {{{lang_strs}}}>'

DATASETS = '../../data/datasets'

F22 = LanguageSet.from_json(f'{DATASETS}/F22/F22.json')
