from .language import Language
from data.const import *
import json, inspect

# LingDB class
class LingDB:
    """An object encapsulating useful lingDB queries and properties. A
    collection of language objects"""

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
    # or returns a True type (ie a nonempty list), append that language's results
    # to a list.
    # Return the entire list after all matching languages have contributed results
    def query(self, fn, allArgs):
        # Get the argument list for the selected function # WARNING (hacky)
        argList = inspect.getargspec(fn)[0][1:]
        argsToPass = [allArgs[a] for a in argList]
        return [lang for lang in self.data if fn(lang, *argsToPass)]

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
