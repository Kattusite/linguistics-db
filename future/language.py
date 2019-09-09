import json

class InvalidDataError(ValueError):
    """An error indicating that an attempt has been made to construct a Language
    using invalid data"""
    pass

class Language:
    """A Language is a collection of data points summarizing the key phonological,
    morphological, and syntactic features of a language."""

    # Given data, a dict of key-value mappings describing the properties of a
    # language, create a new language.
    def __init__(self, data):
        self.data = data

        # Ensure all required fields are provided
        required = ["language"]
        for req in required:
            if req not in self.data:
                raise InvalidDataError("The required language field %s was not provided" % req)

    def __repr__(self):
        return json.dumps(self.data, ensure_ascii=False, indent=4)

    def __str__(self):
        return "<{} language>".format(self.name())

    def __getattr__(self, name):
        if name in self:
            return self.name
        else if name in self.data:
            return self.data.name
        else:
            raise KeyError("Language has no attribute named '%s'" % name)


    def name(self):
        return self.data.language

    def data(self):
        return self.data
