# Generate all of the tables needed for front.html, in order
#
# Usage:
#   From cmd line in project root: (type in cmd after $)
#        > linguistics-db/ $ set PYTHONIOENCODING=utf-8
#        > linguistics-db/ $ python -m gen > gen/out.html
import sys, copy, json

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

# Used for deciding if selectors are activated (Shown) or inactive (hidden)
ACTIVE = True
INACTIVE = False

IPA_TRAPEZOID_ASPECT_RATIO = 1000 / 700
IPA_TRAPEZOID_H = 300
IPA_TRAPEZOID_W = int(IPA_TRAPEZOID_ASPECT_RATIO * IPA_TRAPEZOID_H)

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
def tag(t, body=None, id=None, classList=None, onclick=None, style=None, other=None, type=BOTH):
    # If parameters aren't None, build them into strings
    bodyStr  = body if body else ""
    classStr = ' class="%s"' % " ".join(classList) if classList else ""
    clickStr = ' onclick="%s"' % onclick if onclick else ""
    idStr = ' id="%s"' % id if id else ""
    styleStr = ' style="%s"' % style if style else ""
    otherStr = " %s" % other if other else ""

    openTag = "<{0}{1}{2}{3}{5}{6}>{4}".format(t, idStr, classStr, clickStr, bodyStr, otherStr, styleStr)
    closeTag = "</{0}>".format(t)

    if type == BOTH:
        return "".join([openTag, closeTag])
    elif type == OPEN:
        return openTag
    elif type == CLOSE:
        return closeTag
    else:
        raise ValueError("Invalid tag type! Must specify either open tag, close tag, or both!")

def br():
    tprint(tag("br", type=OPEN))


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
    tprint(tag("select",
               classList=["mode-selector"],
               other='onchange="handleModeSelect(this)"',
               type=OPEN))
    indent()
    modes = ["at least",  "at most",   "exactly",
             "less than", "more than", "not equal to",
             "all"]

    for mode in modes:
        tprint(tag("option", body=mode, type=BOTH))

    dedent()
    tprint(tag("select", type=CLOSE))

# Prints a k-selector
def kselector():
    tprint(tag("input",
               classList=["k-selector"],
               type=OPEN,
               other='type="number" size="2" placeholder="e.g. 1" value="1" min=0 max=999 step=1'
               ) + " of")

def popovertemplate(popoverPrefix, selectWhat):
    """Prints a popover placeholder (to be replaced by JS).
    Use a class of popoverPrefix + ".uninit" and
    use a title of "Select " + selectWhat"""
    tprint('<a class="{0} uninit btn btn-outline-secondary"'.format(popoverPrefix))
    tprint('   role="button"')
    tprint('   data-html="true"')
    tprint('   data-toggle="popover"')
    tprint('   title="<b>Select {0}</b>"'.format(selectWhat))
    tprint('   data-content="Error loading. Sorry!">Select {0}...</a>'.format(selectWhat))

def getSelectorClassList(htmlID, isActive):
    cls = [htmlID, "template"]
    if isActive:
        cls.append("active")
    else:
        cls.append("inactive")
    return cls

# Given the info for a trait, print out the complete HTML representing:
# 1)   A mode selector (<select>at least, at most...</select>)
# 2)   A k selector    (<input>)
# 2.5) Some optional number of <br> tags
# 3)   A placeholder template to be overwritten by JS later.
def modekpopoverdiv(htmlID, popoverPrefix, selectWhat, isActive, num_br=0):
    cls = getSelectorClassList(htmlID, isActive)

    div = tag("div",
              classList=cls,
              other='type="{0}"'.format(htmlID),
              type=OPEN)

    tprint(div + "Contains")
    indent()

    modeselector()
    kselector()

    for i in range(num_br):
        br()

    popovertemplate(popoverPrefix, selectWhat)

    dedent()
    tprint(tag("div", type=CLOSE))

def popoverdiv(htmlID, popoverPrefix, selectWhat, isActive):
    cls = getSelectorClassList(htmlID, isActive)

    tprint(tag("div", classList=cls, other='type="%s"' % htmlID, type=OPEN))
    indent()
    popovertemplate(popoverPrefix, selectWhat)
    dedent()
    tprint(tag("div", type=CLOSE))

