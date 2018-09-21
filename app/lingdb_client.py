#############################################################################
#       lingdb_client.py
#
#############################################################################

import os, re
from lingdb import LingDB, Language
from phonemes import vowels, consonants
from data import language_data
import phonemes

# Substitute Database objects
# (can be replaced with an actual DB later if the overhead is justified.
# Construct LING_DB
def init_DB():
    global LING_DB
    LING_DB = LingDB(language_data)
    # TODO integrate typology data from TYPOLOGY_FILE

# TODO This is a terrible piece of code. Fix it so this doesn't get reinitialized all the time
LING_DB = None
init_DB()


def handleQuery(query):
    """Given a query dict, decide which type of query has been made, and return a
    list of results corresponding to the languages matching that type of query"""
    trait = query["trait"]

    # Map each query string to its function and that function's arguments
    function_map = {
        "consonant-selector":           Language.containsConsonants,
        "consonant-class-selector":     Language.containsConsonantClasses,
        "vowel-selector":               Language.containsVowels,
        "vowel-class-selector":         Language.containsVowelClasses,
        "consonant-places":             Language.containsConsonantPlaces,
        "consonant-manners":            Language.containsConsonantManners,
        "complex-consonant":            Language.containsComplexConsonants,
        "tone-selector":                Language.containsTone,
        "stress-selector":              Language.containsStress,
        "syllable-selector":            Language.containsSyllable
    }

    fn = function_map[trait]
    return LING_DB.query(fn, query)

def handleQueries(queries, listMode):
    """Process multiple queries and direct them as appropriate, according to the
    trait each one represents."""
    # Can be cleaned up with comprehensions
    result_arr = []   # List of sets of Languages
    reply_arr  = []   # List of strings (?)

    # Obtain a list of the languages matching each query
    for query in queries:
        r = handleQuery(query)
        s = set(r)  # The set of all language objects that matched
        reply_arr.append(query["reply"])
        result_arr.append(s)

    n = len(result_arr)
    if n == 0:
        print("Error: attempted to handle invalid query")
        return None # Query invalid

    # Combine the results
    # TODO Clean this whole section up (add HTML styling + a separate formatter function)
    # langStr = " languages "

    nlStr   = "\n<br>\n"
    hrStr   = "\n<hr>\n"

    # TODO allow AND, OR, etc. to be selected as a request field, not hardcoded
    # TODO Magic numbers 0, 1, 2 are bad
    # TODO also allow for displaying the results of each subquery alone--
    # If I query for A & B & C, also display just A, just B, just C.
    # TODO also add a small table with a list of languages matching just A, just B, or A and B
    uRep = createUnionReply(result_arr, reply_arr, LING_DB)
    iRep = createIntersectionReply(result_arr, reply_arr, LING_DB)
    cRep = createConditionalReply(result_arr, reply_arr, 0, LING_DB)

    # The response structure partitions results with newlines and horizontal rules
    # so that the data is returned in a nice format
    response = {
        "logical":          [],
        "implicational":    [],
        "list":             []
    }

    if listMode:
        orderedResults = [sorted(list(s), key=lambda x: x.getLanguage()) for s in result_arr]
        cmpRep = createComparisonTable(orderedResults, reply_arr)
        response["list"].append(cmpRep)

    if n >= 1:
        response["logical"].append(uRep)   # A (or B (or C...))
    if n >= 2:
        response["logical"].append(iRep)   # A (and B (and C...))
        response["implicational"].append(cRep)   # A --> B

        # If exactly two query terms, throw in B --> A
        if n == 2:
            cRep2 = createConditionalReply(result_arr, reply_arr, 1, LING_DB)
            response["implicational"].append(cRep2)

    # Format the response structure with newlines and rules
    sections = []
    # NOTE More elegant way?
    sections.append(nlStr.join(response["logical"]))
    sections.append(nlStr.join(response["implicational"]))
    sections.append(nlStr.join(response["list"]))

    # Filter out empty strings (sections without any content added)
    sections = [s for s in sections if len(s) > 0]

    return hrStr.join(sections)


#############################################################################
#                          Formatted Reply Methods
#############################################################################

def mergeReplies(replies, joinWord):
    """Join together the strings in replies, using joinWord as a semantic separator
    (e.g. "and", "or")"""
    # TODO implement this for more modularity in the createReply functions
    return NotImplemented

def createUnionReply(results, replies, db):
    """Return a string of HTML representing the formatted results to be
    displayed for the given results list and replies list, and containing db,
    assuming the queries are joined together using union (OR)"""
    matches = [x.getLanguage() for x in set.union(*results)]
    num = len(matches)
    den = len(db)
    reply = "".join(["<b>", "</b> or <b>".join(replies), "</b>"])
    frac  = createFractionHTML(num, den)
    return " ".join([frac, reply])

