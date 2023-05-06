# REST Interface

LingDB provides a simple yet expressive REST API that allows you to execute complex
queries against a language dataset.

## Requests

Most functionality is accessed by submitting a `GET` request to the `/languages` endpoint.
Data in LingDB is read-only, so other kinds of requests (`POST`, `PATCH`, `DELETE`, ...) are
not supported.

By default, a `GET /languages` request with no other parameters will return the full set of
information known about all languages in the latest semester's dataset.

### Choosing a dataset

Optionally, the `Dataset=` query parameter may be provided to request information about
a different dataset instead. Datasets are identified by a three character string,
with the first character indicating the season (`F` for fall, `S` for spring),
and the last two characters indicating the year.

Note that the data collected for a language varies semester to semester.
A datapoint that is present in one semester's dataset may be absent in another.

Valid datasets include:
- F17
- S19
- F19
- F21
- F22


### Query Specification

If we'd like to do more than just dump out the raw contents of the dataset,
we'll need to construct more sophisticated requests.

In LingDB, the heart of any `GET /languages` request is a `Query` object.
A `Query` object specifies what data should be collected from each language,
and in what format that data should be returned.

We achieve this by stringing together an arbitrary sequence of `Transformation`s,
which are applied successively until the final result is ready to return.

Before we dive into the specification, let's look at a concrete example.

A `Query` might accomplish something like this:
    "Find all languages that have 10 or more consonants, and also lack the phonemes `/k/` or `/g/`."

As a `Query`, this would be encoded as the following request:
```
GET /languages?
        Query=&
        Get=Consonants&
        Length&
        Geq=10&
        FilterLanguages&
        Get=Consonants&
        ExtractContext&
        Intersect=k;g&
        Length&
        Eq=0&
        FilterLanguages&
```

Every parameter in that request after the first `Query=` parameter specifies a
single `Transformation`


There's a lot going on in this example, so let's break it down:
```
GET /languages?             // Request a set of languages
        Query=&             // Begin a new Query
        Get=Consonants&     // For each language, fetch the list of consonants
        Length&             // Transform each list of consonants to its length;
                            // i.e. the number of consonants
        Geq=10&             //
        FilterLanguages&
        Get=Consonants&
        ExtractContext&
        Intersect=k;g&
        Length&
        Eq=0&
        FilterLanguages&
```

### Query Specification (take 2)

A `GET /languages` request consists of zero or more `Query` objects,
which are encoded into the query parameters of the HTTP request.

As we've seen, sending a `GET /languages` request with no query parameters
will create a request with no `Query` objects, which just returns a list of
all the languages in the dataset.

A `Query` consists of a chain of zero or more query parameters that specify how
the `Query` ought to behave. Each `key=value` query parameter pair is called a
`Token`.

Each `Token` may represent:
1. A new `Transformation` to be added to the `Query`'s `Transformation` chain.
2. A new `QueryDirective` specifying some special non-`Transformation` action.

Let's consider `Transformation` tokens first.

Internally, a `Query` tracks a list of results that will be returned when the query is finished.
One result will be calculated individually for each language in the set. As we've seen, initially
the result for each language is just the language itself; that is, a full dump of all datapoints
associated with that language.

A `Transformation` object maps each input in the list of results to an arbitrary new output,
and then updates the list of results accordingly.

For example, a transformation might take in a list of phonemes, and spit out a number
representing how many phonemes were in that list (i.e., the size of that list).