# Print out the complete HTML representing a simple boolean selector,
# consisting of a div whose contents are the string provided as argument
def booldiv(htmlID, body, isActive):
    cls = getSelectorClassList(htmlID, isActive)

    tprint(tag("div", classList=cls, other='type="%s"' % htmlID, type=OPEN))
    indent()
    tprint(body)
    dedent()
    tprint(tag("div", type=CLOSE))


# Given a single selector dictionary (From selectors.py), print out the entire
# HTML of that selector's body. This is the HTML that will be shown to the user
# when a selector is picked from the dropdown.
def selectorbody(sel, isActive):
    mode    = sel[selectors.MODE]
    htmlID  = sel[selectors.HTML_ID]

    # If this is an inline IPA body, print a mode/k/popover div with extra spacing
    if mode in [selectors.PICK_K_IPA]:
        popoverPrefix   = sel[selectors.POPOVER_PREFIX]
        selWhat         = sel[selectors.SELECT_WHAT]
        modekpopoverdiv(htmlID, popoverPrefix, selWhat, isActive, num_br=2)
    # If this is a popover-based body with multiple selections, print mode/k/popover div
    elif mode in [selectors.PICK_K, selectors.PICK_CLASS, selectors.PICK_MULTI]:
        popoverPrefix   = sel[selectors.POPOVER_PREFIX]
        selWhat         = sel[selectors.SELECT_WHAT]
        modekpopoverdiv(htmlID, popoverPrefix, selWhat, isActive)
    # If this is a popover-based body with one selection, print popover div
    elif mode == selectors.PICK_ONE:
        popoverPrefix   = sel[selectors.POPOVER_PREFIX]
        selWhat         = sel[selectors.SELECT_WHAT]
        popoverdiv(htmlID, popoverPrefix, selWhat, isActive)
    # If there is nothing to select, print basic bool div
    elif mode == selectors.BOOLEAN:
        body = sel[selectors.BOOL_BODY]
        booldiv(htmlID, body, isActive)
    elif mode == selectors.NO_QUERY:
        body = sel[selectors.BOOL_BODY]
        booldiv(htmlID, body, isActive)
    else:
        sys.stderr.write("Attempted to create selector body for an unknown mode!")

# Given a list of traits, print the HTML representing a <select>/<option>
# structure allowing user to pick one trait.
# Raise an exception if the provided argument is Falsy (None or [])
def selectdropdowndiv(selectorList):
    if not selectorList:
        raise ValueError("Cannot create selectdropdown of an empty list!")


    tprint(comment("Auto-generated template for the selectors dropdown"))
    tprint(tag("div",
               classList = ["alert", "alert-info", "trait-div"],
               other = 'id="trait-div-template" role="alert"',
               type=OPEN))
    indent()

    # == Print out the dropdown selector==
    htmlID = "trait-selector"
    tprint(tag("select",
               classList=[htmlID, "template"],
               type=OPEN,
               other='type=%s onchange="handleTraitSelect(this)"' % htmlID))
    indent()
    for sel in selectorList:
        tprint(tag("option", body=sel[selectors.SELECT_NAME], type=BOTH))
    dedent()
    tprint(tag("select", type=CLOSE))

    # == Print out the bodies of each selector ==

    # The first is activated, and the others are not
    selectorbody(selectorList[0], ACTIVE)
    for sel in selectorList[1:]:
        selectorbody(sel, INACTIVE)

    dedent()
    tprint(tag("div", type=CLOSE))

# Print out the popover bodies (templates) for every selector in selectorList
# These are the templates that will be copied into the document by JS
def popoverbodiesdiv(selectorList):

    for sel in selectorList:
        mode = sel[selectors.MODE]
        html_id = sel[selectors.HTML_ID]

        # currently just a program sketch

        # Generate pbox templates
        if mode in [selectors.PICK_K]:
            if "consonant" in html_id:
                pboxgen("consonant", consonants.GLYPHS)
            elif "vowel" in html_id:
                pboxgen("vowel", vowels.GLYPHS)
            else:
                ValueError("Unexpected pbox type in popoverbodiesdiv: %s" % html_id)

        # Generate ipabox templates
        elif mode in [selectors.PICK_K_IPA]:
            if "consonant" in html_id:
                ipaboxgen(ipa_table.CONSONANT_TABLE, consonants.HEADERS, CONSONANT)
            elif "vowel" in html_id:
                ipaboxgen(ipa_table.VOWEL_TABLE, vowels.HEADERS, VOWEL)
            else:
                ValueError("Unexpected ipabox type in popoverbodiesdiv: %s" % html_id)

        # Generate clbox templates
        elif mode in [selectors.PICK_CLASS]:
            if "consonant" in html_id:
                clboxgen("consonant", consonants.HEADERS)
            elif "vowel" in html_id:
                clboxgen("vowel", vowels.CLBOX_HEADERS)
            else:
                ValueError("Unexpected clbox type in popoverbodiesdiv: %s" % html_id)

        # Generate lbox templates
        elif mode in [selectors.PICK_ONE, selectors.PICK_MULTI]:
            lboxgen(sel)

        # No popover to generate!
        elif mode in [selectors.BOOLEAN, selectors.NO_QUERY]:
            continue

        # Illegal mode
        else:
            raise ValueError("Unexpected mode in popoverbodiesdiv: %s" % mode)


    return


