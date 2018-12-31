import sys
from phonemes import consonants, vowels


# These variables specify only which things will be displayed in the
# HTML version of the IPA chart, and in what order
# It is NOT the canonical list of possible characteristics.

# ============== CONSONANT CONSTANTS =================
# see consonants.py




# =============== VOWEL CONSTANTS ================
# see vowels.py

X = 0
Y = 1
Z = 2

# =============== HELPER Functions ===============
def dbg(s):
    """Print a debugging string"""
    # return
    sys.stderr.write(s + "\n")

# Create IPA table from given ipa data and headers
def createIPATable(data, headers):
    axis_order = headers["axis order"]
    word_order = headers["word order"]
    axes = [headers[axis] for axis in axis_order]

    # axes[X] will be e.g. "place" or "backness"

    # Get the number of rows and cols (including headers + doubling for voicing)
    num_rows = len(axes[Y]) + 2                 # (1 header, one "other" row)
    num_cols = len(axes[X]) * len(axes[Z]) + 1  # (1 header)
    num_oth = 0                                 # num elements in "other" row
    table = [[None for i in range(num_cols)] for j in range(num_rows)] # None or "" ?

    for p in data:
        # Get the target row / column
        try:
            row  = axes[Y].index(p[axis_order[Y]]) + 1
            col  = axes[X].index(p[axis_order[X]]) * 2
            col += axes[Z].index(p[axis_order[Z]]) + 1
        except ValueError:
            # Not found in the standard table - place in "other" row instead
            dbg("%s %s %s /%s/ unable to be placed in IPA table - no header exists!" %
                  (p[word_order[0]], p[word_order[1]], p[word_order[2]], p["glyph"]))
            num_oth += 1
            row = num_rows - 1
            col = num_oth

        # Place this phoneme's data in the table
        table[row][col] = p

    # Add in the headers
    for (i, head) in enumerate(axes[Y]):
        table[i+1][0] = head

    for (i, head) in enumerate(axes[X]):
        table[0][2*i+1] = head
        table[0][2*i+2] = head

    table[0][0] = ""
    table[num_rows-1][0] = "other"

    # if "other" row is empty, remove it from table
    if num_oth == 0:
        del table[num_rows-1]
    # otherwise remove all the empty entries in that row
    else:
        table[num_rows-1] = table[num_rows-1][0:num_oth+1]




    return table

# Reconstruct IPA tables
CONSONANT_TABLE = createIPATable(consonants.data, consonants.HEADERS)
VOWEL_TABLE     = createIPATable(vowels.data, vowels.HEADERS)
