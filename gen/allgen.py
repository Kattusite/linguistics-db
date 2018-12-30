# Generate all of the tables needed for front.html, in order
#
# Usage:
#   From cmd line in project root: (type in cmd after $)
#        > linguistics-db/ $ set PYTHONIOENCODING=utf-8
#        > linguistics-db/ $ python -m gen > gen/out.html
import sys, copy

from phonemes import vowels, consonants, metaclasses
from . import ipa_table
from data import const, selectors





################################################################################
#                                                                              #
#                        CONSTANTS                                             #
#                                                                              #
################################################################################

indent_lvl = 0    # current indent level
TAB_WIDTH = 2     # spaces per indentation level

# Tag types
OPEN  = 0   # <body>
CLOSE = 1   # </body>
BOTH  = 2   # <body>...</body>

ROW_SZ = 8  # How many columns per row in pboxgen

# Phoneme types
CONSONANT = "consonant"
VOWEL = "vowel"

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
    otherStr = " %s" % other if other else ""

    openTag = "<{0}{1}{2}{3}{5}>{4}".format(t, idStr, classStr, clickStr, bodyStr, otherStr)
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

# Prints a mode selector
def modeselector():
    tprint(tag("select", classList=["mode-selector"], type=OPEN))
    indent()
    modes = ["at least",  "at most",   "exactly",
             "less than", "more than", "not equal to"]

    for mode in modes:
        tprint(tag("option", body=mode, type=BOTH))

    dedent()
    tprint(tag("select", type=CLOSE))

# Prints a k-selector
def kselector():
    tprint(tag("input",
               classList=["k-selector"],
               type=OPEN,
               other='type="text" size="2" placeholder="1" value="1"'
               ) + " of")

def popovertemplate(popoverPrefix, selectWhat):
    """Prints a popover placeholder (to be replaced by JS).
    Use a class of popoverPrefix + "-uninit" and
    use a title of "Select " + selectWhat"""
    tprint('<a class="{0}-uninit btn btn-outline-secondary"'.format(popoverPrefix))
    tprint('   role="button"')
    tprint('   data-html="true"')
    tprint('   data-toggle="popover"')
    tprint('   title="<b>Select {0}</b>"'.format(selectWhat))
    tprint('   data-content="Error loading. Sorry!">Select {0}...</a>'.format(selectWhat))

# Given the info for a trait, print out the complete HTML representing:
# 1) A mode selector (<select>at least, at most...</select>)
# 2) A k selector    (<input>)
# 3) A placeholder template to be overwritten by JS later.
def modekpopover(selectorID, popoverPrefix, selectWhat, isActive):
    cls = [selectorID, "template"]
    if isActive:
        cls.append("active")

    div = tag("div",
              classList=cls,
              other='type="{0}"'.format(selectorID),
              type=OPEN)

    tprint(div + "Contains")
    indent()

    modeselector()
    kselector()
    popovertemplate(popoverPrefix, selectWhat, isActive)

    dedent()
    tprint(tag("div", type=CLOSE))

# Given a list of traits, print the HTML representing a <select>/<option>
# structure allowing user to pick one trait. The first trait in the list will be
# active (selected), and the others will be inactive (unselected)
def traitselector():
    return

# Given the info for a trait, print out the complete HTML representing:
# 1) An <option> selector containing each
# 2) An associated div to be shown when each <option> is active
# 3) An associated popover to be copied as needed.
def traitselectorgen():
    return

# Types of selector: (for more info see selectors.py)

# -- input selectors
# (not quite the same as trait selectors, which is how I typically use the word "selector"
# * k-selector:    simple html input component to input a number.
# * mode-selector: simple html component to pick a mode from a list.

# -- Trait selectors
# This is what I mean when I say "selector" in this project.
# It is the collection of html elements that allow a user to specify a linguistic
# property, and a set of query parameters.
# * modekpopover - selectors of the form: "at least 5 of a, b, c, d..."
# * binary - binary yes/no selectors: "contains complex consonants"
# * listpopover - select one (and only 1) from a list: "a, b, c, d..."


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


