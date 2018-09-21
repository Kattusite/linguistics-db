# Generate all of the tables needed for front.html, in order

from phonemes import vowels, consonants
from data import const

################################################################################
#                                                                              #
#                        CONSTANTS                                             #
#                                                                              #
################################################################################

indent_lvl = 0    # current indent level
TAB_WIDTH = 2 # spaces per tab

OPEN  = 0   # <body>
CLOSE = 1   # </body>
BOTH  = 2   # <body>...</body>

PBOX_PER_ROW = 5

################################################################################
#                                                                              #
#                        HELPERS                                               #
#                                                                              #
################################################################################

# increase the current indent level
def indent():
    global indent_lvl
    indent_lvl += 1

# decrease the current indent level to a min of 0
def dedent():
    global indent_lvl
    indent_lvl = max(0, indent_lvl-1)

# print str preceded by the current indent level
def tprint(str):
    global indent_lvl
    tab = " " * (TAB_WIDTH * indent_lvl)
    print("%s%s" % (tab, str))

# Wrap str in an HTML tag t and return it, with optional classList
# NOTE this needs a lot of work (making it work w/ indenting, and allowing embedding)
def tag(t, body=None, id=None, classList=None, onclick=None, other=None, type=BOTH):
    # If parameters aren't None, build them into strings
    bodyStr  = body if body else ""
    classStr = ' class="%s"' % " ".join(classList) if classList else ""
    clickStr = ' onclick="%s"' % onclick if onclick else ""
    idStr = ' id="%s"' % id if id else ""

    openTag = "<{0}{1}{2}{3}>{4}".format(t, idStr, classStr, clickStr, bodyStr)
    closeTag = "</{0}>".format(t)

    if type == BOTH:
        return "".join([openTag, closeTag])
    elif type == OPEN:
        return openTag
    elif type == CLOSE:
        return closeTag
    else:
        raise ValueError("Invalid tag type! Must specify either open tag, close tag, or both!")


def comment(com):
    """Wraps com in HTML comment tags and returns it as a string"""
    return "<!--{0}-->".format(com)
################################################################################
#                                                                              #
#                        TABLE GENERATORS                                      #
#                                                                              #
################################################################################

# Use function decorations to print start/end of table
# BUG: wrong syntax
def tablegen(fn, divID):
    tprint(tag("div", id="%s-template" % divID, type=OPEN))
    indent()
    tprint(tag("table", type=OPEN))
    indent()
    tprint(tag("tbody", type=OPEN))
    indent()

    fn()

    dedent()
    tprint(tag("tbody", type=CLOSE))
    dedent()
    tprint(tag("table", type=CLOSE))
    dedent()
    tprint(tag("div", type=CLOSE))

# TODO: Poor style to have "consonant"/"vowel" magic strings
# I propose a constant (int?) consonant.CONSONANT or phoneme.CONSONANT to use
# here instead, and then the str values are mapped from there
def pboxgen(pType, glyphList):
    """Generate the html for a phoneme selector table, using glyphList as source
    glyphList is a str[] containing all valid glyphs. pType is either "consonant"/"vowel"
    depending on whether these are consonants or vowels."""

    abbrev = "cbox" if pType == "consonant" else "vbox"
    tprint("")
    tprint(comment("Auto-generated template for the {0} phoneme selector."
                        .format(pType)))
    tprint(tag("div", id="{0}-template".format(abbrev), type=OPEN))
    indent()
    tprint(tag("table", type=OPEN))
    indent()
    tprint(tag("tbody", type=OPEN))
    indent()

    n = len(glyphList)
    for i, p in enumerate(glyphList):
        # Are we in the last row? If so, special code needed
        # TODO: BUG: Last row may be underfull. Add special cases for this
        # SEVERE BUG: IF last row is underful, closing td tag is omitted!!!
        if i / PBOX_PER_ROW == n / PBOX_PER_ROW: # -1?
            pass # TODO

        # First in new row: print new row and indent
        if i % PBOX_PER_ROW == 0:
            tprint(tag("tr", type=OPEN))
            indent()

        # Add a cell to this row
        tprint(tag("div", body=p, id="{0}-{1}-template".format(pType, p),
                   classList=["pbox-label"], onclick="handlePboxLabel(this)"))

        # Last in row: close row and dedent
        if (i % PBOX_PER_ROW) == PBOX_PER_ROW-1:
            dedent()
            tprint(tag("tr", type=CLOSE))


    dedent()
    tprint(tag("tbody", type=CLOSE))
    dedent()
    tprint(tag("table", type=CLOSE))
    dedent()
    tprint(tag("div", type=CLOSE))

