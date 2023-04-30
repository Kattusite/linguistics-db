"""The transformations module defines the abstract Transformation class and some friends."""

from abc import ABC, abstractmethod
from typing import (
    Any,
    Collection,
    Generic,
    TypeVar,
)


T = TypeVar('T')
V = TypeVar('V')


class Transformation(ABC, Generic[T, V]):
    """A Transformation transforms an input into an arbitrary value.

    These are completely general, and can do literally anything.
    """

    @abstractmethod
    def __call__(self, arg: T) -> V:
        """Execute the transformation on the provided argument and return the result."""
        raise NotImplementedError()


################################################################################
#                               Concrete implementations
################################################################################

class _Length(Transformation):
    """A Transformation that returns the length of a Collection."""

    def __call__(self, x: Collection) -> int:
        """Return the length of the input collection."""
        return len(x)


Length = _Length()


class Intersection(Transformation):
    """Return a new Collection equal to the intersection of a Collection with another."""

    def __init__(self, elements: Collection[T]):
        """Initialize the Transformation."""
        self.elements = elements

    def __call__(self, x: Collection[T]) -> Collection[T]:
        """Return a new collection containing only those elements in both collections."""
        # Preserve ordering of elements; avoid set()
        return [el for el in x if el in self.elements]
