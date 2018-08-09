from . import language
from phonemes import consonants, vowels
from .const import *
import csv



# Read from grammar data into convenient format
def readGrammarData(csvName):

    # Locate the grammar file
    filename = csvName
    csvfile = open(filename)
    reader = csv.reader(csvfile)

    langDict = []

    # Read through file line by line
    for i, row in enumerate(reader):
        # Skip header row
        if i == 0:
            continue
        dictEntry = language.Language(row, None)

        # Add this dictionary entry to the temporary database
        langDict.append(dictEntry);
    return langDict


# Given a CSV phoneme string, return a corresponding phoneme bitstring
# That is, a string of 0s and 1s such that a 1 occurs at index i if and only if
# phonemeList[i] is found in csvStr
# phonemeList is a canonical list of the canonical phonemes to be used to create the string
def csvPhonemesToBitstring(csvStr, phonemeList):
    csvStr = csvStr.replace(PHONEME_DELIMITER, "")
    csvList = csvStr.split(INNER_DELIMITER)
    bitList = []

    # Iterate over canonical list and match against csvList
    for phoneme in phonemeList:
        if phoneme in csvList:
            bitList.append("1")
        else:
            bitList.append("0")

    # Construct string from list of matches
    return "".join(bitList)

# Given a csvStr representing a csv formatted list of consonants, return
# the corresponding bitstring of consonants, using CONSONANT_GLYPHS as the
# canonical list
def csvConsonantsToBitstring(csvStr):
    return csvPhonemesToBitstring(csvStr, CONSONANT_GLYPHS)

# Given a csvStr representing a csv formatted list of vowels, return
# the corresponding bitstring of vowels, using VOWEL_GLYPHS as the
# canonical list
def csvVowelsToBitstring(csvStr):
    return csvPhonemesToBitstring(csvStr, VOWEL_GLYPHS)
