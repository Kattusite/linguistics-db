from .language import Language
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
    QUERY_LANG = 0
    QUERY_RESULT = 1

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
    # Return the entire list of tuples after all matching languages have
    # contributed results
    def query(self, fn, allArgs):
        # Get the argument list for the selected function # WARNING (hacky)
        # Be careful: this gets the VARIABLE NAME attached to a given fn argument
        # so it is sensitive to changes in names of variables, not just types

        argList = inspect.getargspec(fn)[0][1:]
        argsToPass = [allArgs[a] for a in argList]

        # For each language that matches this query, return a tuple of the
        # matching language, and the list of properties in the language that matched
        matches = []  # Array of (lang, result) tuples
        for lang in self.data:
           queryResult = fn(lang, *argsToPass)

           # Check if query result is an empty list or other falsey type
           if queryResult:
              # Convert result lists to tuples so we can hash them (and make sets!)
              if type(queryResult) == type([]):
                  queryResult = tuple(queryResult)

              matches.append((lang, queryResult))

        return matches
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
