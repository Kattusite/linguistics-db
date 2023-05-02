"""The types module defines a collection of types that are useful for type hinting."""

from enum import StrEnum

from typing import (
    List,
    Union,
    cast,
)


class OrderedStr(StrEnum):
    """An OrderedStr is a StrEnum with custom comparisons defined for sorting.

    Given two members of this class, A and B, A < B if A was defined before B in the enum.
    """

    def __lt__(self, other: object) -> bool:
        """Return True if self was defined earlier than other in this OrderedStr."""
        cls = self.__class__
        members: 'List[OrderedStr]' = list(cls.__members__.values())

        # For sanity, do not support comparison with arbitrary strs not part of the enum.
        if self not in members or other not in members:
            return NotImplemented

        other = cast(OrderedStr, other)
        return members.index(self) < members.index(other)


class EndangermentLevel(OrderedStr):
    """An endangerment level that a language may have.

    NOTE: We'd like to name the levels just 0, 1, 2, ... but integers are not valid identifiers,
        so we prefix each name with an "L" to indicate "Level".
    """

    L0      = '0'      # noqa: E221
    L1      = '1'      # noqa: E221
    L2      = '2'      # noqa: E221
    L3      = '3'      # noqa: E221
    L4      = '4'      # noqa: E221
    L5      = '5'      # noqa: E221
    L6A     = '6a'     # noqa: E221
    L6B     = '6b'     # noqa: E221
    L7      = '7'      # noqa: E221
    L8A     = '8a'     # noqa: E221
    L8B     = '8b'     # noqa: E221
    L9      = '9'      # noqa: E221
    L10     = '10'     # noqa: E221


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
