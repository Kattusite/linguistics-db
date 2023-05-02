"""The transformations module defines the abstract Transformation class and some friends."""

from abc import ABC, abstractmethod
from typing import (
    Collection,
    Dict,
    Generic,
    Optional,
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


class MultiplexingTransformation(Transformation[T, V]):
    """An Transformation that delegates to some other one, based on the supplied argument."""

    @abstractmethod
    def _transformations(self) -> Dict[str, Transformation]:
        """Return the transformations to multiplex between, keyed by a str name."""
        raise NotImplementedError()

    @abstractmethod
    def _default_transformation(self) -> Transformation:
        """Return the transformation to be used by default.

        This will be used if the requested transformation is None or not found.
        """
        raise NotImplementedError()

    def __init__(self, transformation_name: Optional[str] = None):
        """Initialize this multiplexer to use the named transformation."""
        self.transformation_name = transformation_name
        if transformation_name is None or transformation_name not in self._transformations():
            self.transformation = self._default_transformation()
        else:
            self.transformation = self._transformations()[transformation_name]

    def __call__(self, arg: T) -> V:
        """Apply this extractor to the input Language."""
        return self.transformation.__call__(arg)


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
