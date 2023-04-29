"""The transformer module defines the Transformer class and some friends."""

from abc import ABC, abstractmethod
from typing import (
    Any,
    Collection,
    Generic,
    TypeVar,
)

from lingdb.language import Language


T = TypeVar('T')
V = TypeVar('V')


"""
NOTE:
    It'd be convenient to be able to chain transformers:

    F22
        .apply(GetConsonants)
        .apply(Intersection('ptk'))
        .apply(Geq(3))

    We could explicitly set whether we want to consider each transformer for rationale:

    F22
        .apply(GetConsonants)
        .apply(Intersection('ptk'))
        .apply(Geq(3), consider=False)

    Or we could introduce some alias for `.apply()` that automatically implies `consider=False`,
    such as `imagine()`, `filter()`, `suppose()`, `where()`

    F22
        .apply(GetConsonants)
        .apply(Intersection('ptk'))
        .where(Geq(3))  # consider = False

    Instead of having each .apply() return a literal value, perhaps we should return
    some special helper class, like `Transformation` or `Transformable`.

    This gives us:
        1) a nice place to define the `.apply()` method
        2) a nice place to keep track of internal state, like the current rationale
            (instead of returning the literal value and then back-computing the rationale,
            we could return an object that simultaneously tracks the value and rationale together.)
"""


# spell-checker:ignore hsilgn aeiou
# pylint: disable=pointless-string-statement
"""

I'm not 100% sold on the names and interfaces so far, so let's look at an example.
Maybe this will give me a clearer understanding of how I want the system to work.

result = (
    LanguageSet                     #  Evaluation       Context         Locked
        .apply(GetName)             #   'English'       'English'       False
        .apply(Reverse)             #   'hsilgnE'       'hsilgnE'       False
        .apply(First(3))            #   'hsi'           'hsi'           False
        .suppose(EndsWith('x'))     #   False           'hsi'           True
)

Well, based on that, I kind of like the names "Evaluation", "Context", "Locked"
(or maybe "finalized")

Or maybe `frozen`?

Might be nice to have an explicit `.lock()` or `.finalize()` instead of
introducing the `.suppose()` implicit locking.

This is especially true if it's only legal to lock once.
No need to make the author keep track of whether they're meant to be writing
`apply()` or `suppose()`

So how about something like:

result = (
    LanguageSet
        .apply(Get('consonants'))
        .apply(Unique)                  # drop any duplicates
        .apply(Intersection('ptk'))
        .freeze()
        .apply(Leq(2))
)

Remember, the ULTIMATE goal here is to filter the LanguageSet down to a smaller one.

So Predicates are inherently special -- they are the only thing that can terminate
a filter chain, since we ultimately need a yes/no on whether to include each language.

Let's add a `filter()` to the end to indicate that we're ready to spit out a new LanguageSet

result = (
    LanguageSet
        .apply(Get('consonants'))
        .apply(Unique)                  # drop any duplicates
        .apply(Intersection('ptk'))
        .freeze()
        .apply(Leq(2))
        .filter()               # drop any language whose current evaluation is Falsy.
)

Everything we've looked at here has been looking at ways to express a single complex query,
like "all languages with at least 3 vowels"

The next step is to plan what it would look like to chain together several queries!

TODO: What's a good name for a single related collection of Transformations?

        Query? Trait? Filter? TransformationChain? Chain?

TODO: Right now, we "freeze" only a single value -- the "context"

    Imagine we were trying to generate a graph or something.
    Wouldn't it also be useful to be able to "extract" or "freeze" arbitrary transformations
    along the chain?

    e.g. I want to filter out only those languages which have Geq(5) vowels,
        but I want to extract a value of "num consonants" for each one.

    One way to solve this is to have `.filter()` return a LanguageSet that we can
    apply arbitrary transformations to. This doesn't actually require us to change
    anything; the current proposal basically already supports this. Yay!


Okay, so what would it look like to try and run multiple queries against a language set?
(e.g. to run implicational universals, like:
    "languages that have Geq(5) vowels" and "languages that have Geq(5) consonants"
)

We need to be able to run either Query against the LanguageSet individually.
    - show all languages that satisfy Query A
    - show all languages that satisfy Query B
    - show all languages that satisfy Query A and B

So we don't want to directly chain them together, necessarily:

BAD

LanguageSet
    .apply(GetConsonants)
    .freeze()
    .apply(Geq(5)) # if this is a predicate, I think we can assume the previous one is a freeze()...
    .filter()
    .apply(GetVowels)
    .freeze()
    .apply(Geq(5)
    .filter()

This is clunky because it forces an ordering (A then B).

Instead we want more like:

LanguageSet.applyAll([
    Query           # some dummy "identity" placeholder
        .apply(GetConsonants)
        .apply(Geq(5))        # since this is a predicate, it's implied that this forces a freeze()
        .filter(),
    Query
        .apply(GetVowels)
        .apply(Geq(5))        # for convenience Geq works on both Collections and ints
        .filter()
])

Another question: How can we dynamically build strings to describe these operations?
    (or should we just hard-code the descriptive strings?)

e.g. how do we go from:

Query
    .apply(GetVowels)
    .apply(Intersection('aeiou'))
    .apply(Geq(3))

to "has at least 3 of 'aeiou'"?

My gut says we'll get best quality by assigning a hard-coded name to each Query.

Another question: What will the UI be like for users to actually build one of these
    fancy Query objects on the site?

Probably will have a series of options to choose from based on type at each step.

So e.g. if it's a collection, there'll be a "CollectionSelector" that gives the user
a choice between:
    "Length", "Reverse", "Unique", "Intersection", ...

TBH most of those sound pretty useless for users, though.
When would a user need to reverse? Or for that matter, even know the length?!

Maybe I need to take a step back and look at some potential questions that a student
might ask about the data.

"""
# pylint: enable=pointless-string-statement


