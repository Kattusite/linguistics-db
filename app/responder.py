
"""responder.py is broadly responsible for taking in the raw query results
returned by querier.py, and converting these results to a response that can
be sent back to the client.

The results for a single query will be in the form of a list of tuples, where
the first element of the tuple is the complete data of the matched language, and
the second element of the tuple is the specific piece of data that caused that
language to match the query (or None if this is not applicable).

The response sent to the client will be in the form of a dictionary, which
can be dumped as a JSON string and send directly to the client. The dictionary
will have the following fields:
* "html": The html content to be rendered on the page.
* "status": An indication of the query's status, to inform what color the
            infobox should be drawn in on the frontend. For example,
            if there is insufficient language data to answer a query, the
            status will be set accordingly, so the box can be colored yellow.
* TBD: As-yet-undetermined fields will need to be added later to enable
         graphs to be drawn; perhaps a list of the complete raw query results
         so that the Google Charts API can make use of them.
"""

def generateHTML(queries, results, listMode=False):
    # TODO: Should be a list of queries, right? and a list of lists of results
    """Given a list of queries, and a list containining one list of results for
    each of those queries (as tuples, described above),
    return the string representation of the HTML that will be displayed
    on the frontend in order to inform the user of the query results."""

    pass

def generateMatchingLanguageTables(queries, results):
    # TODO: Deal with headers (e.g. "8 languages matched...")
    # Could either use "hideHeaders" as in old code, or just write a separate
    # function only responsible for doing this. 
    """Given a list of results for a query (as tuples, described above),
    return the string representation of the HTML that will be displayed to the
    user tabulating the specific languages that matched, and what caused that
    language to be included.

    For example, if the query was for languages with at least 1 of p,t,k;
    a possible table appear as follows:

    * Goemai: p, t
    * Creek: p
    * Choctaw: p, t, k
    """


def generateIntersectionReply(results):
