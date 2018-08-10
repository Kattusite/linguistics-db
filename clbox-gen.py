# A helper program that generates a HTML table to be used for selecting natural classes

from phonemes import consonants, vowels

TYPES = 3


# Given matrix of classes (a 2d array of all properties), generate the associated table
# Designate phonemeType as "consonant" or "vowel" for
def generateTables(matrix, phonemeType):
    print("\n\n\n")
    print('<tbody class="%s-class-selector">' % phonemeType)

    # Find longest list
    lengths = [len(entry) for entry in matrix]
    n = max(lengths)

    # For each row:
    for i in range(n):
        print("  <tr>")
        cssClass = "clbox-label clbox-label-selected" if i==0 else "clbox-label"

        # For each column:
        for j, entry in enumerate(matrix):
            if i < len(entry):
                print('    <td class="%s %s" onclick="handleClboxLabel(this)">%s</td>' %
                        (cssClass, "clbox-label-" + str(j), entry[i]))
            else:
                printEmptyCell()
        print("  </tr>")
    print("</tbody>")

def printEmptyCell():
    print('    <td class="clbox-label-empty"></td>')

# Generate consonant class table (ccbox)
generateTables(consonants.CLASS_MATRIX, "consonant")

generateTables(vowels.CLASS_MATRIX, "vowel")

# generate vowel class table (vcbox)
#generateTables(vowe)
