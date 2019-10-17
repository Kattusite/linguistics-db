from .language import Language
from .exceptions import *
from data.const import *
import json, inspect


# LingDB class
class LingDB:
    """An object encapsulating useful lingDB queries and properties. A
    collection of language objects"""

################################################################################
#                             Constants                                        #
#                                                                              #
################################################################################
    # move these constants for the module? tbd
    QUERY_LANG = 0
    QUERY_RESULT = 1

    # What proportion of langs must have data for a query to be valid?
    QUORUM_THRESHOLD = 0.5
    MATCHES = 'matches'
    NO_DATA = 'no data'


################################################################################
#                             Constructor                                      #
#                                                                              #
################################################################################
    def __init__(self, jsonArr):
        """Create a lingdb from an array of objects (dicts) read from json
        with the format described in data/csvtojson.py"""
        self.data = []
        for jsonObj in jsonArr:
            self.data.append(Language(jsonObj))


################################################################################
#                            Getter Methods                                    #
#                                                                              #
################################################################################

    def size(self):
        """Return the number of language entries represented in this db"""
        return len(self.data)

################################################################################
#                             Query Methods                                    #
#   (these appear largely redundant; directly use language methods instead? )  #
################################################################################

    # This one is tricky. Where fn is a *function* (not a method) from the
    # Language class, and args is a list of args to be passed to that function,
    # apply fn to all languages lang in the DB. Then if lang.fn(*args) is True,
    # or returns a True type (ie a nonempty list), this language is added to a
    # tuple, containing 1) the language that matched and 2) the return value of
    # lang.fn
    # At the end, return a dict with MATCHES keyed to the entire list of tuples
    # after all matching languages have contributed results,
    # and NO_DATA keyed to the list of languages that were unable to contribute
    # results due to a lack of data.
    def query(self, fn, allArgs):
        # Get the argument list for the selected function # WARNING (hacky)
        # Be careful: this gets the VARIABLE NAME attached to a given fn argument
        # so it is sensitive to changes in names of variables, not just types

        argList = inspect.getargspec(fn)[0][1:]
        argsToPass = [allArgs[a] for a in argList]

        # For each language that matches this query, return a tuple of the
        # matching language, and the list of properties in the language that matched
        matches = []  # Array of (lang, result) tuples
        langsWithoutData = []   # Array of langs (those without data)

        # Query each language individually and get their data if they have any
        for lang in self.data:

            hasData = True      # Does lang have any data for this query?
            try:
                queryResult = fn(lang, *argsToPass)
            except NoLanguageDataError:
                queryResult = None
                hasData = False
                langsWithoutData.append(lang)

            # Avoid treating "no data" as a confirmation of a negative result
            if not hasData:
                continue

            # Check if query result is an empty list or other falsey type
            if queryResult:
                # Convert result lists to tuples so we can hash them (and make sets!)
                if type(queryResult) == type([]):
                    queryResult = tuple(queryResult)

                matches.append((lang, queryResult))

        # If no data for more than half of langs, something is wrong.
        # (Perhaps csvtojson failed, or query is malformed)
        if len(langsWithoutData) >= (len(self.data) * LingDB.QUORUM_THRESHOLD):
            raise QuorumError("Too many languages lacked data for a query!")

        return { LingDB.MATCHES: matches, LingDB.NO_DATA: langsWithoutData }
        # return [lang for lang in self.data if fn(lang, *argsToPass)]

################################################################################
#                            Built-ins                                    #
#                                                                              #
################################################################################
    def __repr__(self):
        return __str__(self)

    def __str__(self):
        return json.dumps(self.data)

    def __len__(self):
        return self.size()