def clboxgen(pType, metaclasses):
    """Generate the html for a natural class selector table, using metaclasses as source.
    metaclasses is a str[][] containing a list of (lists of possible classes for each type).
    pType is either "consonant" or "vowel" depending on the type being used"""
    tprint("")
    tprint(comment("Auto-generated template for the {0} class selector."
                        .format(pType)))

    tprint(tag("div", id="{0}-template".format(pType), type=OPEN))
    indent()
    tprint(tag("table", type=OPEN))
    indent()
    tprint(tag("tbody", type=OPEN))
    indent()

    n = max([len(cls) for cls in metaclasses])

    for i in range(n):
        tprint(tag("tr", type=OPEN))
        indent()
        # Print one element from each of the lists
        # (or a placeholder if the list has ended already)
        for j, metaclass in enumerate(metaclasses):
            htmlClasses = []
            clickFn = None
            b=None

            if i < len(metaclass):
                htmlClasses += ["clbox-label", "clbox-label-%d" % j]
                onclick="handleClboxLabel(this)"
                b=metaclass[i]
            else:
                htmlClasses += ["clbox-label-empty"]

            if i == 0:
                htmlClasses += ["clbox-label-selected"]

            tprint(tag("td", body=b, classList=htmlClasses, onclick=clickFn))

        dedent()
        tprint(tag("tr", type=CLOSE))
    dedent()
    tprint(tag("tbody", type=CLOSE))
    dedent()
    tprint(tag("table", type=CLOSE))
    dedent()
    tprint(tag("div", type=CLOSE))

def lboxgen(lType, otherList):
    """Generate the html for a generic list selector table, using otherList as source.
    lType will be a str containing the name of the property being listed"""
    tprint("")
    tprint(comment("Auto-generated template for the {0} list selector."
                        .format(lType)))

    tprint(tag("div", id="%s-template" % lType, type=OPEN))
    indent()
    tprint(tag("table", type=OPEN))
    indent()
    tprint(tag("tbody", type=OPEN))
    indent()

    for s in otherList:
        tprint(tag("tr", type=OPEN))
        indent()
        tprint(tag("td", body=s, classList=["lbox-label"], onclick="handleLboxLabel(this)"))
        dedent()
        tprint(tag("tr", type=CLOSE))

    dedent()
    tprint(tag("tbody", type=CLOSE))
    dedent()
    tprint(tag("table", type=CLOSE))
    dedent()
    tprint(tag("div", type=CLOSE))

def ipacboxgen(glyphList):
    """Generate the html for a IPA consonant chart table, using glyphList as source"""

def ipavboxgen(glyphList):
    """Generate the html for a IPA vowel chart table, using glyphList as source"""


################################################################################
#                                                                              #
#                        MAIN                                                  #
#                                                                              #
################################################################################

def main():
    tprint(comment("  ### BEGIN AUTO-GENERATED HTML. DO NOT EDIT ###"))

    # Generate phoneme selectors
    pboxgen("cbox", consonants.GLYPHS)
    pboxgen("vbox", vowels.GLYPHS)

    # Generate phoneme class selectors
    clboxgen("consonant", consonants.CLASS_MATRIX)
    clboxgen("vowel", vowels.CLASS_MATRIX)

    # Generate general list selectors
    lboxgen("morphology", const.MORPHOLOGY_DICT.keys())
    lboxgen("word-formation", const.WORD_FORMATION_DICT.keys())
    lboxgen("formation-freq", const.FORMATION_DICT.keys())
    lboxgen("word-order", const.WORD_ORDER_DICT.keys())
    lboxgen("headedness", const.HEADEDNESS_DICT.keys())
    lboxgen("agreement", const.CASE_AGREEMENT_DICT.keys())
    lboxgen("case", const.CASE_AGREEMENT_DICT.keys())

    tprint(comment("  ### END AUTO-GENERATED HTML. EDITING IS OK AGAIN ###"))
