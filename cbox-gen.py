# A helper program that generates a HTML table to be used for selecting natural classes

from phonemes import consonants, vowels

TYPES = 3


# Given voicing, place, manner lists, generate the associated table
def generateTables(voicings, places, manners):
    print("\n\n\n")
    print("<tablebody>")
    n = max(len(voicings), len(places), len(manners))
    for i in range(n):
        print("  <tr>")
        if (i < len(voicings)):
            print("    <td>" + voicings[i] + "</td>")
        else:
            printEmptyCell()
        if (i < len(places)):
            print("    <td>" + places[i] + "</td>")
        else:
            printEmptyCell()
        if (i < len(manners)):
            print("    <td>" + manners[i] + "</td>")
        else:
            printEmptyCell()
        print("  </tr>")

    print("</tablebody>")

def printEmptyCell():
    print("    <td></td>")

# Generate consonant class table (ccbox)
generateTables(consonants.CONSONANT_VOICINGS, consonants.CONSONANT_PLACES, consonants.CONSONANT_MANNERS)

# generate vowel class table (vcbox)
#generateTables(vowe)