def createIntersectionReply(results, replies, db):
    """Return a string of HTML representing the formatted results to be
    displayed for the given results list and replies list, and containing db,
    assuming the queries are joined together using intersection (AND)"""
    matches = [x.getLanguage() for x in set.intersection(*results)]
    num = len(matches)
    den = len(db)
    reply = "".join(["<b>", "</b> and <b>".join(replies), "</b>"])
    frac  = createFractionHTML(num, den)
    return " ".join([frac, reply])

def createConditionalReply(results, replies, which, db):
    """Return a string of HTML representing the formatted results to be
    displayed for the given results list and replies list, and containing db,
    assuming the queries are joined together using conditional (R[which] implies R[1,2,3,...])
    The parameter which specifies the index of the item implying the others"""
    matches = [x.getLanguage() for x in set.intersection(*results)]
    num = len(matches)
    den = len(results[which])
    ifReply   = "".join([" that <b>", replies[which], "</b> also "])
    thenReply = "".join(["<b>", "</b> and <b>".join(replies[:which] + replies[which+1:]), "</b>"])
    frac  = createFractionHTML(num, den)
    condStr = " ".join([frac, ifReply, thenReply])
    return condStr

# TODO rename to create lang list
# TODO Sort the languages!!
def createComparisonTable(results, replies):
    # Define table template
    table = """
    <table>
        <tbody>
            <tr>%s</tr>
        </tbody>
    </table>"""

    # Define the columns
    hideHeaders = len(results) <= 1
    cols = "".join([createComparisonRow(results[i], replies[i], hideHeaders) for i in range(len(results))])
    print(len(results), hideHeaders)
    return table % cols



def createComparisonRow(result, reply, hideHeaders):
    header = "" if hideHeaders else str(len(result)) + " languages " + reply
    row = """
    <td>
        <h5>%s</h5>
        <ul>
            %s
        </ul>
    </td>"""

    mid = "</li>\n<li>".join([lang.getLanguage() for lang in result])
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
    text = "".join([quantifier, " languages ", frac])
    ret  = "".join(["<span ",
                    "data-toggle='tooltip' ",
                    "title='%d%% of languages matched'" % round(float * 100),
                    ">",
                    text,
                    "</span>"])
    return ret


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
        (0.60, "About half"),
        (0.75, "Many"),
        (0.90, "Very many"),
        (0.99, "Almost all"),
        (1.00, "All")
    ]

    for quant in succinctQuantifiers:
        if frac <= quant[0]:
            return quant[1]

    raise ValueError("No valid quantifier provided for float %f!" % frac)


#############################################################################
#                                Query Methods
#############################################################################
def queryForConsonants(query):
    # init_DB()
    # return consonants + " " + k
    cons = query["consonants"]
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsConsonants(cons, k, mode)
    return matches

def queryForConsonantClasses(query):
    classArr = query["classes"]
    bitstring = phonemes.consonants.getBitstringFromClasses(classArr)
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsConsonants(bitstring, k, mode)
    return matches

def queryForVowels(query):
    vowels = query["vowels"]
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsVowels(vowels, k, mode)
    return matches

def queryforVowelClasses(query):
    classArr = query["classes"]
    bitstring = phonemes.vowels.getBitstringFromClasses(classArr)
    k = int(query["k"])
    mode = query["mode"]
    matches = LING_DB.queryContainsVowels(bitstring, k, mode)
    return matches

def queryForConsonantPlaces(query):
    matches = LING_DB.queryContainsConsonantPlaces()
    return matches

def queryForConsonantManners(query):
    matches = LING_DB.queryContainsConsonantManners()
    return matches

def queryForComplexConsonants(query):
    matches = LING_DB.queryContainsComplexConsonants()
    return matches

def queryForTone(query):
    matches = LING_DB.queryContainsTone()
    return matches

def queryForStress(query):
    matches = LING_DB.queryContainsStress()
    return matches

def queryForSyllable(query):
    syllable = query["syllable"]
    matches = LING_DB.queryContainsSyllable(syllable)
    return matches

#############################################################################
#                                Helper Methods
#############################################################################
# Reconstruct the consonant glyphs provided in the given consonant bitstring
# This function is deprecated (I'm not sure what it was ever useful for, and it's outdated)
"""
def getConsonantGlyphsFromBitstring(consonants):
    # init_DB()
    results = []
    for i, c in enumerate(consonants):
        if c == "1":
            results.append(CONSONANT_GLYPHS[i])
    return results
"""
