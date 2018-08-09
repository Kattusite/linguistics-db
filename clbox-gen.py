# A helper program that generates a HTML table to be used for selecting natural classes

from phonemes import consonants, vowels

TYPES = 3


# Given voicing, place, manner lists, generate the associated table
# NOTE TODO Plz do this first
# NOTE NOTE NOTE Future me, after you wake up, remove clbox-label entirely (or largely)
# and split into three separate categories (voicings, places, manners)
# this will make it easier to select/deselect choices. think abuot it
# maybe use radio buttons instead
def generateTables(voicings, places, manners):
    print("\n\n\n")
    print("<tablebody>")
    n = max(len(voicings), len(places), len(manners))
    for i in range(n):
        print("  <tr>")
        cssClass = "clbox-label clbox-label-selected" if i==0 else "clbox-label"
        if (i < len(voicings)):
            print('    <td class="%s %s" onclick="handleClboxLabel(this)">%s</td>' % (cssClass, "clbox-label-voicing", voicings[i]))
        else:
            printEmptyCell()
        if (i < len(places)):
            print('    <td class="%s %s" onclick="handleClboxLabel(this)">%s</td>' % (cssClass, "clbox-label-place", places[i]))
        else:
            printEmptyCell()
        if (i < len(manners)):
            print('    <td class="%s %s" onclick="handleClboxLabel(this)">%s</td>' % (cssClass, "clbox-label-manner", manners[i]))
        else:
            printEmptyCell()
        print("  </tr>")

    print("</tablebody>")

def printEmptyCell():
    print('    <td class="clbox-label-empty"></td>')

# Generate consonant class table (ccbox)
generateTables(consonants.CONSONANT_VOICINGS, consonants.CONSONANT_PLACES, consonants.CONSONANT_MANNERS)

# generate vowel class table (vcbox)
#generateTables(vowe)
