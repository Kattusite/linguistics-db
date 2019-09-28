import copy, json
from collections.abc import Sequence

import tinydb

from data import const
from .language import Language

class InvalidModeError(ValueError):
    pass

# TODO: Add a desc field (formerly "reply").
# Add a default desc for each type, and accept an optional named param to
# set a new one.
# e.g. for lists: "has {mode} {k} of {ls}"
# e.g. for strings: "has a {property} {mode} {value}"
# e.g. for numbers: "has a {property} {mode} {k}"
# e.g. for bools : "has {property} equal to {value}"

LIST    = const.LIST
NUM     = const.NUM
STRING  = const.STRING
BOOL    = const.BOOL
ALWAYS  = "Always"
NEVER   = "Never"

"""A list of human-readable descriptions that will be sent as replies to the
end-user. Typically the message to the user will be of the form:
"<X> languages <desc>", where desc will be something like
"have at least 3 consonants".

Each desc is a format string to be used with str.format(), along with a dictionary
of the values to be inserted into it.

"have {mode} {k} of {ls}".format({"mode": "at least", "k": 2, "ls": ["p","t","k"]})
"""


defaultDesc = {
    LIST: "have {mode} {k} of {ls}",
    NUM: "have a {property} of {mode} {k}",
    STRING: "have a {property} of {value}",
    BOOL: "have a {property} of {value}",
}

# Comparison modes
EQ  = "exactly"       # Match if the number of phoneme matches == target
GEQ = "at least"      # Match if the number of phoneme matches >= target
GT  = "more than"     # Match if the number of phoneme matches  > target
LEQ = "at most"       # Match if the number of phoneme matches <= target
LT  = "less than"     # Match if the number of phoneme matches  < target
NEQ = "not equal to"  # Match if the number of phoneme matches != target
ALL = "all"

def intersect(lsA, lsB):
    """Given two lists lsA, lsB, intersect will return a list containing those
    elements common to both lists"""
    return list(set(lsA).intersection(set(lsB)))

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

def createMatches(matchingLangs, causes, db, query):
    """Given a list of matching languages and a list of causes, one for each
    matching language, return a Matches object, whose list of Match objects is s.t.
        matches[i] = Match(matchingLangs[i], causes[i])"""

    matches = [Match(lg, cs) for lg, cs in zip(matchingLangs, causes)]

    return Matches(matches, db, query)

class Match:
    """A match object stores a Language that matched a query, along with
    the specific properties of that language that caused it to match.

    It is intended to  simplify APIs and signatures.
    e.g. "returns a list of list of Match objects" instead of
    "returns a list of lists of (Language, cause) tuples".

    It also allows for fields or convenience methods to be added later on without
    messing with client code.
    """

    def __init__(self, lg, cause):
        self.language = lg
        self.cause = cause

    def __str__(self):
        # TODO improve
        return str(self.language) + ": " + str(self.cause)

    def __repr__(self):
        return self.__str__()

class Matches(Sequence):
    """A Matches object is simply a sequence of Match objects.

    We can define several convenience methods on this type (TODO).

    A Matches object also stores a reference to the db and query that generated it.
    """

    def __init__(self, matches, db, query):
        self.matches = matches
        self.db = db
        self.query = query
        super().__init__()

    def __getitem__(self, i):
        return self.matches[i]

    def __len__(self):
        return len(self.matches)

    def __str__(self):
        # TODO improve
        return str(self.matches)

    def __repr__(self):
        return self.__str__()

    def languageSet(self):
        """Return a set of all the languages associated with matches in self.matches"""
        return set([m.language for m in self.matches])

