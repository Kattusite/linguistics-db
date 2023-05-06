"""The handlers module defines handlers for various kinds of HTTP request."""

from collections.abc import (
    Sequence,
)
import itertools
from typing import (
    Any,
    Dict,
    List,
    NoReturn,
    Tuple,
    Union,
)
from flask import Request
from werkzeug.datastructures import ImmutableOrderedMultiDict, MultiDict
from werkzeug.exceptions import (
    BadRequest,
    InternalServerError,
)

from lingdb.dataset import Dataset
from lingdb.language import LanguageSet

from lingdb.query import Query, QueryResult, get_query_directive
from lingdb.transform import get_transformation, Transformation
from web.exceptions import FailedLoadingDataset, NoSuchDataset


# The order of parameters is important, so we use an OrderedMultiDict
Request.parameter_storage_class = ImmutableOrderedMultiDict

JsonDict = Dict[str, Any]
Serializable = Union[JsonDict, List[JsonDict]]

Token = Tuple[str, str]
"""A single key=value parameter from the HTTP query params."""

QuerySpec = Sequence[Token]
"""A sequence of Token objects specifying a complete Query."""

class LanguageHandler:
    """The LanguageHandler class handles GET /languages requests.

    Each request provides a list of zero or more Query specifications describing what data
    it would like to be returned.

    A Query is encoded in the query parameters of the HTTP request, in a format like the following:

    Example:
        GET /languages?
            Query=&  // if you want you can give a name or something
            Get=Consonants&
            Intersection=p;t;k;b;d;g&
            ExtractContext=&
            Geq=3&
            FilterLanguages=&
            Get=Name&
            Query=&
            ...
    """

    def __init__(self) -> None:
        # Load in datasets once to avoid repeated work.
        self.datasets: Dict[Dataset, LanguageSet] = {}
        for dataset in Dataset:
            # If we fail to import a dataset, try importing the others anyway.
            try:
                self.datasets[dataset] = dataset.load()
            except ValueError as exc:
                # TODO: Log this
                # TODO: In theory lots of errors could be raised.
                #   Add more as we find them.
                print(f'Failed to load dataset {dataset}: {exc}')

        self.latest_dataset = self.datasets[Dataset.latest()]

    def _extract_tokens(self, query_params: MultiDict) -> Sequence[Token]:
        """Extract a Sequence[Token] from the provided query params."""
        # The interface werkzeug provides does not suit our needs,
        # so we convert to a sequence of tokens instead.
        #   (
        #       ('Query', ''), ('Get', 'Consonants'), ('Intersection', 'p;t;k;b;d;g'), ...
        #       ('Query', ''), ...
        #   )
        tokens: Sequence[Token] = tuple(query_params.items(multi=True))
        return tokens

    def _extract_query_specs(self, tokens: Sequence[Token]) -> Sequence[QuerySpec]:
        """Split the input Sequence[Token] into a Sequence[QuerySpec].

        Arguments:
            tokens: a single sequence of tokens, delimited by ('Query', ...) tokens

        Returns:
            a sequence of QuerySpec objects.
            The sequence contains one item per Query included in the request,
            and that item will have the full list of Tokens associated with that query.
        """
        # Now we split on each 'Query' token to create a list of QuerySpec objects.
        def is_query_token(token: Token):
            key, _value = token
            return key == 'Query'

        # NOTE: By this logic, the Query= for the initial query is optional.
        #   Thus, it is perfectly valid for the leading Query= to be omitted.
        #   However, subsequent Query= tokens are required, as they delimit adjacent queries.
        query_specs: Tuple[QuerySpec] = tuple([
            # Extract each group as a tuple ...
            tuple(group)
            # ... Using tokens where `is_query_token() == True` as a group delimiter ...
            for is_delimiter, group in itertools.groupby(tokens, key=is_query_token)
            # ... dropping from the output any group which is just a delimiting query token.
            if not is_delimiter
        ])

        return query_specs

    def _get_initial_dataset(self, query_spec: QuerySpec) -> Dataset:
        """Get the Dataset that should be used as the starting point for this Query."""
        # If no Dataset token is provided, use the latest dataset by default.
        default_dataset = Dataset.latest()

        tokens = query_spec
        if not tokens:
            return default_dataset

        # If a Dataset token appears anywhere in the query_spec, it must come first.
        key, value = tokens[0]
        if key != 'Dataset':
            return default_dataset

        try:
            return Dataset(value)
        except ValueError as err:
            # TODO: Log
            # A named Dataset was requested, but no Dataset by that name could be found.
            raise NoSuchDataset(value) from err

    def _get_language_set(self, dataset: Dataset) -> LanguageSet:
        """Get the LanguageSet that should be used as the starting point for this Query."""
        try:
            return self.datasets[dataset]
        except KeyError as err:
            # TODO: Log
            # A named Dataset was requested, but no Dataset by that name could be found.
            raise FailedLoadingDataset(dataset) from err

    def _parse_token_value(self, token: Token) -> Any:
        """Parse the value of `token` into some appropriate type, then return it.

        Examples:
            parse('42') -> 42
            parse('false') -> False
            parse('a;b;c') -> ['a', 'b', 'c']
            parse('4;7') -> [4, 7]
        """
        key, value = token

        # NOTE: In theory we could use `key` to determine what type we should convert to.
        #   In practice, we mostly don't do that yet. Maybe someday, though.

        # Split apart lists first; if it's a list we need to parse each element recursively
        LIST_DELIMITER = ';'
        if LIST_DELIMITER in value:
            return [self._parse_token_value((key, v)) for v in value.split(LIST_DELIMITER)]

        # Check for bool
        if value.lower() == 'false':
            return False
        if value.lower() == 'true':
            return True

        # Check for int
        try:
            return int(value)
        except ValueError:
            pass

        # NOTE: We don't check for float because right now none of our values can be floats.
        #   But in theory it's the exact same as for `int`.

        # Otherwise just assume str
        return value

    def _build_query(self, query_spec: QuerySpec) -> Query:
        """Construct and return a Query from the provided QuerySpec.

        Arguments:
            query_spec: A QuerySpec listing each Transformation to be included in this Query.

        Returns:
            the constructed Query, including each of the requested Transformations.

        Raises:
            KeyError if a token's key does not correspond to any valid Transformation.
        """
        query = Query()

        # TODO: Implement me
        for i, token in enumerate(query_spec):
            key, value = token

            # Get the transformation identified by this key
            # (or raise an error if no such transformation exists)

            # Not all valid keys correspond to Transformations.
            # First, check if this key corresponds to a QueryDirective, and apply it if so.
            FoundQueryDirective = get_query_directive(key)  # pylint: disable=invalid-name
            if FoundQueryDirective is not None:
                # NOTE: Right now no QueryDirective subclass accepts any args, so we ignore value.
                query.apply(FoundQueryDirective())
                continue

            # Then, check if this key corresponds to a transformation.
            FoundTransformation = get_transformation(key)

            # NOTE: Some Transformations are subclasses of Transformation. (i.e., types)
            #   Others are instances of Transformations (i.e. instances of types)
            if FoundTransformation is not None:
                if isinstance(FoundTransformation, Transformation):
                    # If it's already an instance, we just apply it to the query as-is.
                    query.apply(FoundTransformation)
                    continue
                elif issubclass(FoundTransformation, Transformation):
                    # If it's just a type, we need to instantiate it, passing `arg` as an argument.
                    arg = self._parse_token_value(token)
                    query.apply(FoundTransformation(arg))
                    continue
                else:
                    # TODO: Unexpected. Log & raise error
                    raise ValueError(f'Found unexpected Transformation {FoundTransformation}')

            # Now we handle everything else, that's not a QueryDirective or Transformation.

            # If we're looking at a leading Dataset= token, that's valid, and we can just move on.
            if i == 0 and key == 'Dataset':
                continue

            # Everything else is unrecognized. Treat the request as malformed, and raise an error.
            # TODO: Implement me.
            # TODO: Ensure that we raise an exception with the appropriate HTTP status code.
            # TODO: Find better error type. custom MalformedRequestError? flask error? ...?
            raise ValueError(f'token {i} was unrecognized: {key}={value}')

        return query

    def _execute_query(self, query: Query, dataset: LanguageSet) -> QueryResult:
        """Execute a single query against the provided dataset and return the result."""
        return query.evaluate(dataset)

    def _handle(self, request: Request) -> Serializable:
        """Attempt to handle a request, without doing any error handling."""
        # Pre-process the query parameters
        args = request.args
        all_tokens = self._extract_tokens(args)
        query_specs = self._extract_query_specs(all_tokens)

        # Special case: if no queries were provided, just return the full latest dataset.
        if not query_specs:
            query_spec = (
                ('Dataset', Dataset.latest().value),
            )
            query_specs = (query_spec,)

        # NOTE: If the only Token provided was a Dataset=, we just dump the corresponding dataset.
        #   This case is already handled correctly by `_build_query()`; no need to special case it.

        # Execute the request
        query_results: List[QueryResult] = []
        for query_spec in query_specs:
            initial_dataset = self._get_initial_dataset(query_spec)
            initial_language_set = self._get_language_set(initial_dataset)
            query = self._build_query(query_spec)
            query_result = self._execute_query(query, initial_language_set)
            query_results.append(query_result)

        # Prepare the results to be sent back to the client
        response = [
            {
                'dataset': initial_dataset,
                'query_tokens': dict(query_spec),
                'results': query_result.serializable(),
            } for query_result, query_spec in zip(query_results, query_specs)
        ]

        return response

    def _handle_error(self, request: Request, err: Exception) -> NoReturn:
        """Attempt to handle any error that might arise while handling a request."""

        # TODO: It'd probably be more natural just to make `NoSuchDataset` subclass `HTTPException`.

        if isinstance(err, NoSuchDataset):
            raise BadRequest(description=str(err))

        if isinstance(err, FailedLoadingDataset):
            raise InternalServerError(description=str(err))

        raise err

    def handle(self, request: Request) -> Serializable:
        """Handle an incoming request by executing the zero or more queries contained within it."""
        try:
            return self._handle(request)
        except Exception as err:
            return self._handle_error(request, err)
