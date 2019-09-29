
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


Many of the functions in this file accept as input *queries* and *results*.
queries:
    A list of Query objects (from query.py)

results:
    A list of Matches objects (a Matches object is a proxy for a list of Match objects)
    For example:
    [
        [
            Match(Language({"name": "Goemai", ...}), ["p", "t", "k"]),
            ...
        ],
        ...
    ]


Brief note on terminology for conditional queries: In the expression A -> B,
A is the implicant, and B is the implicand.
"""

import json
from jinja2 import Template

from phonemes import isPhoneme

#############################################################################
#                           Join Modes
#############################################################################
"""Definitions of the several different joining modes that may be employed
to merge the results of several conurrent queries.

E.g. INTERSECTION requires that all relevant queries be satisfied,
UNION requires that any one query be satisfied.

The X_IMPLIES_Y modes are the same as intersection, but provide additional
information that can be used to compute the denominator in generateFractionHTML()
"""

UNION = "union"
INTERSECTION = "intersection"
A_IMPLIES_B = "a implies b"
B_IMPLIES_A = "b implies a"

JOIN_MODES = [UNION, INTERSECTION, A_IMPLIES_B, B_IMPLIES_A]

#############################################################################
#                           Return Status Codes
#############################################################################
RET_CODE = "code"   # The key for return codes
PAYLOAD = "payload" # The key for the payload
DATA = "data"

# What sort of message sort be displayed to the user?
SUCCESS = "success"        # Green message
INFO = "info"              # Blue message
WARN = "warning"           # Yellow message
DANGER = "danger"          # Red message

def respond(HTML, status, data=None):
    """Given a string of HTML content and a status code, return a dictionary
    as JSON containing the two fields.

    The JSON returned should be suitable to send directly back to the client
    for processing."""

    resp = {
        RET_CODE: status,
        PAYLOAD: HTML,
    }

    if data is not None:
        resp[DATA] = data

    return json.dumps(resp, ensure_ascii=False)

def quorumErrorHTML(err):
    HTML = """
    <span class=quote>There is as yet insufficient data for a meaningful answer.</span>
    <br>
    <span class=quoteattrib> -- Isaac Asmiov, 1956 </span>
    <br><br>
    Please check back later once more data has been gathered!"""
    return HTML

def serverErrorHTML(err):
    HTML = """Sorry, an unknown server error occurred! Please let the developer know how you got this message so they can fix it."""
    return HTML

def generateHTML(results, listMode=False):
    """Given a list of queries, and a list (of lists) containining one list of
    matches for each of those queries (as tuples, described above),
    return the string representation of the HTML that will be displayed
    on the frontend in order to inform the user of the query results."""

    n = len(results) # which equals the number of queries

    # TODO move long pieces of HTML into separate directory e.g. templates?
    # TODO oneQueryHTML should not have a col-md-4 - makes no sense

    oneQueryHTML = """
    {{ reply }}

    <!-- Show language list button, followed by the list itself -->
    <br>
    <a data-toggle="collapse" data-target=".lang-list" onclick="toggleShowHideText(this)" style="cursor: pointer;margin-top: 10px;display: inline-block;">Show matching languages...</a>

    <div class="lang-list collapse" aria-expanded="false">
        <hr>
        <div class="container-fluid">
            <div class="row">

                <!-- Which languages satisfy the query -->
                <div class="col-md-4">
                    <table class="lang-list-table"
                        <tbody>
                            {% for match in results[0] %}
                            <tr>
                                <td>{{ match.language.name() }}</td>
                                <td>{{ match.cause }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

            </div>
        </div>
    </div>

    <!-- Div to hold chart. TODO: make better -->
    <div id="chart_div"></div>
    """

    twoQueryHTML = """
    <h4>Non-implicational</h4>
    {{ unionReply }}
    <br>
    {{ intersectionReply }}
    <br>
    <hr>

    <h4>Implicational</h4>
    {{ abReply }}
    <br>
    {{ baReply }}
    <br>

    <!-- Show language list button, followed by the list itself -->
    <a data-toggle="collapse" data-target=".lang-list" onclick="toggleShowHideText(this)" style="cursor: pointer;margin-top: 10px;display: inline-block;">Show matching languages...</a>


    <div class="lang-list collapse" aria-expanded="false">
        <hr>
        <div class="container-fluid">
            <div class="row">

                <!-- Which languages satisfy the first query -->
                <div class="col-md-4">
                    <h5>{{ aNum }} languages {{ aDesc }}</h5>
                    <table class="lang-list-table"
                        <tbody>
                            {% for match in results[0] %}
                            <tr>
                                <td>{{ match.language.name() }}</td>
                                <td>{{ match.cause }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <!-- Which languages satisfy the second query -->
                <div class="col-md-4">
                    <h5>{{ bNum }} languages {{ bDesc }}</h5>
                    <table class="lang-list-table"
                        <tbody>
                            {% for match in results[1] %}
                            <tr>
                                <td>{{ match.language.name() }}</td>
                                <td>{{ match.cause }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

            </div>
        </div>
    </div>

    <!-- Div to hold chart. TODO: make better -->
    <div id="chart_div"></div>
    """

    rawHTML = ""
    if n == 1:
        rawHTML = oneQueryHTML
    elif n == 2:
        rawHTML = twoQueryHTML
    else:
        raise ValueError("Number of concurrent queries must be 1 or 2 (not %d)" % n)

    # Iterate over all results and make the causes "prettier" to render
    for matches in results:
        for match in matches:

            # Replace None causes with the empty string
            if match.cause is None:
                match.cause = ""

            # Replace list causes with a prettier string.
            # Phonemes are enclosed in /../ and brackets, quotation marks are removed
            if type(match.cause) == type([]):
                match.cause = ["/%s/" % p if isPhoneme(p) else p for p in match.cause ]
                match.cause = ", ".join(match.cause)

    replies = generateRepliesHTML(results)
    replies["results"] = results # not sure if jinja needs this to be passed to use it in the template

    template = Template(rawHTML)

    HTML = template.render(replies)

    return HTML

def generateRepliesHTML(results):
    # TODO: Standardize naming.
    # "desc" refers to the latter half of the reply: e.g. "have stress"
    # "reply" refers to the entire string: "About half of languages (10 / 20) have stress"
    """Generates the "params" dictionaries required by generateHTML().
    These dictionaries will contain entries for each of the replies (as HTML) that
    will need to be inserted into the template above in generateHTML().

    If there is exactly 1 query, the dictionary will have the following keys:
        reply

    If there are exactly 2 queries, the dictionary will have the following keys:
        aReply
        bReply
        unionReply
        intersectionReply
        abReply
        baReply

        aNum
        aDesc

        bNum
        bDesc
    """

    n = len(results)

    replies = {}

    if n == 1:
        replies["reply"] = generateReplyHTML(results, UNION) # mode doesn't matter
    elif n == 2:
        replies["aReply"] = generateReplyHTML(results[:1], UNION) # TODO fix slice
        replies["bReply"] = generateReplyHTML(results[1:], UNION)
        replies["intersectionReply"] = generateReplyHTML(results, INTERSECTION)
        replies["unionReply"] = generateReplyHTML(results, UNION)
        replies["abReply"] = generateReplyHTML(results, A_IMPLIES_B)
        replies["baReply"] = generateReplyHTML(results, B_IMPLIES_A)

        # TODO: add missing fields
        replies["aNum"] = len(results[0])
        replies["bNum"] = len(results[1])
        replies["aDesc"] = results[0].query.desc()
        replies["bDesc"] = results[1].query.desc()
    else:
        raise ValueError("Number of concurrent queries must be 1 or 2 (not %d)" % n)

    return replies

def getLanguageSetsFromResults(results):
    """Given results, a list of Matches objects, return a list of
    sets of languages s.t. set[i] is a set containing every language in
    results[i]
    """
    return [matches.languageSet() for matches in results]

def generateReplyHTML(results, joinMode):
    """Given results, a list of Matches objects, generate the HTML of the reply
    in the format specified by the second argument (e.g. union, intersection, etc)

    e.g.

    "Almost all languages (19/20) have tone"
    "About half of languages (10/20) have tone AND have stress"
    """

    if joinMode not in JOIN_MODES:
        raise ValueError("'%s' is not a valid joinMode." % joinMode)

    sets = getLanguageSetsFromResults(results)

    setFn = set.intersection
    if joinMode == UNION:
        setFn = set.union

    langs = setFn(*sets)

    # NOTE: We assume all results are Matches objects from queries to same DB
    db = results[0].db

    numerator = len(langs)
    denominator = len(db)

    # TODO: Verify these indices aren't flipped around.
    if joinMode == A_IMPLIES_B:
        denominator = len(results[0])
    elif joinMode == B_IMPLIES_A:
        denominator = len(results[1])

    queries = [matches.query for matches in results]

    fractionStr = generateFractionHTML(numerator, denominator)
    descStr = mergeQueryDescs(queries, joinMode)

    return fractionStr.format(descStr)


def generateFractionHTML(numerator, denominator):
    """Given a numerator and denominator, return HTML to render an expression of
    the form:

    "_About half of languages_ (9/20) {}"

    """
    HTML = """
    <span data-toggle="tooltip" title="" data-original-title="{{ percent }}% of languages matched">
    {{ quantifier }} languages <span style="font-size: x-small;">({{ numerator }} / {{ denominator }})</span>
    </span> {{ desc }}"""

    params = {
        "percent": round(numerator / denominator * 100),
        "quantifier": floatToQuantifier(numerator / denominator),
        "numerator": numerator,
        "denominator": denominator,
        "desc": "{}", # Placeholder to be replaced in subsequent step.
    }

    template = Template(HTML)

    return template.render(**params)

def mergeQueryDescs(queries, joinMode):
    """Given queries (a list of queries), and joinMode, one of
    INTERSECTION, UNION, A_IMPLIES_B, B_IMPLIES_A
    return a string of the form
    "has at least one of [p,t,k]"
    "that have at least 3 consonants also have stress"

    or more generally: "{pre} {queries[0].desc()} {mid} {queries[1].desc()}"
    """

    if len(queries) == 1:
        return "<b>{desc}</b>".format(desc=queries[0].desc())

    if len(queries) != 2:
        raise ValueError("mergeQueryDescs(): Currently only 1 or 2 queries are supported")

    pre = ""
    mid = ""
    if joinMode == UNION:
        mid = "or"
    elif joinMode == INTERSECTION:
        mid = "and"
    elif joinMode in [A_IMPLIES_B, B_IMPLIES_A]:
        pre = "that"
        mid = "also"
    else:
        raise ValueError("generateReply() received unrecognized joinMode '%s'" % joinMode)

    params = {
        "pre": pre,
        "mid": mid,
        "desc0": queries[0].desc(),
        "desc1": queries[1].desc(),
    }

    return "{pre} <b>{desc0}</b> {mid} <b>{desc1}</b>".format(**params).strip()

#############################################################################
#                                Helper Methods
#############################################################################
def floatToQuantifier(frac):
    # TODO: Consider whether these definitions should be elsewhere (e.g. separate file)
    """Given a floating point number float in the range 0 to 1, return a quantifier
    string like "all", "nearly all", "few", "no" to represent it"""
    if frac < 0 or frac > 1:
        raise ValueError("Error: Float %f is not in the range [0,1]!" % frac)

    # NOTE: Quantifier lists must be kept sorted! They are iterated over in order.
    # fancyQuantifiers = [
    #     (0.00, "No"),
    #     (0.10, "Hardly any"),
    #     (0.20, "Few"),
    #     (0.30, "Not many"),
    #     (0.40, "Some"),
    #     (0.55, "A lot of"),
    #     (0.65, "Many"),
    #     (0.85, "Most"),
    #     (0.99, "Nearly all"),
    #     (1.00, "All")
    # ]
    # succinctQuantifiers = [
    #     (0.00, "No"),
    #     (0.10, "Almost no"),
    #     (0.25, "Very few"),
    #     (0.40, "Few"),
    #     (0.60, "About half of"),
    #     (0.75, "Many"),
    #     (0.90, "Very many"),
    #     (0.99, "Almost all"),
    #     (1.00, "All")
    # ]

    revisedQuantifiers = [
        (0.00, "No"),
        (0.15, "Few"),
        (0.30, "Some"),
        (0.40, "Many"),
        (0.60, "About half of"),
        (0.90, "Most"),
        (0.99, "Almost all"),
        (1.00, "All")
    ]

    for quant in revisedQuantifiers:
        if frac <= quant[0]:
            return quant[1]

    raise ValueError("No valid quantifier provided for float %f!" % frac)
