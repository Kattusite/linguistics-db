# Generate all of the tables needed for front.html, in order

from phonemes import vowels, consonants

indent_lvl = 0    # current indent level
TAB_WIDTH = 2 # spaces per tab

OPEN_TAG  = 0   # <body>
CLOSE_TAG = 1   # </body>
BOTH_TAG  = 2   # <body>...</body>

PBOX_PER_ROW = 5

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
def tag(t, b="", id=None, classList=None, onclick=None, other=None, type=BOTH_TAG):
    # If parameters aren't None, build them into strings
    classStr = ' class="%s"' % " ".join(classList) if classList else ""
    clickStr = ' onclick="%s"' % onclick if onclick else ""
    idStr = ' id="%s"' % id if id else ""

    openTag = "<{0}{1}{2}{3}>{4}".format(t, idStr, classStr, clickStr, b)
    closeTag = "</{0}>".format(t)

    if type == BOTH_TAG:
        return "".join([openTag, closeTag])
    elif type == OPEN_TAG:
        return openTag
    elif type == CLOSE_TAG:
        return closeTag
    else:
        raise ValueError("Invalid tag type! Must specify either open tag, close tag, or both!")

def pboxgen(glyphList):
    """Generate the html for a phoneme selector table, using glyphList as source"""
    tprint(tag("div", id="cbox-template", type=OPEN_TAG))
    indent()
    tprint(tag("table", type=OPEN_TAG))
    indent()
    tprint(tag("tbody", type=OPEN_TAG))
    indent()

    for i, p in enumerate(consonants.GLYPHS):
        # First in new row: print new row and indent
        if i % PBOX_PER_ROW == 0:
            tprint(tag("tr", type=OPEN_TAG))
            indent()

        # Add a cell to this row
        tprint(tag("div", b=p, id="cbox-{0}-template".format(p),
                   classList=["pbox-label"], onclick="handlePboxLabel(this)"))

        # Last in row: close row and dedent
        if (i % PBOX_PER_ROW) == PBOX_PER_ROW-1:
            dedent()
            tprint(tag("tr", type=CLOSE_TAG))

        # TODO: BUG: Last row may be underfull. Add special cases for this

    dedent()
    tprint(tag("tbody", type=CLOSE_TAG))
    dedent()
    tprint(tag("table", type=CLOSE_TAG))
    dedent()
    tprint(tag("div", type=CLOSE_TAG))

def clboxgen(classList):
    """Generate the html for a natural class selector table, using classList as source"""

def lboxgen(otherList):
    """Generate the html for a generic list selector table, using otherList as source"""

def ipacboxgen(glyphList):
    """Generate the html for a IPA consonant chart table, using glyphList as source"""

def ipavboxgen(glyphList):
    """Generate the html for a IPA vowel chart table, using glyphList as source"""


def main():
    pboxgen(consonants.GLYPHS)
