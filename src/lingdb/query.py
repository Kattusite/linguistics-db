"""The query module represents queries that can be applied to sets of languages."""

from itertools import zip_longest
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    Union,
)


from lingdb.language import Language, LanguageSet
from lingdb.transform import Transformation
from lingdb.types import DatapointValue


Context = DatapointValue
"""Any type that can be returned in a QueryResult as the Context for a single Language.

Context is a more specific piece of information extracted from a Language.

NOTE: An entire Language itself is not a valid kind of context. It must be more specific than that.
"""

ContextSet = Sequence[Context]
"""A collection containing one Context for each Language in a LanguageSet."""

Result = Union[Context, Language]
"""Either a raw Language, or a piece of Context about a Language."""

ResultSet = Union[ContextSet, LanguageSet]
"""Either a raw LanguageSet, or a ContextSet with one context for each language in a LanguageSet."""

History = List
"""A historical collection tracking all past values of an attribute."""


# TODO: Move to lingdb.query.result
class QueryResult:
    """A QueryResult is the output produced by a Query.

    It consists of a "result" indicating the main result of the computation,
    plus some additional "context" that might have been extracted at various
    intermediate points during the computation, e.g. to expose rationale to users,
    or to pull out data points for use in a graph.
    """

    def __init__(self, language_set: LanguageSet) -> None:
        """Initialize a QueryResult with the provided language_set.

        At first, the result_set and language_set are both just the starting language_set,
        and there are no initial pieces of context.
        """
        # During Query processing, the LanguageSet may be altered, e.g. by filtering.
        #
        # We keep track of the past LanguageSets, mostly for debugging.
        self._language_sets: History[LanguageSet] = [language_set]
        """The internal history of all past values of self.language_set, exposed for debugging."""

        # During Query processing, `result` is iteratively updated to track the "running total".
        #
        # We initialize it to the input LanguageSet, to account for the special case where no
        # transformations are applied -- in this case the Query is the identity mapping.
        self._result_sets: History[ResultSet] = [language_set]
        """An internal history of all past values of self._result, exposed for debugging."""

        # During Query processing, new context entries might be added to the list.
        # The list starts empty because no context is captured until specifically requested.
        self.contexts: List[ContextSet] = []
        """A list of all sets of context extracted during request processing, if any."""

    def __str__(self) -> str:
        """Return a string representation of this object."""

        def truncate(items: ResultSet, max_items: int = 5) -> str:
            """Show only the first N results from a list to avoid spam."""
            if len(items) < max_items:
                return str(items)
            items_str = ', '.join(str(item) for item in items[:max_items])
            return f'[{items_str}, ...]'

        result_set = truncate(self.result_set)
        contexts = [truncate(context) for context in self.contexts]

        return f'<{len(self.result_set)} results: {result_set}, contexts={contexts}>'

    def __repr__(self) -> str:
        """Return a string representation of this object."""
        param_names = ('language_set', 'result_set', 'contexts')
        params = ', '.join(f'{param}={getattr(self, param)}' for param in param_names)
        return f'{self.__class__.__name__}({params})'

    def serializable(self) -> Dict[str, Any]:
        """Return a json-serializable representation of this QueryResult."""
        language_names = [language.name for language in self.language_set]

        result_set = self.result_set
        if isinstance(result_set, LanguageSet):
            result_set = [language.name for language in result_set]

        # Convert [(1,2,3), (a,b,c)] -> [(1,a), (2,b), (3,c)]
        context_lists = list(zip(*self.contexts))
        return [
            {'language': language, 'result': result, 'contexts': context_list}
            for language, result, context_list
            in zip_longest(language_names, result_set, context_lists, fillvalue=tuple())
        ]

        # NOTE: Alternatively we could return the parallel lists version:
        # return {
        #     'language_set': [language.name for language in self.language_set],
        #     'result_set': result_set,
        #     'contexts': self.contexts,
        # }

    ############################################################################
    #                               Properties
    ############################################################################

    @property
    def result_set(self):
        """The current evaluation of the result of this query."""
        return self._result_sets[-1]

    @result_set.setter
    def result_set(self, result_set: ResultSet):
        self._result_sets.append(result_set)

    @property
    def language_set(self):
        """The current LanguageSet being considered by this query."""
        return self._language_sets[-1]

    @language_set.setter
    def language_set(self, language_set: LanguageSet):
        self._language_sets.append(language_set)

    ############################################################################
    #                               Mutators
    ############################################################################

    def extract_context(self):
        """Append the current result to context."""
        # A ContextSet can only be a list of Context, which must be primitives or lists thereof.
        # A LanguageSet might appear in self.result_set (since it is a valid ResultSet),
        # but it is not a valid ContextSet.
        if isinstance(self.result_set, LanguageSet):
            raise TypeError(
                'Cannot extract an entire LanguageSet as a ContextSet. '
                'Try transforming the LanguageSet first.'
            )
        self.contexts.append(self.result_set)

    def apply(self, transformation: Transformation[Result, Result]):
        """Mutate the current result by applying a Transformation."""
        old_result_set = self.result_set
        try:
            new_result_set = list(map(transformation, old_result_set))

        # A Transformation may raise an arbitrary exception, so we can't be more specific.
        except Exception as exc:
            raise RuntimeError('Transformation function raised an error') from exc

        self.result_set = new_result_set

    def filter_languages(self):
        """Filter the current LanguageSet by removing any Language whose current result is False."""
        old_language_set = self.language_set
        old_result_set = self.result_set
        new_languages = []

        for language, result in zip(old_language_set, old_result_set):
            # NOTE: In theory, we could try casting `result` to `bool` with `bool(result)`.
            #   But that seems like it could lead to subtle bugs. For now, we just require
            #   that clients must have a Predicate in the Query chain immediately before this
            #   to explicitly cast everything to a bool.
            if not isinstance(result, bool):
                raise TypeError('\n'.join([
                    'Filtering is only possible if the most recent results were of type bool',
                    f'  Language: {language}',
                    f'  Result: ({type(result)}) {result}',
                ]))

            if result:
                new_languages.append(language)

        new_language_set = LanguageSet(new_languages)
        self.language_set = new_language_set


