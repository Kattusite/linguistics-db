"""The predicates module defines the abstract Predicate class and some friends."""

from abc import abstractmethod
from collections.abc import Collection
from typing import (
    Any,
    Protocol,
    Set,
    TypeVar,
)

from lingdb.types import OrderedStr, Phoneme

from .transformations import Transformation

T = TypeVar('T')


class Predicate(Transformation[T, bool]):
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

class Bool(Predicate):
    """A Predicate that returns True if its argument is truthy, or False if falsy."""

    def __call__(self, x: Any) -> bool:
        """Return True if its argument is truthy, or False if falsy."""
        return bool(x)


class Not(Predicate):
    """A Predicate that returns True if its argument is falsy, or False if truthy.

    The opposite of Bool.
    """

    def __call__(self, x: Any) -> bool:
        """Return False if its argument is truthy, or True if falsy."""
        return not bool(x)


class Contains(Predicate):
    """A Predicate that returns True if a Collection contains an element."""

    def __init__(self, needle: T):
        """Initialize the Predicate."""
        self.needle = needle

    def __call__(self, haystack: Collection[T]) -> bool:
        """Return True if the argument contains the desired element."""
        return self.needle in haystack


class ContainedIn(Predicate):
    """A Predicate that returns True if an element is contained in a Collection."""

    def __init__(self, haystack: Collection[T]):
        """Initialize the Predicate."""
        self.haystack = haystack

    def __call__(self, needle: T) -> bool:
        """Return True if the argument contains the desired element."""
        return needle in self.haystack


class SubstringContainedIn(Predicate):
    """A Predicate that returns True if a substring of an element is contained in a Collection."""

    def __init__(self, haystack: Collection[str]) -> None:
        """Bind `haystack` to create a complete predicate that can be applied to a `needle`."""
        self.haystack = haystack

    def __call__(self, needle: str) -> bool:
        """Return True if `needle` is contained in any of the items in `self.haystack`."""
        return any(needle in hay for hay in self.haystack)


################################################################################
#                               Comparisons
################################################################################

class Comparable(Protocol):
    """Types that support comparison."""

    @abstractmethod
    def __lt__(self: 'CT', other: 'CT') -> bool:  # noqa: D105
        pass

    @abstractmethod
    def __gt__(self: 'CT', other: 'CT') -> bool:  # noqa: D105
        pass

    @abstractmethod
    def __ge__(self: 'CT', other: 'CT') -> bool:  # noqa: D105
        pass

    @abstractmethod
    def __le__(self: 'CT', other: 'CT') -> bool:  # noqa: D105
        pass

    @abstractmethod
    def __eq__(self: 'CT', other: object) -> bool:  # noqa: D105
        pass

    @abstractmethod
    def __ne__(self: 'CT', other: object) -> bool:  # noqa: D105
        pass


CT = TypeVar("CT", bound=Comparable)


