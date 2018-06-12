PHONEME_GLYPHS = {
  "n":"n",
  "t":"t",
  "m":"m",
  "k":"k",
  "j":"j",
  "s":"s",
  "p":"p",
  "l":"l",
  "w":"w",
  "h":"h",
  "b":"b",
  "d":"d",
  "g":"g",
  "engma":"ŋ",
  "esh":"ʃ",
  "glottal stop":"ʔ",
  "voiceless postalveolar affricate":"tʃ",
  "f":"f",
  "r":"r",
  "palatal nasal":"ɲ",
  "z":"z",
  "voiceless alveolar affricate":"ts",
  "voiced postalveolar affricate":"dʒ",
  "x":"x",
  "v":"v",
}

PER_ROW = 5

print("<tablebody>")
for i, phoneme in enumerate(PHONEME_GLYPHS):
    if (i % PER_ROW == 0):
        print("  <tr>")
    a = '    <td><div id="pbox-%(glyph)s-template" class="pbox-label" onclick=handlePboxLabel(this)>%(glyph)s</div>'
    c = (a + '</td>') % {"glyph": PHONEME_GLYPHS[phoneme]}
    print(c)
    if (i % PER_ROW == PER_ROW-1):
        print("  </tr>")


print("</tablebody>")
