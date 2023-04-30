"""The types module defines a collection of types that are useful for type hinting."""

from typing import (
    List,
    Union,
)


class Phoneme(str):
    """A Phoneme represents a phoneme in a natural language, plus the glyph used to write it."""


DatapointPrimitive = Union[str, int, bool, Phoneme]
"""The basic types of datapoints associated with a Language.

For example, language names are stored as strings, the number of consonants is stored
as an int, and whether the language has stress is stored as a bool.

Primitives don't include Lists; for a similar type including those, see DatapointValue.

Primitives also exclude None and float, despite those values being valid in JSON.
That is because to date, no survey questions have required answers that are floats or None.
"""

DatapointValue = Union[DatapointPrimitive, List[DatapointPrimitive]]
"""The type of any value that can be associated with a key in a Language.

All values in a language's JSON file are either a Primitive, or a List[Primitive];
in other words, every value has type DatapointValue.
"""
