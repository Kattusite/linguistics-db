#############################################################################
#       lingdb_client.py
#
#############################################################################

import os, re, sys
from lingdb import LingDB, Language
from phonemes import vowels, consonants
import data
from data import selectors
import phonemes

# Lightweight "Database" objects representing each language dataset
# (can be replaced with an actual DB later if the overhead is justified.
# One dataset per semester that we have data (duh :P)
datasets = {
    name: LingDB(data.getDataset(name)) for name in data.getDatasetNames()
}

def handleQuery(query, dataset):
    """Given a query dict, decide which type of query has been made, and return a
    list of results corresponding to the languages matching that type of query"""

    lingDB = datasets[dataset]
    trait = query["trait"]

    # Look up this query's function in the mapping table (from selectors.py)
    try:
        fn = selectors.function_map[trait]
    except KeyError as e:
        sys.stderr.write("Unrecognized query type: lingdb_client has no defined function handler for: %s\n" % trait)
        raise e

    # Pass the function into query() to be called with its arguments
    return lingDB.query(fn, query)

def handleQueries(queries, dataset, listMode=False):
    """Process multiple queries and direct them as appropriate, according to the
    trait each one represents."""

    lingDB = datasets[dataset]

    # Can be cleaned up with comprehensions
    result_arr = []   # List of sets of (Language, queryResult) pairs
    lang_arr   = []   # list of sets of languages
    reply_arr  = []   # List of strings to be rendered on frontend

    # Create a result set, lang set, and reply for each query
    for query in queries:
        queryResults = handleQuery(query, dataset)

        # Convert to sets so we can use set ops like intersect and union later.
        # resultSet = set of (language, matchingProperty) pairs
        resultTuple = tuple(queryResults)
        resultSet = set(resultTuple)


        # langSet = set of language objects
        langSet = set([res[LingDB.QUERY_LANG] for res in queryResults])

        reply_arr.append(query["reply"])
        result_arr.append(resultSet)
        lang_arr.append(langSet)

    # Define some constants
    n = len(result_arr)
    nlStr   = "\n<br>\n"
    hrStr   = "\n<hr>\n"

    # If no queries were handled, something went wrong!
    if n == 0:
        print("lingdb_client error: 0 queries were properly handled!")
        return None # Query invalid

    # Combine the results of the n queries
    # TODO Clean this whole section up (add HTML styling + a separate formatter function)
    # TODO allow AND, OR, etc. to be selected as a request field, not hardcoded
    # TODO Magic numbers 0, 1, 2 are bad
    # TODO also allow for displaying the results of each subquery alone--
    # If I query for A & B & C, also display just A, just B, just C.
    # TODO also add a small table with a list of languages matching just A, just B, or A and B
    uRep = createUnionReply(lang_arr, reply_arr, lingDB)
    iRep = createIntersectionReply(lang_arr, reply_arr, lingDB)
    cRep = createConditionalReply(lang_arr, reply_arr, 0, lingDB)

    # The response structure partitions results with newlines and horizontal rules
    # so that the data is returned in a nice format
    response = {
        "logical":          [],
        "implicational":    [],
        "list":             []
    }

    listRep = createLangLists(result_arr, reply_arr, listMode=listMode)
    response["list"].append(listRep)

    if n >= 1:
        response["logical"].append(uRep)   # A (or B (or C...))
    if n >= 2:
        response["logical"].append(iRep)   # A (and B (and C...))
        response["implicational"].append(cRep)   # A --> B

        # If exactly two query terms, throw in B --> A
        if n == 2:
            cRep2 = createConditionalReply(lang_arr, reply_arr, 1, lingDB)
            response["implicational"].append(cRep2)

    # Format the response structure with newlines and rules
    sections = []
    sections.append(nlStr.join(response["logical"]))
    sections.append(nlStr.join(response["implicational"]))

    # Filter out empty strings (sections without any content added)
    sections = [s for s in sections if len(s) > 0]

    # Add the list section onto the bottom (it has its own <hr> element)
    joinedSections = hrStr.join(sections)
    listSection = nlStr.join(response["list"])

    return "".join([joinedSections, listSection])


#############################################################################
#                          Formatted Reply Methods
#############################################################################

def mergeReplies(replies, joinWord):
    """Join together the strings in replies, using joinWord as a semantic separator
    (e.g. "and", "or")"""
    # TODO implement this for more modularity in the createReply functions
    return NotImplemented

def createUnionReply(langs, replies, db):
    """Return a string of HTML representing the formatted results to be
    displayed for the given results list and replies list, and containing db,
    assuming the queries are joined together using union (OR)"""
    matches = [x.getLanguage() for x in set.union(*langs)]
    num = len(matches)
    den = len(db)
    reply = "".join(["<b>", "</b> or <b>".join(replies), "</b>"])
    frac  = createFractionHTML(num, den)
    return " ".join([frac, reply])

def createIntersectionReply(langs, replies, db):
    """Return a string of HTML representing the formatted results to be
    displayed for the given results list and replies list, and containing db,
    assuming the queries are joined together using intersection (AND)"""
    matches = [x.getLanguage() for x in set.intersection(*langs)]
    num = len(matches)
    den = len(db)
    reply = "".join(["<b>", "</b> and <b>".join(replies), "</b>"])
    frac  = createFractionHTML(num, den)
    return " ".join([frac, reply])