# Given the info for a list of selectors, print out the complete HTML representing
# the following for every selector in the list:
# 1) An <option> selector containing each
# 2) An associated div to be shown when each <option> is active
# 3) An associated popover to be copied as needed.
def traitselectorgen():
    # This isn't yet implemented - other functions do the job and it would take
    # more code to get this to auto-generate the popovers. Steps 1) and 2) are
    # completed by the above function (selectdropdown).
    # Step 3) requires additional info in the selectors.py definition (e.g glyph lists)
    raise NotImplementedError("Not yet written")
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
# pboxgen (and pbox's in general) are deprecated now that ipaboxes exist
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
            # id="{0}-{1}-template".format(abbrev, p),
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

def clboxgen(pType, headers):
    """Generate the html for a natural class selector table, using headers as a source.
    headers is a dict mapping trait types to possible trait values
    (e.g. "height": ["high", "med", "low", "..."])
    is a str[][] containing a list of (lists of possible classes for each type).
    popoverPrefix is the popover prefix being created (e.g. "ccbox-selector")"""

    if pType == CONSONANT:
        popoverPrefix = selectors.CONSONANT_CLASS[selectors.POPOVER_PREFIX]
    elif pType == VOWEL:
        popoverPrefix = selectors.VOWEL_CLASS[selectors.POPOVER_PREFIX]
    else:
        raise ValueError("Illegal phoneme type passed to clboxgen")

    tprint("")
    tprint(comment("Auto-generated template for the {0} class selector."
                        .format(popoverPrefix)))

    tprint(tag("div",
               classList=["template"],
               id="{0}-template".format(popoverPrefix),
               type=OPEN))
    indent()
    tprint(tag("table", classList=["{0}-table".format(popoverPrefix)], type=OPEN))
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

def lboxgen(listData):
    """Generate the html for a generic list selector table, using listData as
    a source. listData will be a dict with (at least) two fields: selectors.DICT: containing
    a parseDict, whose keys are the elements of the list, and selectors.MULTI, a bool
    signifying whether it is possible to select multiple elements from the list"""

    lType = listData[selectors.POPOVER_PREFIX]

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
        td = tag("td", body=s,
                       classList=["lbox-label"],
                       onclick="handleLboxLabel(this, %s)" % multStr)
        tprint(tag("tr", body=td, type=BOTH))

    dedent()
    tprint(tag("tbody", type=CLOSE))
    dedent()
    tprint(tag("table", type=CLOSE))
    dedent()
    tprint(tag("div", type=CLOSE))

def voweltrapezoid():
    """Print the vowel trapezoid image in an img tag"""
    src_str = "src='/static/img/Blank_vowel_trapezoid.png'"
    w_str = "width={0}px".format(IPA_TRAPEZOID_W)
    h_str = "height={0}px".format(IPA_TRAPEZOID_H)
    imgdata = "{0} {1} {2}".format(src_str, w_str, h_str)

    style_str = "position: relative; top: 25px; left: 40px; margin-bottom: 25px;"
    img = tag("img", other=imgdata, style=style_str, type=OPEN)
    tprint(img)

    # Add a little bit of extra padding to keep the image inside the blue box