In the parlance of functional programming, a `Transformation` is a function that we
[map](https://en.wikipedia.org/wiki/Map_(higher-order_function)) over the current list
of results to produce a new list of results.

In effect, a `Query` is just a chain of these `Transformation` objects that will be applied
successively, with the output of one `Transformation` being the input for the next `Transformation` in the chain:

```
1. Initial value: (all languages)
    [
        {"language": "Baba Malay",  "result": <all datapoints>},
        {"language": "Breton",      "result": <all datapoints>},
        {"language": "Cavineña",    "result": <all datapoints>},
        ...
    ]

2. Transformation (Get=Consonants)
    [
        {"language": "Baba Malay",  "result": ["n", "t", "m", ...]},
        {"language": "Breton",      "result": ["n", "t", "m", ...]},
        {"language": "Cavineña",    "result": ["n", "t", "m", ...]},
        ...
    ]

3. Transformation (Length)
    [
        {"language": "Baba Malay",  "result": 18},
        {"language": "Breton",      "result": 29},
        {"language": "Cavineña",    "result": 16},
        ...
    ]

4. Transformation (Geq=20)
    [
        {"language": "Baba Malay",  "result": false},
        {"language": "Breton",      "result": true},
        {"language": "Cavineña",    "result": false},
        ...
    ]
```


#### Transformations

There are a few notable categories of `Transformation`:

1. an `Extractor` is a `Transformation` mapping a Language to a specific data point
   from that language. In the example above, "Get Consonants" was an `Extractor`.

   An `Extractor` is generally the first `Transformation` in a `Query`, since the
   initial set of results upon which the very first `Transformation` will act is
   always a language.

2. a `Predicate` is a `Transformation` that maps a value to either `true` or `false`.
   In other words, a `Predicate` is a condition that may or may not be true of the
   value.

   A `Predicate` may be used in conjunction with the special `FilterLanguages` token
   to restrict the set of languages under consideration by a query to only that subset
   of the results for which the predicate holds true.

3. a `Transformation` that does not fall into either category has no special name;
   these are just considered transformations.

Note that some `Transformation` tokens require a value (`key=value`),
while others do not (`key=`, or just `key`).
If a `Transformation` requires a list of values, separate them with a semicolon (`key=v1;v2;v3`).

Refer to the `lingdb.transform` documentation for a complete list of the supported `Transformation` types.
The token's `key` must exactly match the name of the `Transformation` as it is defined
in that module, including uppercase and lowercase letters.

TODO: Generate napoleon docs for `lingdb.transform`, instead of enumerating them all manually.



#### Query Directives

A `Query` supports a few additional operations in addition to the standard operations available
using a chain of `Transformation` tokens.
At any point in the list of tokens for a particular `Query`,
a special token called a `QueryDirective` may appear.
These query directives instruct the query to behave in a slightly different way, described below:

- `ExtractContext`

  Immediately store a copy of the current result in a list of `contexts` that will
  be returned alongside the final answer.

  This is useful for pulling out intermediate results that might provide additional
  information about the final answer, or how it was reached.

- `FilterLanguages`

  Restrict the set of languages currently being considered to only those languages
  for which the current result is `true`.

  Any language for which the current result is `false` will be dropped from consideration.
  No results will be returned for languages filtered in this way.

- `Query`

  Immediately start a new query, ending the previous query (if there was one).

  This is optional for the first `Query` in a request, but required for all subsequent
  queries included in that same request.

- `Dataset=<datasetname>`

  If provided, this must be the name of a dataset which is to be used as the starting point
  for this query.

  If the `Dataset` token is provided, it _must_ be the very first token in its `Query`.
  `Dataset` tokens appearing elsewhere in a `Query` are invalid, and may be rejected by the server.

  Different queries within a single request may use different datasets; however, use this at your
  own risk. The frontend may not display such results nicely, though the raw JSON results should
  still be accurate.



#### Other notes

There are some special quirks to be aware of:

- The first `Query=` token is always optional. The first `Query` begins immediately starting
  from the first token in the query params, even if not preceded by a `Query=` token.
  However, subsequent queries after the first will always require a `Query=` token to start.

- If provided, the `Dataset=<dataset>` token must be the first token in the `Query`.
  Requests containing queries with a `Dataset=` token appearing in some other position
  are technically invalid, and may be rejected by the server.

- If a comparison `Predicate` (like `Geq`, `Lt`, or `Neq`) appears immediately after a result
  that is a list of values, the predicate will automatically compare against the _length_ of
  that list of values, rather than the list itself. This exists as a convenience, to make
  queries easier to specify.

- In some cases, a comparison `Predicate` may automatically attempt to convert values to a
  different type, if it is able to detect that some other type is appropriate.
  For example, `Eq=0` may be used as a shorthand for `Eq=false` if necessary. (Though it is preferred to use the special predicate `Not` in this case.)

  This behavior may lead to unexpected results. To avoid issues, it's recommended to always
  ensure you apply transformations to values of the expected types for that transformation.


## Responses

The response format is still subject to change as the API stabilizes.
The goal is for responses to `GET /languages` to look something like this:

```
[
    // one object per Query
    {
        // the dataset to which this query was applied
        "dataset": "F22",

        // the input tokens received for this query (for debugging).
        "query_tokens": [
            {"Get": "Consonants"},
            {"ExtractContext": ""},
            {"Geq": 25},
        ],

        // one object per language in the (possibly filtered) set under consideration
        results: [
            {
                // the language this result originated from
                "language": "Baba Malay",

                // the final result of applying the full transformation chain
                "result": false,

                // one entry per "ExtractContext" token
                "contexts: [
                    ["n", "t", "k", ...],
                ]
            }
        ]
    }
]
```