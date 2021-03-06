"""A collection of helpful functions for manipulating lists of dicts
representing IPA phonemes"""

# ============ Public Functions ============
def unique(ls):
    """Return a list containing the unique elements of the input list. Note that
    the input list must consist of hashable elements"""
    return list(set(ls))

def filter(dataSrc, propertyName, propertyValue):
    """Given dataSrc, a list of dicts representing IPA phonemes, return a subset
    of that list containing only elements such that el[propertyName] == propertyValue"""
    filtered = [p for p in dataSrc if p[propertyName] == propertyValue]
    return filtered

def subtract(a, b):
    """Return a list containing all elements of a, except those in b"""
    result = [p for p in a if p not in b]
    return result

def producible(dataSrc):
    """Given dataSrc, a list of dicts representing IPA phonemes, return a subset
    of that list containing the producible phonemes (i.e. those with valid glyphs)"""
    return filter(dataSrc, "producible", True)

def glyphs(dataSrc):
    """Given dataSrc, a list of dicts representing IPA phonemes, return a list
    containing the glyphs of the producible members of the list"""
    prod = producible(dataSrc)
    glyphs = [p["glyph"] for p in prod]
    return glyphs

def getGlyphsMatching(dataSrc, propertyName, propertyValue):
    """Finds a list of all phonemes from dataSrc such that the phoneme's
    property named propertyName has the value specified by propertyValue. Return
    a list of the glyphs of all matching phonemes"""
    prod = producible(dataSrc)
    filt = filter(prod, propertyName, propertyValue)
    return glyphs(filt)

def enumerateProperty(dataSrc, propertyName):
    """Create a dict mapping the unique values of propertyName to the phoneme glyphs
    satisfying the corresponding property value, using dataSrc as the source of
    phoneme data.

    E.g. enumerateProperty(consonants.data, "voicing") -->
         {"voiced":    ["b", "d", ...],
          "voiceless": ["p", "t", ...]}"""

    # Find all unique values of the given property
    values = unique([p[propertyName] for p in dataSrc])
    dict = {val: getGlyphsMatching(dataSrc, propertyName, val) for val in values}
    return dict

def getGlyphsFromClass(dataSrc, classesDict, propertyValue):
    """Return a list of glyphs from classesDict who are described by propertyValue
    (e.g. plosives, voiced consonants, labiodentals, rounded vowels...).
    If 'any ' appears in propertyValue, return all glyphs in dataSrc instead"""

    if ("any " in propertyValue):
        return glyphs(dataSrc).copy()
    elif propertyValue not in classesDict:
        raise ValueError("Class %s not recognized as a natural class" % propertyValue)
        return [] # control never reaches this line, but whatever
    else:
        return classesDict[propertyValue].copy()

def getGlyphsFromClasses(dataSrc, classesDict, propertyValues):
    """Return a list of glyphs satisfying the intersection of getGlyphsFromClass
    called on every propertyValue (natural class) in propertyValues.
    e.g. "voiced bilabial plosive" --> 'b'  """

    if len(propertyValues) == 0:
        return []

    glyphSet = set(getGlyphsFromClass(dataSrc, classesDict, propertyValues[0]))
    for propertyValue in propertyValues[1:]:
        glyphList = getGlyphsFromClass(dataSrc, classesDict, propertyValue)
        glyphSet = set(glyphList).intersection(glyphSet)

    return list(glyphSet)

def getDataFromGlyph(dataSrc, glyph):
    """Return the phoneme in dataSrc represented by glyph, or None if no such
    phoneme exists"""
    # Doing a linear scan like this is algorithmically slow but "fast enough" in practice
    # If it ever becomes too slow in the future, give consonants.py a dict mapping glyphs to
    # phoneme dicts
    for p in dataSrc:
        if p["glyph"] == glyph:
            return p
    return None
