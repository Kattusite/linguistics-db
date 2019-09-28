import json

class InvalidDataError(ValueError):
    """An error indicating that an attempt has been made to construct a Language
    using invalid data"""
    pass

class Language:
    """A Language is a collection of data points summarizing the key phonological,
    morphological, and syntactic features of a language."""

    def __init__(self, data):
        """Initialize a new language using a complete dictionary 'data' of
        key-value mappings enumerating the properties of that language."""
        self.data = data

        # Ensure all required fields are provided
        required = ["name", "student", "netid"]
        for req in required:
            if req not in self.data:
                raise InvalidDataError("The required language field %s was not provided" % req)

    def __repr__(self):
        """Return a detailed representation of the language's entire data"""
        return json.dumps(self.data, ensure_ascii=False, indent=4)

    def __str__(self):
        """Return a succinct representation of the language's name"""
        return "<{} language>".format(self.name())

    def __getattr__(self, attr):
        """Get the attribute described by name, searching first in the top-level
        for the language, then in the language's data."""
        if attr in vars(self):
            return vars(self)[attr]
        elif attr in self.data:
            return self.data[attr]
        else:
            raise KeyError("Language has no attribute named '%s'" % attr)

    def __hash__(self):
        """Return a hash of this language based on the name of the language and
        student maintainer"""
        return hash((self.name(), self.student(), self.netid()))

    def name(self):
        """Return the name of this language"""
        return self.data["name"]

    def student(self):
        """Return the name of the student responsible for this language's data"""
        return self.data["student"]

    def netid(self):
        """Return the netid of the student responsible for this language's data"""
        return self.data["netid"]

    def data(self):
        """Return the raw data for this language, as a dictionary"""
        return self.data
