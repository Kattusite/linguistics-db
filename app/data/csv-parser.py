# Merge and anonymize the grammar/typology csv,
# Then convert it to a json file

import csv, json, hashlib, re
from lingdb import const

NETID = 1
NAME  = 2

G_TIME            = 0
G_NETID           = 1
G_NAME            = 2
G_LANGUAGE        = 3
G_NUM_CONSONANTS  = 4
G_NUM_VOWELS      = 5
G_NUM_PHONEMES    = 6
G_CONSONANTS      = 7
G_VOWELS          = 8
G_PHONETIC        = 9
G_SYLLABLE        = 10

#GRAMMAR_HEADERS as string
G_STR = [
    "time",             # G_TIME
    "netid",            # G_NETID
    "name",             # G_NAME
    "language",         # G_LANGUAGE
    "num consonants",   # G_NUM_CONSONANTS
    "num vowels",       # G_NUM_VOWELS
    "num phonemes",     # G_NUM_PHONEMES
    "consonants",       # G_CONSONANTS
    "vowels",           # G_VOWELS
    "phonetic",         # G_PHONETIC
    "syllable"          # G_SYLLABLE
]

T_TIME            = 0
T_NETID           = 1
T_NAME            = 2
T_LANGUAGE        = 3
T_CITATION        = 4
T_RECOMMEND       = 5
T_MORPHOLOGY      = 6
T_WORD_FORMATION  = 7
T_FORMATION_FREQ  = 8
T_WORD_ORDER      = 9
T_HEADEDNESS      = 10
T_AGREEMENT       = 11
T_CASE            = 12

#GRAMMAR_HEADERS as string
T_STR = [
    "time",
    "netid",
    "name",
    "language",
    "citation",
    "recommend",
    "morphological type",
    "word formation",
    "word formation frequency",
    "word order",
    "headedness",
    "agreement",
    "case"
]

def main():
    grammarCSV = open("unanon-grammar.csv", "r", newline='')
    grammarReader = csv.reader(grammarCSV)

    typologyCSV = open("unanon-typology.csv", "r", newline='')
    typologyReader = csv.reader(typologyCSV)

    outputCSV = open("anon-combined.csv", "w", newline='')
    outputWriter = csv.writer(outputCSV)

    t_header = []
    t_data = {}
    t_netid = []
    for i, row in enumerate(typologyReader):
        if i == 0:
            t_header = row
            continue
        netid = asciify(row[NETID]).encode("ASCII")
        name  = asciify(row[NAME]).encode("ASCII")
        anon_netid = hashlib.sha3_256(netid).hexdigest()
        anon_name  = hashlib.sha3_256(name).hexdigest()
        row[NETID] = anon_netid
        row[NAME]  = anon_name
        t_data[anon_netid] = row
        t_netid.append(anon_netid)

    g_header = []
    g_data = {}
    g_netid = []
    for i, row in enumerate(grammarReader):
        if i == 0:
            g_header = row
            continue
        netid = asciify(row[NETID]).encode("ASCII")
        name  = asciify(row[NAME]).encode("ASCII")
        anon_netid = hashlib.sha3_256(netid).hexdigest()
        anon_name  = hashlib.sha3_256(name).hexdigest()
        row[NETID] = anon_netid
        row[NAME]  = anon_name
        g_data[anon_netid] = row
        g_netid.append(anon_netid)


    # Merge netid lists
    netidSet = set(g_netid).union(set(t_netid))

    json_array = []
    # For each anon netid, print a row of csv and create a JSON blob
    for id in netidSet:
        # For the time being ignore the csv because it's really annoying
        # Just construct the JSON for now
        g_list = g_data[id]
        t_list = t_data[id]
        json_obj = {}

        if g_list is not None:
            json_obj[G_STR[G_LANGUAGE]]        = g_list[G_LANGUAGE]
            json_obj[G_STR[G_NAME]]            = g_list[G_NAME]
            json_obj[G_STR[G_NETID]]           = g_list[G_NETID]
            json_obj[G_STR[G_NUM_VOWELS]]      = g_list[G_NUM_VOWELS]
            json_obj[G_STR[G_NUM_CONSONANTS]]  = g_list[G_NUM_CONSONANTS]
            json_obj[G_STR[G_NUM_PHONEMES]]    = g_list[G_NUM_PHONEMES]
            json_obj[G_STR[G_NUM_PHONEMES]]    = g_list[G_NUM_PHONEMES]
            json_obj[G_STR[G_CONSONANTS]]      = csvConsonantsToBitstring(g_list[G_CONSONANTS])
            json_obj[G_STR[G_VOWELS]]          = csvVowelsToBitstring(g_list[G_VOWELS])
            


        if t_list is not None:


def asciify(str):
    return re.sub(r'[^\x00-\x7F]',' ', str)


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


main()
