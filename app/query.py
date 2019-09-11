import tinydb

from data import const

class InvalidModeError(ValueError):
    pass

class InvalidKError(ValueError):
    pass

class InvalidLsError(ValueError):
    pass

class InvalidPropertyError(ValueError):
    pass

LIST = "List"
NUM = "Num"
STRING = "String"

# Comparison modes
EQ  = "exactly"       # Match if the number of phoneme matches == target
GEQ = "at least"      # Match if the number of phoneme matches >= target
GT  = "more than"     # Match if the number of phoneme matches  > target
LEQ = "at most"       # Match if the number of phoneme matches <= target
LT  = "less than"     # Match if the number of phoneme matches  < target
NEQ = "not equal to"  # Match if the number of phoneme matches != target
ALL = "all"

"""A Query is in simplest form a function on a language, which returns true if the
query is satisfied on that language, and false if the query is not satisfied on
that language."""

def intersect(lsA, lsB):
    """Given two lists lsA, lsB, intersect will return a list containing those
    elements common to both lists"""
    return list(set(lsA).intersect(set(lsB)))

def compareByMode(mode, a, b):
    """Compare two values a,b using the comparison function specified by
    the provided string 'mode'."""
    comp = {
        LT:     (lambda a, b: a < b),
        GT:     (lambda a, b: a > b),
        GEQ:    (lambda a, b: a >= b),
        LEQ:    (lambda a, b: a <= b),
        EQ:     (lambda a, b: a == b),
        NEQ:    (lambda a, b: a != b),
    }
    if mode not in comp:
        raise KeyError("compareByMode: unrecognized mode '%s'" % mode)
    return comp[mode](a, b)

class List:
    """Query.List is a class defining the properties of a list based query from
    the user to the database.
    A List query is of the form "at least 2 of [x,y,z]",
    or "exactly 0 of [p,q,r,s]"."""

    def __init__(self, property, mode, k, ls):
        """Create a List based query using the given mode, k, and ls. Mode is
        one of the constants defined in data.const; e.g. GREATER_THAN, LESS_THAN,
        EQUAL, .... K specifies the modifier for this mode; e.g. "less than K".
        ls defines the list on which the mode and k operate; e.g. "at least K of
        ls=[a,b,c,...]". """

        if mode not in const.modes:
            raise InvalidModeError("'%s' is not a valid mode for list queries!" % mode)

        if type(k) != type(0):
            raise InvalidKError("'%s' is not a valid integer K for list queries!" % k)

        if type(ls) != type([]):
            raise InvalidLsError("'%s' is not a valid list for list queries!" % ls)

        if type(property) != type(""):
            raise InvalidLsError("'%s' is not a valid property for numerical queries!" % property)

        self.property = property
        self.mode = mode
        self.k = k
        self.ls = ls
        self.type = LIST

    def query(self, db):
        """Execute this query on the specified database, returning the status code
        and results.

        Results will be returned as a tuple where the first element is the entire
        data of the matching language, and the second element is a list of the
        specific list elements that language had that allowed it to satisfy
        this query. For example, if we query for a language with at least 3
        consonants, the second tuple entry would be a list of all consonants in
        the matching language."""

        Lang = tinydb.Query()
        matchingLangs = db.search(Lang[self.property].test(self.test))

        # Extract the second tuple entry explaining which values caused each
        # language to match.
        causes = [intersect(lang[self.property], self.ls) for lang in matchingLangs]

        # Combine each matching langage with its cause
        results = zip(matchingLangs, causes)

    def test(self, ls):
        """A method to be passed to TinyDB's .test() method to check whether a
        given list ls matches the parameters defined by this query."""

        intersection = intersect(ls, self.ls)
        return compareByMode(len(intersection), self.k)


class Num:
    """Query.Num is a class defining the properties of a numerical query from the
    user to the database.
    A Num query is of the form "Property 'num consonants' has value at least 4",
    or "Property 'num phonemes' has value at most 7"."""

    def __init__(self, property, mode, k):
        """Create a Number based query comparing the value of the given property
        to the provided k value using the given mode.
        Can be read as 'Does property have a value of <comparison mode> k?'"""

        if mode not in const.modes:
            raise InvalidModeError("'%s' is not a valid mode for numerical queries!" % mode)

        if type(k) != type(0):
            raise InvalidKError("'%s' is not a valid integer K for numerical queries!" % k)

        if type(property) != type("")
            raise InvalidLsError("'%s' is not a valid property for numerical queries!" % property)

        self.mode = mode
        self.k = k
        self.property = property
        self.type = NUM

    def query(self, db):
        """Execute this query on the specified database, returning the status code
        and results.

        Results will be returned as a tuple where the first element is the entire
        data of the matching language, and the second element is the specific
        value that language had for this query's property."""

        Lang = tinydb.Query()
        matchingLangs = db.search(Lang[self.property]).test(self.test)

        causes = [lang[query.property] for lang in matchingLangs]

        return zip(matchingLangs, causes)

    def test(self, n):
        return compareByMode(self.mode, n, self.k)

class String:
    """Query.String is a class defining the properties of a string-based query
    from the user to the database.
    A String query is of the form "Property 'country' is equal to 'Ecuador'."""

    def __init__(self, property, mode, value):
        """Create a String based query comparing the value of the given property
        to the provided value using the given mode.
        Only == and != are supported as modes for string based queries."""

        if mode not in [const.EQUAL, const.NOT_EQUAL]:
            raise InvalidModeError("'%s' is not a valid mode for string queries!" % mode)

        if type(value) != type(""):
            raise InvalidKError("'%s' is not a valid value for string queries!" % value)

        if type(property) != type("")
            raise InvalidLsError("'%s' is not a valid property for string queries!" % property)

        self.mode = mode
        self.value = value
        self.property = property
        self.type = STRING

    def query(self, db):
        """Execute this query on the specified database, returning the status code
        and results.

        Results will be returned as a tuple where the first element is the entire
        data of the matching language, and the second element is the specific value
        that language had for this query's specified property."""

        Lang = tinydb.Query()
        matchingLangs = db.search(Lang[self.property].test(self.test))

        causes = [lang[query.property] for lang in matchingLangs]
        return zip(matchingLangs, causes)

    def test(self, s):
        return compareByMode(self.mode, s, self.value)

class Always:
    """Query.Always is a class defining a query that returns success for all
    languages in the database unconditionally.

    Results will be returned as a tuple where the first element is the entire
    data of the matching language, and the second element is None."""
    def query(self, db):
        matchingLangs = db.all()
        causes = [None for lang in matchingLangs]
        return zip(matchingLangs, causes)

class Never:
    """Query.Never is a class defining a query that returns failure for all
    languages in the database unconditionally.

    This query never returns any results."""
    def query(self, db):
        return []