def createConditionalReply(langs, replies, which, db):
    """Return a string of HTML representing the formatted results to be
    displayed for the given results list and replies list, and containing db,
    assuming the queries are joined together using conditional (R[which] implies R[1,2,3,...])
    The parameter which specifies the index of the item implying the others"""
    matches = [x.getLanguage() for x in set.intersection(*langs)]
    num = len(matches)
    den = len(langs[which])
    ifReply   = "".join([" that <b>", replies[which], "</b> also "])
    thenReply = "".join(["<b>", "</b> and <b>".join(replies[:which] + replies[which+1:]), "</b>"])
    frac  = createFractionHTML(num, den)
    condStr = " ".join([frac, ifReply, thenReply])
    return condStr

# Create HTML for a table representing one or more lists of tabulated results,
# of the form "language" : "result" (if result is not a bool)
# Use bootstrap layout instead of the actual HTML <table> tags
def createLangLists(results, replies, listMode=False):
    # Define table template
    table = """
    <div class="lang-list %s">
        <hr>
        <div class="container-fluid">
            <div class="row">
                %s
            </div>
        </div>
    </div>"""

    # WARNING: Bootstrap v3.0 ONLY. If transition to v4.0, "in" becomes "show"
    listClass = "collapse" if not listMode else "collapse in"

    # Sort the result list lexicographically by the name of the language.
    getLangName = lambda x: x[LingDB.QUERY_LANG].getLanguage()
    orderedResults = [sorted(list(s), key=getLangName) for s in results]

    # Define the columns
    n = len(results)
    hideHeaders = n <= 1
    langLists = [createLangList(orderedResults[i], replies[i], hideHeaders) for i in range(n)]
    cols = "".join(langLists)
    # print(n, hideHeaders)
    return table % (listClass, cols)

# BUG: Handling of wrapping each list element in /.../ is poor. I assume that
# all things are phonemes (if <= 2 chars, but a boolean flag might be better)
def createLangList(results, reply, hideHeaders):
    header = "" if hideHeaders else str(len(results)) + " languages " + reply
    ls = """
    <div class="col-md-4">
        <h5>%s</h5>
        <table class="lang-list-table">
            <tbody>
                %s
            </tbody>
        </table>
    </div>"""

    rows = []
    for res in results:
        lang = res[LingDB.QUERY_LANG].getLanguage()

        matchedProperty = res[LingDB.QUERY_RESULT]

        # The type of matchedProperty is tuple or bool. Figure out which.
        # If bool, display nothing (the query had no additional info to report)
        # If tuple, it is a list of matching glyphs. Sort and prettify it
        if type(matchedProperty) == type(True):
            matchedStr = ""
        elif type(matchedProperty) == type(tuple([])):
            matchedList = sorted(list(matchedProperty))

            # Workaround for wrapping phonemes and only phonemes in /.../
            matchedList = ["/%s/" % s if phonemes.isPhoneme(s) else s for s in matchedList]
            matchedStr = str(matchedList)

            # Eliminate special array characters so it is human readable
            matchedStr = matchedStr.replace("\'","")
            matchedStr = matchedStr.replace("[", "")
            matchedStr = matchedStr.replace("]", "")
        else:
            raise TypeError(("Passed a matchedProperty %s of incorrect type!"
                             % matchedProperty) +
                             "\nMust be tuple or bool!")

        tr = """
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>"""

        rows.append(tr % (lang, matchedStr))

    return ls % (header, "".join(rows))




# Deprecated.. just here in case I mess up too badly
def createOldLangList(results, reply, hideHeaders):
    header = "" if hideHeaders else str(len(result)) + " languages " + reply
    td = """
    <td>
        <h5>%s</h5>
        <ul>
            %s
        </ul>
    </td>"""

    langs = [ res[LingDB.QUERY_LANG].getLanguage() for res in results ]
    mid = "</li>\n<li>".join(langs)
    bodyList = ["<li>", mid, "</li>"]
    body = "".join(bodyList)

    return row % (header, body)


def createFractionHTML(num, den):
    float = 0
    if (den != 0):
        float = num / den
    quantifier = floatToQuantifier(float)
    frac = "".join(["<span style='font-size: x-small;'>",
                    "(%d / %d)" % (num, den),
                    "</span>"])
    text =     "".join([quantifier, " languages ", frac])
    tooltip =  "".join(["<span ",
                        "onclick='handleListToggle() '"
                        "data-toggle='tooltip' ",
                        "style='cursor: pointer;'",
                        "title='%d%% of languages matched'" % round(float * 100),
                        ">",
                        text,
                        "</span>"])
    collapse = "".join(["<span ",
                        "data-toggle='collapse'",
                        "data-target='.lang-list'"
                        ">",
                        tooltip,
                        "</span>"])
    return collapse

#############################################################################
#                                Helper Methods
#############################################################################
def floatToQuantifier(frac):
    # TODO Move quantifiers into a data class somewhere so they are more easily moddable
    # NOTE Quantifier lists must be kept sorted!
    """Given a floating point number float in the range 0 to 1, return a quantifier
    string like "all", "nearly all", "few", "no" to represent it"""
    if frac < 0 or frac > 1:
        raise ValueError("Error: Float %f is not in the range [0,1]!" % frac)

    fancyQuantifiers = [
        (0.00, "No"),
        (0.10, "Hardly any"),
        (0.20, "Few"),
        (0.30, "Not many"),
        (0.40, "Some"),
        (0.55, "A lot of"),
        (0.65, "Many"),
        (0.85, "Most"),
        (0.99, "Nearly all"),
        (1.00, "All")
    ]
    succinctQuantifiers = [
        (0.00, "No"),
        (0.10, "Almost no"),
        (0.25, "Very few"),
        (0.40, "Few"),
        (0.60, "About half of"),
        (0.75, "Many"),
        (0.90, "Very many"),
        (0.99, "Almost all"),
        (1.00, "All")
    ]

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
