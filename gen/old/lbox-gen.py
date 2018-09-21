# A helper program for generating selectors for a list of generic characteristics
# The L stands for List

# NOTE DEPRECATED
from data import const

# Use the strings in arr to generate a table
def generateTable(type, arr):
    print("\n\n\n")
    print('<tbody class="%s-selector">' % type)
    for s in arr:
        print('  <tr>')
        row = '    <td class="lbox-label" onclick="handleLboxLabel(this)">%s</td>' % (s)
        print(row)
        print('  </tr>')
    print('</tbody>')

def main():
    generateTable("morphology", const.MORPHOLOGY_DICT.keys())
    generateTable("word-formation", const.WORD_FORMATION_DICT.keys())
    generateTable("formation-freq", const.FORMATION_DICT.keys())
    generateTable("word-order", const.WORD_ORDER_DICT.keys())
    generateTable("headedness", const.HEADEDNESS_DICT.keys())
    generateTable("agreement", const.CASE_AGREEMENT_DICT.keys())
    generateTable("case", const.CASE_AGREEMENT_DICT.keys())

main()
