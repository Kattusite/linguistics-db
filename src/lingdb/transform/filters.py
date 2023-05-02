"""The transform.filters module defines the special Filter Transformation.

It also defines several FilterPredicates, the names of which can be provided
as arguments to Filter in order to filter a collection.
"""

from enum import Enum
from typing import Collection, Optional

from lingdb.transform import Predicate, Transformation
from lingdb.types import Phoneme


class IsNasal(Predicate[Phoneme]):
    """A FilterPredicate returning True if a phoneme is a nasal."""

    def __call__(self, x: Phoneme) -> bool:
        """Return True if x is a nasal phoneme."""
        # TODO: This is for the sake of illustration. Not exhaustive.
        return x in 'mn'


class FilterPredicate(Enum):
    """Predicates that can be identified by name to use them in a Filter Transformation."""

    NASAL = IsNasal

    # Users might pass predicate names from query params in the wrong case.
    # Let's try to accept predicates case-insensitively.
    @classmethod
    def _missing_(cls, value: object) -> 'Optional[FilterPredicate]':
        if not isinstance(value, str):
            return None
        return cls(value.upper())


class Filter(Transformation[Collection, Collection]):
    """A Filter builds maps collection to another, taking only items that satisfy a predicate."""
    # TODO: Implement me


# pylint: disable=pointless-string-statement
"""
For example, we'd like to use this for expressions like:
    - has >= 3 vocalic
    - has == 1 mid vowel
    - has < 4 nasals

In theory we could implement that as an Intersection,
but then we'd have to explicitly define what the second collection was.
(on the frontend).

This way, we can just give a name to the property we want the phoneme to have (on the frontend),
and then map to an actual collection on the backend by filtering down the list of results.

Note that this Filter is NOT intended to filter down the list of Languages;
see FilterLanguages for that.

This one is meant to filter the items in a result collection so that we get some other result
collection, which we can then apply more transformations to.

For example, here's "has < 4 nasals":
    Query()
        .apply(GetConsonants)
        .apply(Filter("Nasal"))
        .apply(Lt(4))

Basically, I see this taking some of the functionality of the `phonemes` and `metaclasses`
libraries from the v2 LingDB implementation.

It's worth noting that there may be a much better way to implement this than as Predicates.
Worth sketching this out in more detail before implementing much further.
"""
