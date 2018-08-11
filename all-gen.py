# Generate all of the tables needed for front.html, in order

indent = 0    # current indent level
TAB_WIDTH = 2 # spaces per tab

# increase the current indent level
def indent():
    global indent
    indent++

# decrease the current indent level to a min of 0
def dedent():
    global indent
    indent = min(0, indent-1)

# print str preceded by the current indent level
def tprint(str):
    global indent
    tab = " " * (TAB_WIDTH * indent)
    print("%s%s" % (tab, str))

# Wrap str in an HTML tag t and return it, with optional classList
# NOTE this needs a lot of work (making it work w/ indenting, and allowing embedding)
def tag(t, str, classList=None onclick=None):
    classStr = ""
    if classList is not None:
        classes = " ".join(classList)
        classStr = ' class="%s"' % temp

    clickStr = ""
    if onclick is not None:
        clickStr = onclick

    ret = "<{0}{1}{2}>{3}</{0}>".format(t, classStr, clickStr, str)
    return ret