class Query:
    """A Query is in simplest form a function on a language, which returns true if the
    query is satisfied on that language, and false if the query is not satisfied on
    that language.

    The query.Query class acts as the ancestor for all other query classes."""

    def __init__(self):
        self.descStr = "<Base Query - undefined parameters>"

        # TODO: Insert value into the property name if possible
        # e.g. property == "num {value}" ==> "num consonants"
        # TODO: must call super.__init__() from every init
        # if self.property and self.value:
        #     self.property = self.property.format({"value": self.value})

    def __str__(self):
        """Return a human-readable description of what it would take for this
        query to be satisfied; for example, a List query might look like:
        "{n} languages contain {mode} {k} of {ls}".
        """
        return self.descStr()

    def __repr__(self):
        """Return a complete description of the fields of this query."""
        t = type(self)
        data = json.dumps(vars(self), indent=2)
        return "{0} query:\n{1}".format(t, data)

    def desc(self):
        """Return a copy of the query's desc field, with all placeholders
        replaced by their actual values for this query.

        e.g. if the raw desc property is "has {mode} {k} of {ls}",
        desc() may return "has at least 2 of p, t, k".

        Note that desc() also reformats lists so they are closer to plain English;
        in particular, enclosing square brackets are omitted, as are quotes
        around string literals."""

        # Create a deepcopy of vars to avoid modifying the original query
        params = copy.deepcopy(vars(self))

        # Convert literal lists to simplified string representations
        if "ls" in params:
            params["ls"] = ", ".join(params["ls"])

        return self.descStr.format(**params)

class List(Query):
    """Query.List is a class defining the properties of a list based query from
    the user to the database.
    A List query is of the form "at least 2 of [x,y,z]",
    or "exactly 0 of [p,q,r,s]"."""

    def __init__(self, property, mode, k, ls, desc=defaultDesc[LIST]):
        """Create a List based query using the given mode, k, and ls. Mode is
        one of the constants defined in data.const; e.g. GREATER_THAN, LESS_THAN,
        EQUAL, .... K specifies the modifier for this mode; e.g. "less than K".
        ls defines the list on which the mode and k operate; e.g. "at least K of
        ls=[a,b,c,...]". """

        if mode not in [ EQ, NEQ, GT, LT, GEQ, LEQ, ALL ]:
            raise InvalidModeError("'%s' is not a valid mode for list queries!" % mode)

        if type(k) != type(0):
            raise TypeError("'%s' is not a valid integer K for list queries!" % k)

        if type(ls) != type([]):
            raise TypeError("'%s' is not a valid list for list queries!" % ls)

        # Special case: allow lists of properties to signify "meta" properties
        # that are a concatenation of several other existing properties
        if type(property) != type("") and type(property) != type([]):
            raise TypeError("'%s' is not a valid property for list queries!" % property)

        self.property = property
        self.mode = mode
        self.k = k
        self.ls = ls

        self.descStr = desc
        self.type = LIST

    def query(self, db):
        """Execute this query on the specified database, returning the status code
        and results.

        Results will be returned as a list of Match objects, each containing
        the matching language and the data that caused that language to qualify.

        For example, if we query for a language with at least 3 consonants,
        the cause would be a list of all consonants in the matching language."""

        Lang = tinydb.Query()

        # Special case for "meta" properties consisting of several concatenated properties
        if type(self.property) == type([]):
            matches = db.search(Lang.test(self.metatest))
            matchingLangs = [Language(m) for m in matches]

            causes = []
            for lang in matchingLangs:
                lgCauses = []
                for metaprop in self.property:
                    lgCauses += intersect(getattr(lang, self.property), self.ls)
                causes.append(lgCauses)
            return createMatches(matchingLangs, causes, db, self)

        matches =  db.search(Lang[self.property].test(self.test))
        matchingLangs = [Language(m) for m in matches]

        # Extract the second tuple entry explaining which values caused each
        # language to match.
        causes = [intersect(getattr(lang, self.property), self.ls) for lang in matchingLangs]

        # Combine each matching langage with its cause
        return createMatches(matchingLangs, causes, db, self)

    def test(self, ls):
        """A method to be passed to TinyDB's .test() method to check whether a
        given list ls matches the parameters defined by this query."""

        intersection = intersect(ls, self.ls)
        return compareByMode(self.mode, len(intersection), self.k)

    def metatest(self, lg):
        """A method to be passd to TinyDB's .test() method to check whether a
        given language lg matches the parameters defined by this special query."""

        sets = [set(lg[metaprop]) for metaprop in self.property]
        features = set.union(*sets)
        intersection = intersect(ls, self.ls)

        return compareByMode(self.mode, len(intersection), self.k)

