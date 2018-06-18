# Merge and anonymize the grammar/typology csv,
# Then convert it to a json file

import csv, json, hashlib, re
from operator import itemgetter, attrgetter
from phonemes import CONSONANT_GLYPHS, VOWEL_GLYPHS
from lingdb import const as ling_const
from .const import *


# Read in the CSV files from the declared constant filenames, and then
# Return a JSON object representing that csv data
def csvToJSON():
    grammarCSV = open(DATA_PATH + "unanon-grammar.csv", "r", newline='')
    grammarReader = csv.reader(grammarCSV)

    typologyCSV = open(DATA_PATH + "unanon-typology.csv", "r", newline='')
    typologyReader = csv.reader(typologyCSV)

    t_header = []
    t_data = {}
    t_netid = []
    for i, row in enumerate(typologyReader):
        if i == 0:
            t_header = row
            continue
        netid = asciify(row[NETID]).encode("ASCII")
        name  = asciify(row[NAME]).encode("ASCII")
        # Slice off first few chars to make hashes manageable (collisions negligible)
        anon_netid = hashlib.sha3_256(netid).hexdigest()[:HASH_SIZE]
        anon_name  = hashlib.sha3_256(name).hexdigest()[:HASH_SIZE]
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
        # Slice off first few chars to make hashes manageable (collisions negligible)
        anon_netid = hashlib.sha3_256(netid).hexdigest()[:HASH_SIZE]
        anon_name  = hashlib.sha3_256(name).hexdigest()[:HASH_SIZE]
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
        g_list = g_data.get(id)
        t_list = t_data.get(id)
        json_obj = {}

        if g_list is not None:
            # Extract simple grammar attributes
            json_obj[G_STR[G_LANGUAGE]]        = g_list[G_LANGUAGE]
            json_obj[G_STR[G_NAME]]            = g_list[G_NAME]
            json_obj[G_STR[G_NETID]]           = g_list[G_NETID]
            json_obj[G_STR[G_NUM_VOWELS]]      = g_list[G_NUM_VOWELS]
            json_obj[G_STR[G_NUM_CONSONANTS]]  = g_list[G_NUM_CONSONANTS]
            json_obj[G_STR[G_NUM_PHONEMES]]    = g_list[G_NUM_PHONEMES]
            json_obj[G_STR[G_NUM_PHONEMES]]    = g_list[G_NUM_PHONEMES]

            # Extract phoneme lists
            json_obj[G_STR[G_CONSONANTS]]      = csvConsonantsToBitstring(g_list[G_CONSONANTS])
            json_obj[G_STR[G_VOWELS]]          = csvVowelsToBitstring(g_list[G_VOWELS])

            # Extract phonetic + syllable info
            phonetic = g_list[G_PHONETIC].split(ling_const.INNER_DELIMITER)
            syllable = g_list[G_SYLLABLE].split(ling_const.INNER_DELIMITER)

            # Process phonetics
            # Offset indices relative to this one
            offset = G_P_3PLUS_PLACES

            # Initialize all json fields to False
            for i, str in enumerate(G_P_STR):
                json_obj[G_STR[offset + i]] = False

            # Search raw CSV fields for containing correct attribute names.
            # On match, set corresponding field to True
            for p in phonetic:
                for i, str in enumerate(G_P_STR):
                    if str in p:
                        json_obj[G_STR[offset + i]] = True

            # Process syllable
            offset = G_S_CV
            # Initialize all json fields to False
            for i, str in enumerate(G_S_STR):
                json_obj[G_STR[offset + i]] = False

            # Search raw CSV fields for containing correct attribute names
            # (but not containing other names e.g. CV matches CV not CCV)

            # Construct Regexps for syllables
            syllable_RE = []
            for i, str in enumerate(G_S_STR):
                # BUG: This depends on assumption that VCC follows VC in CSV.
                syllable_RE.append("\W?" + str + "\W?") # e.g. \W?CV\W?

            # On match, set corresponding field to True
            for s in syllable:
                for i, str in enumerate(G_S_STR):
                    if re.search(syllable_RE[i], s):
                        json_obj[G_STR[offset + i]] = True

        if t_list is not None:
            pass

        json_array.append(json_obj)
        # print(json_obj)

    # Sort the array by language, then name, netid hashes (for convenience)
    json_array = sorted(json_array, key=itemgetter("language", "name", "netid"))
    return json_array



def main():
    json_array = csvToJSON()

    # Open output files (CSV currently unused)
    outputCSV = open(DATA_PATH + "anon-combined.csv", "w", newline='')
    outputCSVWriter = csv.writer(outputCSV)

    outputJSON = open(DATA_PATH + "anon-combined.json", "w")

    json.dump(json_array,
              outputJSON,
              sort_keys=False,
              ensure_ascii=False,
              indent=4)


def asciify(str):
    return re.sub(r'[^\x00-\x7F]',' ', str)


# Given a CSV phoneme string, return a corresponding phoneme bitstring
# That is, a string of 0s and 1s such that a 1 occurs at index i if and only if
# phonemeList[i] is found in csvStr
# phonemeList is a canonical list of the canonical phonemes to be used to create the string
def csvPhonemesToBitstring(csvStr, phonemeList):
    csvStr = csvStr.replace(ling_const.PHONEME_DELIMITER, "")
    csvList = csvStr.split(ling_const.INNER_DELIMITER)
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
