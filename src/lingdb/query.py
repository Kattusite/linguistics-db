"""The query module represents queries that can be applied to sets of languages."""

from transformer import Transformation


class QueryResult:
    """A QueryResult is the output produced by a Query.

    It consists of a "result" indicating the main result of the computation,
    plus some additional "context" that might have been extracted at various
    intermediate points during the computation, e.g. to expose rationale to users,
    or to pull out data points for use in a graph.
    """

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

    def __init__(self):
        pass

    def apply(Transformation[T, V]) ->