class Num(Query):
    """Query.Num is a class defining the properties of a numerical query from the
    user to the database.
    A Num query is of the form "Property 'num consonants' has value at least 4",
    or "Property 'num phonemes' has value at most 7"."""

    def __init__(self, property, mode, k, desc=defaultDesc[NUM]):
        """Create a Number based query comparing the value of the given property
        to the provided k value using the given mode.
        Can be read as 'Does property have a value of <comparison mode> k?'"""

        if mode not in [ EQ, NEQ, GT, LT, LEQ, GEQ ]:
            raise InvalidModeError("'%s' is not a valid mode for numerical queries!" % mode)

        if type(k) != type(0):
            raise TypeError("'%s' is not a valid integer K for numerical queries!" % k)

        if type(property) != type(""):
            raise TypeError("'%s' is not a valid property for numerical queries!" % property)

        self.mode = mode
        self.k = k
        self.property = property

        self.descStr = desc
        self.type = NUM

    def query(self, db):
        """Execute this query on the specified database, returning the status code
        and results.

        Results will be returned as a list of Match objects.
        For Num queries, the cause field will be the specific numerical value
        of the relevant property for the matching language."""

        Lang = tinydb.Query()
        matches = db.search(Lang[self.property].test(self.test))
        matchingLangs = [Language(m) for m in matches]

        causes = [getattr(lang, self.property) for lang in matchingLangs]

        # Combine each matching langage with its cause
        return createMatches(matchingLangs, causes, db, self)

    def test(self, n):
        return compareByMode(self.mode, n, self.k)

class String(Query):
    """Query.String is a class defining the properties of a string-based query
    from the user to the database.
    A String query is of the form "Property 'country' is equal to 'Ecuador'."""

    def __init__(self, property, mode, value, desc=defaultDesc[STRING]):
        """Create a String based query comparing the value of the given property
        to the provided value using the given mode.
        Only == and != are supported as modes for string based queries."""

        if mode not in [ EQ, NEQ ]:
            raise InvalidModeError("'%s' is not a valid mode for string queries!" % mode)

        if type(value) != type(""):
            raise TypeError("'%s' is not a valid value for string queries!" % value)

        if type(property) != type(""):
            raise TypeError("'%s' is not a valid property for string queries!" % property)

        self.mode = mode
        self.value = value
        self.property = property

        self.descStr = desc
        self.type = STRING

    def query(self, db):
        """Execute this query on the specified database, returning the status code
        and results.

        Results will be returned as a list of Match objects.
        For String queries, the cause will be the specific string value of
        the relevant property for the matching language."""

        Lang = tinydb.Query()
        matches = db.search(Lang[self.property].test(self.test))
        matchingLangs = [Language(m) for m in matches]

        causes = [getattr(lang, self.property) for lang in matchingLangs]

        # Combine each matching langage with its cause
        return createMatches(matchingLangs, causes, db, self)

    def test(self, s):
        return compareByMode(self.mode, s, self.value)

class Bool(Query):
    """Query.String is a class defining the properties of a boolean-based query
    from the user to the database.
    A Bool query is of the form "Property 'tone' is equal to 'True'",
    which might have a reply of the form:
    "X languages have tone."
    """

    def __init__(self, property, value, desc=defaultDesc[BOOL]):

        if value is None:
            value = True

        if type(value) != type(True):
            raise TypeError("%s is not a valid value for a boolean query" % value)

        if type(property) != type(""):
            raise TypeError()

        self.property = property
        self.value = value
        self.mode = EQ

        self.descStr = desc
        self.type = BOOL

    def query(self, db):
        """Execute this query on the specified database, returning the status code
        and results.

        Results will be returned as a list of Match objects.
        For Bool queries, the cause will always be None."""

        Lang = tinydb.Query()
        matches = db.search(Lang[self.property].test(self.test))
        matchingLangs = [Language(m) for m in matches]

        causes = [None for m in matches]

        # Combine each matching langage with its cause
        return createMatches(matchingLangs, causes, db, self)

    def test(self, b):
        return compareByMode(self.mode, b, self.value)


class Always(Query):
    """Query.Always is a class defining a query that returns success for all
    languages in the database unconditionally.

    Results will be returned as a list of Match objects.
    For Always queries, the cause will always be None"""
    def query(self, db):
        matches = db.all()
        matchingLangs = [Language(m) for m in matches]
        causes = [None for lang in matchingLangs]
        # Combine each matching langage with its cause
        return createMatches(matchingLangs, causes, db, self)

class Never(Query):
    """Query.Never is a class defining a query that returns failure for all
    languages in the database unconditionally.

    The Never query only ever returns an empty list.
    (i.e. a list of zero Match objects)"""
    def query(self, db):
        return createMatches([], [], db, self)
