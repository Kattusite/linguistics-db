import language, tinydb
import query as Query
from data import const

"""Querier.py defines the functions needed to take in a POST request from the
frontend, and translate the fields of this request into a TinyDB query.
This query will then be executed, and its results will be processed in the
manner specified by the form fields. Finally, a status code will be returned
to indicate the status of the query, and a response body will be returned
containing the content to be displayed back to the end user."""

QUORUM_THRESHOLD = 0.5

class QuorumError(RuntimeError):
    pass

def dbFromDataset(dataset):
    """Given the name of a dataset, return a TinyDB instance representing that
    dataset's complete data."""
    # This function may be unnecessary (?)
    filename = dataset + ".json"
    return const.DATASET_PATH.format(dataset, filename)

def handleQueries(queries, db):
    # TODO: How are results of different queries merged together?
    allResults = [handleQuery(q, db) for q in queries]
    return allResults

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

    # TODO: Status
    # status =
    # return results, status

    return results

def toLanguages(queryResults):
    """Given a list of results from queries, return a list of Languages, one
    for each language that appeared in the results."""
    return [Language(result) for result in queryResults]