class Transformation(ABC, Generic[T, V]):
    """A Transformation transforms an input into an arbitrary value.

    These are completely general, and can do literally anything.
    """

    @abstractmethod
    def __call__(self, arg: T) -> V:
        """Execute the transformation on the provided argument and return the result."""
        raise NotImplementedError()


class Extractor(Transformation):
    """An Extractor is a transformer that pulls out a value directly from a Language.

    Extractors generally do not do any "analysis".

    Examples:
        - Language -> list of consonants in that language
        - Language -> name
        - Language -> has stress in that language?
    """

    # TODO: Does it make sense to have an Extractor at all?
    #   Why not just stick to transformers?

    @abstractmethod
    def __call__(self, language: Language) -> Any:
        """Execute the transformation on the provided Language and return the result."""
        raise NotImplementedError()


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
#                               Concrete examples
################################################################################

class Get(Extractor):
    """An Extractor that gets a named field from a language."""

    def __init__(self, attr: str):
        """Initialize a Get Extractor."""
        self.attr = attr

    def __call__(self, language: Language) -> Any:
        """Execute the Get Extractor."""
        return getattr(language, self.attr)


GetName = Get('name')
GetConsonants = Get('consonants')
GetNumConsonants = Get('num_consonants')
GetEndangermentLevel = Get('endangerment_level')


class _Length(Transformation):
    """A Transformation that returns the length of a Collection."""

    def __call__(self, x: Collection) -> int:
        """Return the length of the input collection."""
        return len(x)


Length = _Length()


class Contains(Predicate):
    """A Predicate that returns True if a Collection contains an element."""

    def __init__(self, needle: Any):
        """Initialize the Predicate."""
        self.needle = needle

    def __call__(self, x: Collection) -> bool:
        """Return True if the argument contains the desired element."""
        return self.needle in x


class Intersection(Transformation):
    """Return a new Collection equal to the intersection of a Collection with another."""

    def __init__(self, elements: Collection[T]):
        """Initialize the Transformation."""
        self.elements = elements

    def __call__(self, x: Collection[T]) -> Collection[T]:
        """Return a new collection containing only those elements in both collections."""
        # Preserve ordering of elements; avoid set()
        return [el for el in x if el in self.elements]