class Comparison(Predicate[CT]):
    """A Comparison is a special Predicate that implements comparisons, like >= or !=.

    A Comparison takes an argument, like 3 or "SVO", to form a simple comparison predicate,
    like "greater than 3" or "not equal to SVO".

    The comparison returns true if this predicate holds for the item it is called upon.

    Comparison predicates may be called on values of any comparable type, including int or str.

    As a convenience for callers, they may also be called on values that are a Collection.
    In that case, the comparison will be done on the size of the collection,
    as if an implicit `Length` transformation were applied immediately before.
    """

    # TODO: Is it wise to do these implicit length conversions?
    #   I'm increasingly convinced it's a bad idea.
    #   It makes sense for Geq, Leq, Gt, Lt, because for those it's not clear what a Collection
    #   comparison would look like anyway.
    #   Actually, maybe a "subset" or "superset" would make sense there.
    #   But imagine something like a value that is a List[int]:
    #       value = [5, 1, 34, 2]
    #       Neq(3)(value)
    #   If we add the implicit Length transformation, this is asking:
    #       does value have a length not equal to 3?
    #   If we don't, maybe it was really asking:
    #       does value equal [3]?
    #   technically, we should have written that as:
    #       Neq([3])(value)
    #   But the URL encoding scheme we chose makes it hard to tell the difference between
    #   a list of length one, and a primitive item not part of any list.
    #   We could potentially solve that by requiring that lists of one element must
    #   still end with a list delimiter, like tuples of size one in Python. (item,)
    #   In our query param encoding scheme, that would look like:
    #       Neq=3&          versus          Neq=3;&
    #   which might be good enough.
    #   Let's try implementing it and see how annoying it turns out.

    @abstractmethod
    def _compare(self, left: CT, right: CT) -> bool:
        """Return the result of comparing `left ?? right`, where ?? is a comparison operation."""
        raise NotImplementedError

    def __init__(self, right: CT) -> None:
        """Bind an argument to the Comparison to form a complete comparison predicate.

        The complete predicate can then be called on an arbitrary value to apply the predicate.
        """
        self.right = right

    def __call__(self, left: CT) -> bool:
        """Apply the comparison predicate, returning whether it is true of the provided argument."""
        right = self.right

        # If left is a Collection and right is an int, automatically assume we
        # want to compare against the length of the collection.
        # NOTE: str and Phoneme are Collections, too. This may lead to surprising results.
        if isinstance(left, Collection) and isinstance(right, int):
            left = len(left)  # type: ignore

        # If the values are of different types, it may be invalid to compare them.

        # However, we don't want to blindly check type(left) == type(right), due to inheritance.
        # If a Phoneme is passed in a query parameter, it'll deserialize to a str,
        # and we may never know to promote it back to a Phoneme again.

        # Only `right` is at risk of being demoted, though, since it comes from the query param.
        # But `left` is populated from the Language, so it will have the correct type.

        # So we first attempt to promote `right` to an instance of `type(left)`, if possible.

        def promote(right):
            """Promote `right` to be an instance of `type(left)`, if possible.

            This promotion is only possible if:
                1) left is an instance of type(right); i.e. it is an instance of a subclass of right
                2) left provides an __init__ that takes only a `type(right)`; i.e. the parent type
            """
            if not isinstance(left, type(right)):
                raise TypeError(
                    f'Cannot promote right ({right}, type: {type(right)}) '
                    f'to non-subclass type {type(left)}'
                )

            # This is a proxy for (2) above, since Phoneme and OrderedStr both definitely define
            # a constructor that takes a `str` and returns the promoted type.
            # Other types might happen to work, too, but I don't expect them to be passed in yet,
            # so for now we hard-code other type conversions as disallowed.
            if not isinstance(left, (Phoneme, OrderedStr)):
                raise TypeError(
                    f'Cannot promote right ({right}, type: {type(right)}) '
                    f'to unrecognized type {type(left)}'
                )

            PromotedType = type(left)  # pylint: disable=invalid-name
            return PromotedType(right)

        try:
            right = promote(right)
        except TypeError:
            # TODO: Log a warning.
            pass

        # We've now tried to promote, so left and right will have compatible types,
        # so long as it's remotely possible for them to.

        # Then, for the reasons described above,
        # it suffices to check only whether `left` is an instance of `right`'s type.

        # NOTE: This means it will be legal to compare `left: bool` with `right: int`.
        #   That's probably fine -- it allows e.g. Eq=0& as a shorthand for Eq=false&

        if not isinstance(left, type(right)):
            raise TypeError('Cannot compare arguments of different types')

        return self._compare(left, right)  # type: ignore  # it gets too messy to get it perfect


################################################################################
#                               Basic Comparisons
################################################################################

# WARNING: The non-equality Comparisons (Geq, Leq, Gt, Lt) may behave unexpectedly for Collections.
#   You might expect them to do something like a subset / superset check,
#   but what they actually do is an element-by-element lexicographic comparison.
#   (exactly what Python tries to do if you attempt comparing two lists or strs)

