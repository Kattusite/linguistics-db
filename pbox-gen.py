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
print("  <tr>")
for i, phoneme in enumerate(PHONEME_GLYPHS):
    a = '    <td><label class="pbox-label" for="pbox-template-%(glyph)s">%(glyph)s</label>\n'
    b = '        <input id="pbox-template-%(glyph)s" type="checkbox" class="pbox-check"></td>'   
    c = (a + b) % {"glyph": PHONEME_GLYPHS[phoneme]}
    print(c)
    if (i % PER_ROW == 4):
        print("  </tr>")


print("</tablebody>")
