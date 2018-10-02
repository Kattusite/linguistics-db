# A helper program that generates HTML for the phoneme selector tables
# The P stands for Phoneme

# NOTE DEPRECATED
from phonemes import VOWEL_GLYPHS, CONSONANT_GLYPHS

PER_ROW = 5


# TODO modularize into a single function that takes a glyph list and v/c selector to indicate vowel or consonant

# Generate consonant table (cbox)
print("\n\n\n")
print("<tbody>")
for i, phoneme in enumerate(CONSONANT_GLYPHS):
    if (i % PER_ROW == 0):
        print("  <tr>")
    a = '    <td><div id="cbox-%(glyph)s-template" class="pbox-label" onclick=handlePboxLabel(this)>%(glyph)s</div>'
    c = (a + '</td>') % {"glyph": phoneme}
    print(c)
    if (i % PER_ROW == PER_ROW-1):
        print("  </tr>")
print("</tbody>")


# Generate vowel table (vbox)
print("\n\n\n")
print("<tbody>")
for i, phoneme in enumerate(VOWEL_GLYPHS):
    # if on first element in row, start a new <tr>
    if (i % PER_ROW == 0):
        print("  <tr>")

    # if on last row, attempt to center
    if (i // PER_ROW == len(VOWEL_GLYPHS) // PER_ROW):
        howManyOnThisRow = len(VOWEL_GLYPHS) % PER_ROW
        howManyPadding = PER_ROW - howManyOnThisRow
        howManyPaddingLeft = howManyPadding // 2
        # Pad on the left with empty td
        if i % PER_ROW < howManyPaddingLeft:
            print('    <td><div class="pbox-label-empty"></div></td>')

    a = '    <td><div id="vbox-%(glyph)s-template" class="pbox-label" onclick=handlePboxLabel(this)>%(glyph)s</div>'
    c = (a + '</td>') % {"glyph": phoneme}
    print(c)

    # if on last element in row, terminate <tr>
    if (i % PER_ROW == PER_ROW-1):
        print("  </tr>")
print("</tbody>")