class Geq(Comparison):
    """A Comparison that returns True if `left` is greater than or equal to `right`."""

    def _compare(self, left: CT, right: CT) -> bool:
        return left >= right


class Leq(Comparison):
    """A Comparison that returns True if `left` is less than or equal to `right`."""

    def _compare(self, left: CT, right: CT) -> bool:
        return left <= right


class Gt(Comparison):
    """A Comparison that returns True if `left` is greater than `right`."""

    def _compare(self, left: CT, right: CT) -> bool:
        return left > right


class Lt(Comparison):
    """A Comparison that returns True if `left` is less than `right`."""

    def _compare(self, left: CT, right: CT) -> bool:
        return left < right


class Eq(Comparison):
    """A Comparison that returns True if `left` is equal to `right`."""

    def _compare(self, left: CT, right: CT) -> bool:
        return left == right


class Neq(Comparison):
    """A Comparison that returns True if `left` is not equal to `right`."""

    def _compare(self, left: CT, right: CT) -> bool:
        return left != right


class EqualsIgnoreCase(Comparison[str]):
    """A Predicate that returns True if two strings are equal, ignoring case."""

    def _compare(self, left: str, right: str) -> bool:
        return left.casefold() == right.casefold()


################################################################################
#                              Range Comparisons
################################################################################

class RangeComparison(Predicate[Comparable]):
    """A Predicate that compares an item against a range of endpoints."""

    def __init__(self, endpoints: Collection[Comparable]) -> None:
        """Bind the two endpoints [low, high] to create a complete predicate that can be applied."""
        if len(endpoints) != 2:
            raise ValueError(f'Exactly two endpoints required; found: {endpoints}')

        [low, high] = endpoints
        if low >= high:
            raise ValueError(f'Low endpoint was not less than high endpoint: [{low}, {high}]')

        self.low = low
        self.high = high

    @abstractmethod
    def __call__(self, x: Comparable) -> bool:
        """Return True if the comparison predicate is satisfied."""
        raise NotImplementedError()


class Between(RangeComparison):
    """A predicate that returns True if an item is between two others, excluding the endpoints."""

    def __call__(self, x: Comparable) -> bool:
        """Return True if x is strictly between the two endpoints."""
        return self.low < x < self.high


class InRange(RangeComparison):
    """A predicate that returns True if an item is between two others, including the endpoints."""

    def __call__(self, x: Comparable) -> bool:
        """Return True if x is between the two endpoints, or equal to an endpoint."""
        return self.low <= x <= self.high


################################################################################
#                              Set Comparisons
################################################################################

class SetComparison(Predicate[Collection]):
    """A Predicate comparing between Collections of elements, treating them as sets."""

    def __init__(self, right: Collection) -> None:
        """Bind `right` to form a complete comparison predicate that can be applied."""
        self.right = set(right)

    def __call__(self, left: Collection) -> bool:
        """Apply the complete comparison predicate to `left`."""
        return self._compare(set(left), self.right)

    @abstractmethod
    def _compare(self, left: Set, right: Set) -> bool:
        raise NotImplementedError()


class Subset(Comparison[Set]):
    """A predicate that returns True if a List is a subset of another."""

    def _compare(self, left: Set, right: Set) -> bool:
        return left <= right


class Superset(Predicate):
    """A predicate that returns True if a Collection is a superset of another."""

    def _compare(self, left: Set, right: Set) -> bool:
        return left >= right


class StrictSubset(Predicate):
    """A predicate that returns True if a Collection is a strict subset of another."""

    def _compare(self, left: Set, right: Set) -> bool:
        return left < right


class StrictSuperset(Predicate):
    """A predicate that returns True if a Collection is a strict superset of another."""

    def _compare(self, left: Set, right: Set) -> bool:
        return left > right
