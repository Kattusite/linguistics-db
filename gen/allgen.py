# Generate all of the tables needed for front.html, in order
#
# Usage:
#   From cmd line in project root: (type in cmd after $)
#        > linguistics-db/ $ set PYTHONIOENCODING=utf-8
#        > linguistics-db/ $ python -m gen > gen/out.html

from phonemes import vowels, consonants
from data import const



################################################################################
#                                                                              #
#                        CONSTANTS                                             #
#                                                                              #
################################################################################

indent_lvl = 0    # current indent level
TAB_WIDTH = 2     # spaces per indentation level

OPEN  = 0   # <body>
CLOSE = 1   # </body>
BOTH  = 2   # <body>...</body>

ROW_SZ = 5  # How many columns per row in pboxgen

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
#                        SELECTOR GENERATORS                                   #
#                                                                              #
################################################################################

# Prints a k-selector
def kselectorgen():
    return

# Prints a mode selector
def modeselectorgen():
    return

# Prints a popover
def popovergen():
    return

# Given a list of traits and their info, print out the complete HTML representing:
# 1) An <option> selector containing each
# 2) An associated div to be shown when each <option> is active
# 3) An associated popover to be copied as needed.
def traitselectorgen():
    return

################################################################################
#                                                                              #
#                        TABLE GENERATORS                                      #
#                                                                              #
################################################################################

# Use function decorations to print start/end of table
# BUG: wrong syntax
# def tablegen(fn, divID):
#     tprint(tag("div", id="%s-template" % divID, type=OPEN))
#     indent()
#     tprint(tag("table", type=OPEN))
#     indent()
#     tprint(tag("tbody", type=OPEN))
#     indent()
#
#     fn()
#
#     dedent()
#     tprint(tag("tbody", type=CLOSE))
#     dedent()
#     tprint(tag("table", type=CLOSE))
#     dedent()
#     tprint(tag("div", type=CLOSE))

# TODO: Poor style to have "consonant"/"vowel" magic strings
# I propose a constant (int?) consonant.CONSONANT or phoneme.CONSONANT to use
# here instead, and then the str values are mapped from there
def pboxgen(pType, glyphList):
    """Generate the html for a phoneme selector table, using glyphList as source
    glyphList is a str[] containing all valid glyphs. pType is either "consonant"/"vowel"
    depending on whether these are consonants or vowels."""
    if pType not in ["consonant", "vowel"]:
        raise ValueError("Invalid phoneme type! %s not recognized" % pType)
    abbrev = "cbox" if pType == "consonant" else "vbox"
    tprint("")
    tprint(comment("Auto-generated template for the {0} phoneme selector."
                        .format(pType)))
    tprint(tag("div", classList=["template"], id="{0}-template".format(abbrev), type=OPEN))
    indent()
    tprint(tag("table", type=OPEN))
    indent()
    tprint(tag("tbody", type=OPEN))
    indent()

    n = len(glyphList)

    # Calculate padding needed for last row:
    howManyOnLastRow = n % ROW_SZ
    howManyPadding = ROW_SZ - howManyOnLastRow
    howManyPaddingLeft = howManyPadding // 2

    for i, p in enumerate(glyphList):

        # Start a new tr tag for each row
        if i % ROW_SZ == 0:
            tprint(tag("tr", type=OPEN))
            indent()

        # Are we in the last row? If so, print empty cells until "centered"
        if (i // ROW_SZ == n // ROW_SZ):
            while(howManyPaddingLeft > 0):
                emptyDiv = tag("div", classList=["pbox-label-empty"])
                tprint(tag("td", body=emptyDiv))
                howManyPaddingLeft -= 1


        # Add a cell to this row, wrapping <div> in a <td>
        div = tag(
            "div",
            body=p,
            id="{0}-{1}-template".format(abbrev, p),
            classList=["pbox-label"],
            onclick="handlePboxLabel(this)"
        )
        tprint(tag("td", body=div))

        # Last in row, or last in list: close row and dedent
        if (i % ROW_SZ) == ROW_SZ-1 or i == n-1:
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
    if pType not in ["consonant", "vowel"]:
        raise ValueError("Invalid phoneme type! %s not recognized" % pType)
    abbrev = "ccbox" if pType == "consonant" else "vcbox"

    tprint("")
    tprint(comment("Auto-generated template for the {0} class selector."
                        .format(pType)))

    tprint(tag("div", classList=["template"], id="{0}-template".format(abbrev), type=OPEN))
    indent()
    tprint(tag("table", type=OPEN))
    indent()
    tprint(tag("tbody", classList=["{0}-class-selector".format(pType)], type=OPEN))
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
                clickFn="handleClboxLabel(this)"
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

def lboxgen(lType, listData):
    """Generate the html for a generic list selector table, using listData as
    a source. listData will be a dict with two fields: const.DICT: containing
    a parseDict, whose keys are the elements of the list, and const.MULTI, a bool
    signifying whether it is possible to select multiple elements from the list"""

    otherList = listData[const.DICT]
    multi     = listData[const.MULTI]
    multStr = str(multi).lower()

    tprint("")
    tprint(comment("Auto-generated template for the {0} list selector."
                        .format(lType)))

    tprint(tag("div", classList=["template"], id="%s-template" % lType, type=OPEN))
    indent()
    tprint(tag("table", type=OPEN))
    indent()
    tprint(tag("tbody", type=OPEN))
    indent()

    for s in otherList:
        tprint(tag("tr", type=OPEN))
        indent()
        tprint(tag("td", body=s,
                         classList=["lbox-label"],
                         onclick="handleLboxLabel(this, %s)" % multStr))
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
    pboxgen("consonant", consonants.GLYPHS)
    pboxgen("vowel", vowels.GLYPHS)

    # Generate phoneme class selectors
    clboxgen("consonant", consonants.CLASS_MATRIX)
    clboxgen("vowel", vowels.CLASS_MATRIX)

    # Generate general list selectors
    lboxgen("morphology", const.MORPHOLOGY)
    lboxgen("word-formation", const.WORD_FORMATION)
    lboxgen("formation-freq", const.FORMATION)
    lboxgen("word-order", const.WORD_ORDER)
    lboxgen("headedness", const.HEADEDNESS)
    lboxgen("agreement", const.CASE_AGREEMENT)
    lboxgen("case", const.CASE_AGREEMENT)

    tprint(comment("  ### END AUTO-GENERATED HTML. EDITING IS OK AGAIN ###"))
