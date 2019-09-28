import json
import tinydb

from . import query as Query
from . import language
from data import const, selectors, datasets
from phonemes import vowels, consonants, metaclasses

"""Querier.py defines the functions needed to take in a POST request from the
frontend, and translate the fields of this request's form into a TinyDB query.
This query will then be executed, and its results will be processed in the
manner specified by the form fields. Finally, a status code will be returned
to indicate the status of the query, and a response body will be returned
containing the content to be displayed back to the end user."""

QUORUM_THRESHOLD = 0.5

class QuorumError(RuntimeError):
    pass

def dbFromRequest(request):
    """Given an XHR request from the frontend, return the TinyDB instance that
    contains the dataset the request is looking for"""
    form = request.form
    dataset = form["dataset"]
    return datasets.getDatabase(dataset)


def queriesFromRequest(request):
    """Given an XHR request from the frontend, return a list of Query objects,
    one for each query specified in the XHR request"""

    form = request.form

    queryDatas = json.loads(form["payload"])

    """To make a query, we might need:
    * Type          (String, Num, Bool, etc.)
    * Property      (e.g. "num consonants")
    * Mode          (e.g. GT, LT, etc.)
    * k             (e.g. 0, 1, 2, 3, ...)
    * ls            (e.g. [p, t, k])
    * desc          (optional - e.g. "have {mode} {k} of {property}")
    * value         (e.g. "Nigeria", False)

    Currently the XHR contains absolutely none of these fields.
    Instead it has mode, selList, sel, trait, reply

    Maybe we can put some info (e.g. type) into selectors.py and infer the rest...

    """

    queries = []
    for queryData in queryDatas:

        getData = lambda key: None if key not in queryData else queryData[key]

        # Read fields from request
        trait   = getData("trait")
        mode    = getData("mode")
        ls      = getData("selList")
        value   = getData("sel")
        k       = getData("k")
        if k is not None:
            k = int(k)

        # TODO: We have already implemented some functionality for generating
        # the replies from descriptions serverside, but are overriding all this
        # functionality by setting the desc exactly as provided by the client
        desc    = getData("reply")

        # Get required data from selector
        selector = selectors.SELECTORS_DICT[trait]

        type = selector[selectors.TYPE]
        property = selector[selectors.PROPERTY]

        # Some traits are special, and have parameterized properties.
        # We must supply the parameter (which is passed in as the "sel" param of the request)
        if "{value}" in property:
            property = property.format(**{"value": value})

        # Some traits signify queries over special "classes" of phonemes,
        # and we must translate these class descriptions into concrete lists
        # of phonemes
        if trait == selectors.CONSONANT_CLASS[selectors.HTML_ID]:
            ls = consonants.getGlyphsFromClasses(ls)
        elif trait == selectors.VOWEL_CLASS[selectors.HTML_ID]:
            ls = vowels.getGlyphsFromClasses(ls)
        elif trait == selectors.METACLASS[selectors.HTML_ID]:
            ls = metaclasses.getGlyphsFromClasses(ls)

        # Call the appropriate constructor for a query of the given type
        query = None
        if type == Query.LIST:
            query = Query.List(property, mode, k, ls, desc=desc)
        elif type == Query.NUM:
            query = Query.Num(property, mode, k, desc=desc)
        elif type == Query.STRING:
            query = Query.String(property, mode, value, desc=desc)
        elif type == Query.BOOL:
            query = Query.Bool(property, value, desc=desc)
        elif type == Query.ALWAYS:
            query = Query.Always()
        elif type == Query.NEVER:
            query = Query.Never()

        queries.append(query)

    return queries

    # NOTE about special cases:
    # There are some requests that are "special cases", where the frontend UI
    # lies about how the data is really represented.
    # e.g. Metaclasses are really simultaneous consonant/vowel queries.
    #   maybe define a separate Query() TYPE = "phoneme" to hardcode this functionality?
    # e.g. PHONEME_INVENTORY_SIZE and CONSONANT_ARTICULATION are aliases for some other type
    # For now let's add special cases for these?

    # Idea: Write custom tinydb.test() methods to combine e.g. vowels + consonants.
    # This will take care of the metaclasses issue.



def handleQueries(queries, db):
    """Execute each query in queries and return a list of Matches objects indicating
    the results of running all queries."""
    return [handleQuery(q, db) for q in queries]

def handleQuery(query, db):
    """handleQuery will run a single query from the frontend against the DB,
    returning the status code and results.
    Results will be a tuple consisting of first the entire JSON of the language
    that was matched, followed by the specific values held by that language
    that were responsible for satisfying the query.
    E.g. If we asked for a language with at least three consonants, we would
    return all the consonants in that language as the second tuple entry."""

    results = query.query(db)

    # Perform a quorum check - did enough of the queried languages have data to
    # provide?
    Lang = tinydb.Query()
    langsWithData = db.search(Lang[query.property].exists())
    if len(langsWithData) < QUORUM_THRESHOLD * len(db):
        raise QuorumError("Not enough languages had data for property '%s'" % query.property)

    return results