def getTrapezoidStyle(table, x, y, alignCenter=False):
    """Generate the style string for the cell of a given table at specified x, y
    coordinates. This generated style string should have the effect of shifting
    the cell so that it appears in the correct location on the trapezoid (ie
    mapping from rectangular coordinates to trapezoidal ones)"""

    # WARNING: This function was made through ages of trial and error fine-tuning
    # constants and magic numbers. It is a pain to modify - small changes might
    # break things, and some day it should probably all be rewritten in favor
    # of a better way
    # If you need to change something here, just tweak one number at a time
    # until it starts looking right, then move onto the next number and hope
    # it all still works

    # what number row / column header does this cell fall under?
    # x  :  0   1   2   3   4   5   6   7   8
    # col:  0   1   1   2   2   3   3   4   4
    ytorow = (lambda y : y)
    xtocol = (lambda x : (x+1) // 2)

    # Coord (1,1) is the top left content cell, (0,0) is the top left header
    max_x = len(table[1])
    max_y = len(table)

    max_col = xtocol(max_x) - 1
    max_row = ytorow(max_y) - 1

    # offset = -1 if on the left side of a column (odd), +1 if on the right side (even)
    if (x % 2 == 1):
        offset = -1
    else:
        offset = +1

    if (x == 0 or alignCenter):
        offset = 0

    row = ytorow(y)
    col = xtocol(x)

    # Should be in the range 0.0 .. 1.0 for cells
    row_ratio = max((row - 1) / (max_row - 1), 0)
    col_ratio = max((col - 1) / (max_col - 1), 0)

    # Magic Numbers:
    H_SCALING = 0.85 # How much of trapezoid image is whitespace vertically?
    W_SCALING = 0.80 # How much of trapezoid image is whitespace horizontally?

    row_px = row_ratio * IPA_TRAPEZOID_H * H_SCALING
    col_px = col_ratio * IPA_TRAPEZOID_W * W_SCALING

    # Magic Numbers:
    X_OFFSET = 70      # X coord of the upper left cell
    Y_OFFSET = 35      # Y coord of the upper left cell
    SKEW_FACTOR = 0.4  # Magnitude of the skew effect (0 = rectangle, 1 = triangle)

    # how far offset the origin (0,0) should be w.r.t. image
    x_skew = row_ratio * IPA_TRAPEZOID_W * SKEW_FACTOR * (1 - col_ratio)

    x_trans = col_px + X_OFFSET + x_skew
    y_trans = row_px + Y_OFFSET

    # Apply the left/right offsets (unrounded = left, rounded = right)
    # Magic number:
    OFFSET_SIZE = 13  # How much to offset cells left/right of central position
    if x != 0 and y != 0:
        x_trans = x_trans + (offset * OFFSET_SIZE)
    elif x == 0:
        # x_trans = x_trans - 70      # labels along diagonal
        x_trans = 0                 # labels in vertical line
    elif y == 0:
        x_trans = x_trans - 13
        y_trans = y_trans - 40

    x_str = "left: {0}px;".format(x_trans)
    y_str = "top: {0}px;".format(y_trans)

    pos_str = "position: absolute;"

    style = "{0} {1} {2}".format(pos_str, x_str, y_str)

    return style

def ipaboxgen(table, headers, pType):
    """Generate the html for a IPA vowel chart table,
    where table is a 2D array containing the data to be represented,
    headers is a dict containing the names of the relevant headers (see ipa_table.py),
    and type is either CONSONANT or VOWEL"""

    if pType == CONSONANT:
        selData = selectors.IPA_CONSONANT
        fn = "handleIpacboxLabel(this)"
    elif pType == VOWEL:
        selData = selectors.IPA_VOWEL
        fn = "handleIpavboxLabel(this)"
    else:
        raise ValueError("ipaboxgen: type %d not consonant/vowel")

    id = "{0}-template".format(selData[selectors.POPOVER_PREFIX])

    axes = headers["axis order"]

    isOtherRow = (table[-1][0] == "other")

    # Print the table as HTML
    tprint(comment("Auto-generated template for the IPA %s chart" % pType))
    tprint(tag("div",
               classList=["template"],
               id=id,
               type=OPEN,
               style='position: relative;'))
    indent()

    table_style = None

    # if VOWEL, add a background image.
    if pType == VOWEL:
        voweltrapezoid()
        # Positioning used to get table on top of img
        table_style = "position: absolute; top: 0px;"

    tprint(tag("table", type=OPEN, style=table_style))
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

        for (x, cell) in enumerate(row):

            # Print headers specially.
            if y == 0 or x == 0:
                # Header cells should have type string (the contents of header)
                assert type(cell) == type("str")
                oth = "scope='%s' colspan='%d'"
                classList = ["ipa-header"]
                category = '""'
                style = getTrapezoidStyle(table, x, y) if pType == VOWEL else None

                # Set parameters for row headers / col headers differently.
                if y == 0 and x == 0:
                    oth = oth % ("col", 1)
                    classList = []
                    style = None
                elif y == 0:
                    # skip every other row (headers are 2 col wide)
                    if (x % 2 == 1):
                        continue
                    oth = oth % ("col", 2)
                    category = axes[ipa_table.X]
                elif x == 0:
                    oth = oth % ("row", 1)
                    category = axes[ipa_table.Y]

                tprint(tag("th",
                            classList=classList,
                            onclick=fn,
                            body=cell,
                            type=BOTH,
                            style=style,
                            other="%s category='%s' trait='%s'" % (oth, category, cell)))

            # Non header cell: make an IPA cell
            else:
                # For non-header rows the cell should be a dict or empty str
                body = ""
                classList = []
                onclick = None
                other = None
                style = None

                if not cell:  # cell == "" or None
                    classList.append("ipa-box-empty")
                elif not cell["producible"]:
                    classList.append("ipa-box-impossible")
                else:
                    classList.append("ipa-box")

                    # if this is in the "other" row, add a class for custom styling / selection
                    if isOtherRow and y == len(table)-1:
                        classList.append("other")

                    body = cell["glyph"]
                    onclick = fn
                    # e.g. "manner='plosive' place='labiodental' voicing='voiced'"
                    other = ("%s='%s' %s='%s' %s='%s'" %
                        (axes[ipa_table.X], cell[axes[ipa_table.X]],
                         axes[ipa_table.Y], cell[axes[ipa_table.Y]],
                         axes[ipa_table.Z], cell[axes[ipa_table.Z]]))

                    # For vowels add extra CSS for positioning
                    if pType == VOWEL:
                        # Schwa (ə) is a special case. should be centered in chart
                        alignCenter = (body == "ə")
                        style = getTrapezoidStyle(table, x, y, alignCenter)

                tprint(tag("td", body=body,
                            classList=classList,
                            onclick=onclick,
                            other=other,
                            style=style,
                            type=BOTH))


        dedent()
        tprint(tag("tr", type=CLOSE))

    dedent()
    tprint(tag("tbody", type=CLOSE))
    dedent()
    tprint(tag("table", type=CLOSE))
    dedent()
    tprint(tag("div", type=CLOSE))


# Print the selectors.py constants to a .js file for use
def exportJavascript():
    # TODO move these constants elsewhere (__main__ or __init__ perhaps?)
    JS_PATH = "app/static/js/"
    JS_NAME = "selectors_const.js"

    filename = "{0}{1}".format(JS_PATH, JS_NAME)

    VAR_NAME = "SELECTORS_DICT"

    # Remove the functions because they aren't transferrable to JS
    dict = copy.deepcopy(selectors.SELECTORS_DICT)
    for key in dict:
        val = dict[key]
        del val[selectors.FUNCTION]

    VAR_DATA = json.dumps(dict, sort_keys=True, indent=4)

    with open(filename, "w", encoding="utf-8") as js:
        var = "var {0} = {1};\n".format(VAR_NAME, VAR_DATA)

        js.write("/* Automatically generated by selectors.py. DO NOT EDIT! */\n")
        js.write(var)
        js.flush() # "with" should take care of this, but being explicit is nice


################################################################################
#                                                                              #
#                        MAIN                                                  #
#                                                                              #
################################################################################

# Prints the auto generated html to stdout, or a file named output if specified
def main(output=None):

    # Print the js file
    exportJavascript()

    # Redirect to file if desired
    if output:
        file = open(output, "w", encoding="utf-8")
        sys.stdout = file

    tprint(comment("  ### BEGIN AUTO-GENERATED HTML. DO NOT EDIT ###"))

    # Generate the dropdown menu and its associated divs
    selectdropdowndiv(selectors.SELECTORS)

    # Generate popover body templates (pbox, clbox, lbox, ipabox)
    popoverbodiesdiv(selectors.SELECTORS)

    tprint(comment("  ### END AUTO-GENERATED HTML. EDITING IS OK AGAIN ###"))

    # Make sure we're really done printing
    sys.stdout.flush()