# TODO: need to change this to take in header dicts instead of [][]
def clboxgen(pType, headers):
    """Generate the html for a natural class selector table, using headers as a source.
    headers is a dict mapping trait types to possible trait values
    (e.g. "height": ["high", "med", "low", "..."])
    is a str[][] containing a list of (lists of possible classes for each type).
    pType is either "consonant" or "vowel" depending on the type being used"""

    if pType == CONSONANT:
        abbrev = "ccbox"
    elif pType == VOWEL:
        abbrev = "vcbox"
    else:
        raise ValueError("Invalid phoneme type! %s not recognized" % pType)

    tprint("")
    tprint(comment("Auto-generated template for the {0} class selector."
                        .format(pType)))

    tprint(tag("div", classList=["template"], id="{0}-template".format(abbrev), type=OPEN))
    indent()
    tprint(tag("table", classList=["{0}-class-selector".format(pType)], type=OPEN))
    indent()
    tprint(tag("tbody", type=OPEN))
    indent()

    classNames = headers["word order"]

    # Add "any x" to the front of each list and continue
    classes = [ (["any " + name]) + headers[name] for name in classNames ]

    n = max([len(cls) for cls in classes])

    for i in range(n):
        tprint(tag("tr", type=OPEN))
        indent()
        # Print one element from each of the lists
        # (or a placeholder if the list has ended already)
        for j, cls in enumerate(classes):
            htmlClasses = []
            clickFn = None
            b=None
            other=None

            if i < len(cls):
                htmlClasses += ["clbox-label"]
                clickFn="handleClboxLabel(this)"
                other = ' type="clbox-label-%d"' % j
                b=cls[i]
            else:
                htmlClasses += ["clbox-label-empty"]

            if i == 0:
                htmlClasses += ["selected"]

            tprint(tag("td", body=b, classList=htmlClasses, onclick=clickFn, other=other))

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
    a source. listData will be a dict with two fields: selectors.DICT: containing
    a parseDict, whose keys are the elements of the list, and selectors.MULTI, a bool
    signifying whether it is possible to select multiple elements from the list"""

    otherList = listData[selectors.DICT]
    multi     = listData[selectors.MULTI]
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

def ipaboxgen(table, headers, ptype):
    """Generate the html for a IPA vowel chart table,
    where table is a 2D array containing the data to be represented,
    headers is a dict containing the names of the relevant headers (see ipa_table.py),
    and type is either CONSONANT or VOWEL"""

    if ptype == CONSONANT:
        id = "ipacbox-template"
        fn = "handleIpacboxLabel(this)"
    elif ptype == VOWEL:
        id = "ipavbox-template"
        fn = "handleIpavboxLabel(this)"
    else:
        raise ValueError("ipaboxgen: type %d not consonant/vowel")

    axes = headers["axis order"]

    isOtherRow = table[-1][0] == "other"

    # Print the table as HTML
    tprint(comment("Auto-generated template for the IPA %s chart" % ptype))

    tprint(tag("div", classList=["template"], id=id, type=OPEN))
    indent()
    tprint(tag("table", type=OPEN))
    indent()
    tprint(tag("tbody", type=OPEN))
    indent()

    for (y, row) in enumerate(table):

        # If the last row is the "other" row, add a class to allow custom CSS
        if isOtherRow and y == len(table)-1:
            tprint(tag("tr", classList=["other-pad"], type=BOTH)) # for padding
            tprint(tag("tr", classList=["other-row"], type=OPEN)) # for content
        else:
            tprint(tag("tr", type=OPEN))
        indent()

        for (x, col) in enumerate(row):

            # Print first row specially (all headers)
            if y == 0:
                # For the header row the type of the cell should be a string
                assert type(col) == type("str")
                if (x % 2 == 1): # skip every other row (headers are 2 col wide)
                    continue
                oth = "scope='col' colspan='%d'"

                # print the first col header half as wide as the others
                if x == 0:
                    oth = oth % 1
                    classList = []
                else:
                    oth = oth % 2
                    classList=["ipa-header"]

                # print the header for this col
                category = axes[ipa_table.X]
                tprint(tag("th",
                            classList=classList,
                            onclick=fn,
                            body=col,
                            type=BOTH,
                            other="%s category=%s trait=%s" % (oth, category, col)))


            # Print all other rows after the first one
            else:
                # Print first col as a header
                if x == 0:
                    assert type(col) == type("str")
                    category = axes[ipa_table.Y]
                    tprint(tag("th",
                                classList=["ipa-header"],
                                onclick=fn,
                                body=col,
                                type=BOTH,
                                other="scope='row' category=%s trait='%s'" % (category, col)))

                # Non header cols: make an IPA cell
                else:
                    # For non-header rows the col should be a dict or empty str
                    body = ""
                    classList = []
                    onclick = None
                    other = None

                    if not col:  # col == "" or None
                        classList.append("ipa-box-empty")
                    elif not col["producible"]:
                        classList.append("ipa-box-impossible")
                    else:
                        classList.append("ipa-box")

                        # if this is in the "other" row, add a class for custom styling / selection
                        if isOtherRow and y == len(table)-1:
                            classList.append("other")

                        body = col["glyph"]
                        onclick = fn
                        # e.g. "manner='plosive' place='labiodental' voicing='voiced'"
                        other = ("%s='%s' %s='%s' %s='%s'" %
                            (axes[ipa_table.X], col[axes[ipa_table.X]],
                             axes[ipa_table.Y], col[axes[ipa_table.Y]],
                             axes[ipa_table.Z], col[axes[ipa_table.Z]]))

                    tprint(tag("td", body=body,
                                classList=classList,
                                onclick=onclick,
                                other=other,
                                type=BOTH))


        dedent()
        tprint(tag("tr", type=CLOSE))

    dedent()
    tprint(tag("tbody", type=CLOSE))
    dedent()
    tprint(tag("table", type=CLOSE))
    dedent()
    tprint(tag("div", type=CLOSE))


################################################################################
#                                                                              #
#                        MAIN                                                  #
#                                                                              #
################################################################################

# Prints the auto generated html to stdout, or a file named output if specified
def main(output=None):

    # Redirect to file if desired
    if output:
        file = open(output, "w", encoding="utf-8")
        sys.stdout = file

    tprint(comment("  ### BEGIN AUTO-GENERATED HTML. DO NOT EDIT ###"))

    # Generate phoneme selectors
    pboxgen("consonant",    consonants.GLYPHS)
    pboxgen("vowel",        vowels.GLYPHS)

    # Generate phoneme class selectors
    clboxgen("consonant",   consonants.HEADERS)
    clboxgen("vowel",       vowels.HEADERS)

    # Generate general list selectors
    lboxgen("syllable",         selectors.SYLLABLE)
    lboxgen("morphology",       selectors.MORPHOLOGY)
    lboxgen("word-formation",   selectors.WORD_FORMATION)
    lboxgen("formation-freq",   selectors.FORMATION)
    lboxgen("word-order",       selectors.WORD_ORDER)
    lboxgen("headedness",       selectors.HEADEDNESS)
    lboxgen("agreement",        selectors.AGREEMENT)
    lboxgen("case",             selectors.CASE)
    lboxgen("metaclass",        metaclasses.METACLASSES)

    # Generate IPA selectors
    #print(ipa_table.CONSONANT_TABLE)
    ipaboxgen(ipa_table.CONSONANT_TABLE,
              consonants.HEADERS,
              CONSONANT)

    ipaboxgen(ipa_table.VOWEL_TABLE,
              vowels.HEADERS,
              VOWEL)

    tprint(comment("  ### END AUTO-GENERATED HTML. EDITING IS OK AGAIN ###"))

    # Make sure we're really done printing
    sys.stdout.flush()
