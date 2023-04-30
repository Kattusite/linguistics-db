"""The predicates module defines the abstract Predicate class and some friends."""

from abc import abstractmethod
from typing import (
    Any,
    Collection,
)

from .transformations import Transformation


class Predicate(Transformation):
    """A Predicate is a special transformer that always outputs a bool.

    It is excluded from consideration when building the rationale explaining
    why a language was or was not included in a LanguageSet.

    It is usually used for the final check; e.g.
        - greater than 3?
        - contains the element "p"
        - equals "bar"
        -
    """

    @abstractmethod
    def __call__(self, x: Any) -> bool:
        """Execute the transformation on the provided argument and return the bool result."""
        raise NotImplementedError()


################################################################################
#                               Concrete implementations
################################################################################

class Contains(Predicate):
    """A Predicate that returns True if a Collection contains an element."""

    def __init__(self, needle: Any):
        """Initialize the Predicate."""
        self.needle = needle

    def __call__(self, haystack: Collection) -> bool:
        """Return True if the argument contains the desired element."""
        return self.needle in haystack