# TODO: Move to lingdb.query.directives
class QueryDirective:
    """QueryDirective acts a special processor directive, triggering special Query behavior.

    A QueryDirective slots into a Query's Transformation chain, but it is not a Transformation.
    Instead, it acts as a placeholder in the Transformation chain to signal to the Query
    that some special behavior should be injected between ordinary Transformations, like extracting
    context, or filtering the LanguageSet of interest.

    Unlike an ordinary Transformation, there is no notion of transforming inputs to outputs.
    A QueryDirective will generally not modify the currently evaluated result of the Query.
    """


class ExtractContext(QueryDirective):
    """ExtractContext is a QueryDirective signaling a Query should extract context."""


# TODO: Rename to FilterLanguages?
class FilterLanguageSet(QueryDirective):
    """FilterLanguageSet is a QueryDirective signaling a Query should filter its LanguageSet."""


def get_query_directive(name: str) -> Optional[Type[QueryDirective]]:
    """Return the QueryDirective class of the given name, or None if that name is unrecognized."""
    matching_subclasses = [
        subclass for subclass in QueryDirective.__subclasses__()
        if subclass.__name__ == name
    ]
    if len(matching_subclasses) > 1:
        # TODO Log
        raise KeyError(f'More than one subclass named {name} was found: {matching_subclasses}')
    if len(matching_subclasses) == 1:
        return matching_subclasses[0]
    return None


# spell-checker:ignore ptkbdg
class Query:
    """A Query is a collection of transformations that can be applied to set of languages.

    Queries consist of zero or more Transformations, connected together in a chain.

    Example:
        A query to extract the Collection of consonants in a language:
            Query().apply(Get('consonants'))

        A query to filter a language set down to only those languages with >= 4 of 'ptkbdg',
        extracting as context the set of consonants from 'ptkbdg' that the language had.
            (Query()
                .apply(Get('consonants'))
                .apply(Intersect('ptkbdg'))
                .extract_context()
                .apply(Geq(4))
                .filter()
            )
    """

    def __init__(self) -> None:
        """Initialize an empty query, with no transformations."""
        self.transformations: List[Union[Transformation, QueryDirective]] = []

    def apply(
        self,
        transformation: Union[Transformation[Result, Result], QueryDirective],
    ) -> 'Query':
        """Apply the provided transformation to this chain.

        Returns:
            the Query itself, to allow for method chaining.
        """
        self.transformations.append(transformation)
        return self

    def extract_context(self) -> 'Query':
        """Extract the result of evaluating the Query at this moment, and save it as context."""
        self.transformations.append(ExtractContext())
        return self

    def filter(self) -> 'Query':
        """Filter the LanguageSet being processed to only those which satisfy the latest predicate.

        Raises:
            TypeError: if the latest Transformation was not a Predicate

        Returns:
            - the Query itself, to allow for method chaining.

        NOTE: Though `filter()` does technically allow for method chaining,
            `filter()` is generally expected to be the final filter in the chain.
        """
        self.transformations.append(FilterLanguageSet())
        return self

    def evaluate(self, languages: LanguageSet) -> QueryResult:
        """Evaluate the full Query and return a QueryResult with the result and all context."""
        result = QueryResult(languages)

        for transformation in self.transformations:
            if isinstance(transformation, Transformation):
                result.apply(transformation)

            if isinstance(transformation, ExtractContext):
                result.extract_context()

            if isinstance(transformation, FilterLanguageSet):
                result.filter_languages()

        return result
