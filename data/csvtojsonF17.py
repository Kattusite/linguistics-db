# Merge and anonymize the grammar/typology csv,
# Then convert it to a json file
# NOTE: I apologize in advance to any future developer (including myself)
# This whole file is a glorious mess, but last I checked it does work
# It would probably be worth streamlining significantly at some point
# (or rewriting entirely), as this is far from the best way

import csv, json, hashlib, re, sys
from operator import itemgetter, attrgetter
from phonemes import consonants, vowels
from .const import *
from . import selectors

# Warning: the import * from .const means the namespace is horribly cluttered
# I'd like to fix it one day by removing this import

########################################
DEBUG = False
VERBOSE = False
#########################################

DICT = selectors.DICT

# Read in the CSV files from the declared constant filenames, and then
# Return a JSON object representing that csv data
def csvToJSON(datasetName):

    noFileErr = "{0} file {1} not found for dataset {2}. Continuing without it..."
    gFilename = "unanon-grammar.csv"
    tFilename = "unanon-typology.csv"

    validGrammar = True
    validTypology = True

    # Locate the grammar CSV file if it exists, and open it for reading
    try:
        grammarCSV = open(DATASET_PATH.format(datasetName, gFilename),
                            "r", newline='', encoding='utf-8')
        grammarReader = csv.reader(grammarCSV)
    except FileNotFoundError:
        print(noFileErr.format("Grammar", gFilename, datasetName), file=sys.stderr)
        validGrammar = False

    # Locate the typology CSV file if it exists, and open it for reading
    try:
        tFilename = "unanon-typology.csv"
        typologyCSV = open(DATASET_PATH.format(datasetName, tFilename),
                            "r", newline='', encoding='utf-8')
        typologyReader = csv.reader(typologyCSV)
    except FileNotFoundError:
        print(noFileErr.format("Typology", tFilename, datasetName), file=sys.stderr)
        validTypology = False

    # Anonymize netids and names
    # These are dicts mapping (anonymous) netids to their CSV data
    g_data = anonymize(grammarReader, datasetName, "anon-grammar.csv")   if validGrammar  else {}
    t_data = anonymize(typologyReader, datasetName, "anon-typology.csv") if validTypology else {}

    # Merge netid lists to get list of all students with any sort of data
    g_netids = set(g_data.keys())
    t_netids = set(t_data.keys())
    netidSet = g_netids.union(t_netids)

    # NOTE: If neither grammar/typology file exists, netidSet = (), and we skip the loop

    # For each anon netid, print a row of csv and create a dict for JSON
    json_array = []
    for id in netidSet:
        # Just construct the dict for now
        g_list = g_data.get(id)
        t_list = t_data.get(id)
        json_obj = {}

        # Decide on the language name
        language = g_list[G_LANGUAGE] if g_list else (t_list[T_LANGUAGE] if t_list else "unknown")

        # Print info about currently parsing language
        if (VERBOSE):
            print("\n======== Parsing %s with netid %s =========" % (language, id))

        if g_list is not None:
            # Extract simple grammar attributes
            json_obj[G_STR[G_LANGUAGE]]        = g_list[G_LANGUAGE].strip()
            json_obj[G_STR[G_NAME]]            = g_list[G_NAME]
            json_obj[G_STR[G_NETID]]           = g_list[G_NETID]
            json_obj[G_STR[G_NUM_VOWELS]]      = g_list[G_NUM_VOWELS]
            json_obj[G_STR[G_NUM_CONSONANTS]]  = g_list[G_NUM_CONSONANTS]
            json_obj[G_STR[G_NUM_PHONEMES]]    = g_list[G_NUM_PHONEMES]

            # Extract phoneme lists
            consonantGlyphs = csvConsonantsToGlyphList(g_list[G_CONSONANTS])
            vowelGlyphs     = csvVowelsToGlyphList(g_list[G_VOWELS])

            json_obj[G_STR[G_CONSONANTS]] = consonantGlyphs
            json_obj[G_STR[G_VOWELS]]     = vowelGlyphs

            # Figure out the manners / places of articulation
            # TODO remove hardcoded values
            json_obj[G_STR[G_NUM_PLACES]]  = consonants.getNumPlacesFromGlyphs(consonantGlyphs)
            json_obj[G_STR[G_NUM_MANNERS]] = consonants.getNumMannersFromGlyphs(consonantGlyphs)

            # Extract phonetic + syllable info
            phonetic = g_list[G_PHONETIC].split(INNER_DELIMITER)
            syllables = g_list[G_SYLLABLES].split(INNER_DELIMITER)

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

            # Process syllables

            # Search raw CSV fields for containing correct attribute names
            # (but not containing other names e.g. CV matches CV not CCV)
            sylDict = selectors.SYLLABLE[DICT]
            sylList = [parsePhrase(s, sylDict, ["VC", "CV"]) for s in syllables]
            json_obj[G_STR[G_SYLLABLES]] = sylList


        if t_list is not None:
            # NOTE: "Language" field may be overwritten, so if data is inconsistent on
            # spelling there will be potential issues
            # Extract simple typology attributes
            json_obj[T_STR[T_LANGUAGE]]        = t_list[T_LANGUAGE].strip()
            json_obj[T_STR[T_CITATION]]        = t_list[T_CITATION]
            json_obj[T_STR[T_RECOMMEND]]       = t_list[T_RECOMMEND]

            ### Parse morphological type into a list of short-names
            morph = t_list[T_MORPHOLOGY].split(INNER_DELIMITER)
            morphDict = selectors.MORPHOLOGY[DICT]
            morphList = [parsePhrase(m, morphDict, None) for m in morph]
            json_obj[T_STR[T_MORPHOLOGY]] = morphList


            ### Parse word formation into a list of short-names
            wf = t_list[T_WORD_FORMATION].split(INNER_DELIMITER)
            wfDict = selectors.WORD_FORMATION[DICT]
            wfList = [parsePhrase(w, wfDict, None) for w in wf]
            json_obj[T_STR[T_WORD_FORMATION]] = wfList

            ### Parse word formation freq into a short-name
            #json_obj[T_STR[G_NUM_CONSONANTS]]  = t_list[G_NUM_CONSONANTS]
            wfFreq = t_list[T_FORMATION_FREQ].lower()

            # extract frequency from morph
            freqDict = selectors.FORMATION_FREQ[DICT]
            freq = parsePhrase(wfFreq, freqDict, None)
            if freq is None:
                raise ValueError("Failed to parse morphological type")

            modeDict = selectors.FORMATION_MODE[DICT]
            mode = parsePhrase(wfFreq, modeDict, [" and "])
            if mode is None:
                raise ValueError("Failed to parse morphological type")

            json_obj[T_STR[T_FORMATION_FREQ]] = "%s %s" % (freq, mode)

            ### Parse word order into a short-name
            order = t_list[T_WORD_ORDER].split(INNER_DELIMITER)
            orderDict = selectors.WORD_ORDER[DICT]
            orderList = [parsePhrase(o, orderDict, ["free", "seemingly free"]) for o in order]
            json_obj[T_STR[T_WORD_ORDER]] = orderList

            ### Parse headedness into a short-name
            # NOTE "mixed" & "headedness" must occur together-  "mixed head-initial" (eg) makes no sense
            head = t_list[T_HEADEDNESS]
            hFreqDict = selectors.HEADEDNESS_FREQ[DICT]
            hFreq = parsePhrase(head, hFreqDict, None)

            hModeDict = selectors.HEADEDNESS_MODE[DICT]
            hMode = parsePhrase(head, hModeDict, None)
            # HACK: This needs to be a list to be able to use Language.matchXxxxYyyy methods naturally
            # TODO: Find a more elegant way of doing things
            hList = ["%s %s" % (hFreq, hMode)]
            json_obj[T_STR[T_HEADEDNESS]] = hList

            ### Parse case and agreement into short-names
            case = t_list[T_CASE]
            agree = t_list[T_AGREEMENT]

            caseDict = selectors.CASE[DICT]
            agreeDict = selectors.AGREEMENT[DICT]

            json_obj[T_STR[T_CASE]]      = parsePhrase(case,  caseDict, ["Has case"])
            json_obj[T_STR[T_AGREEMENT]] = parsePhrase(agree, agreeDict, ["Has agreement"])


        json_array.append(json_obj)
        # print(json_obj)

    # Sort the array by language, then name, netid hashes (for convenience)
    json_array = sorted(json_array, key=itemgetter("language", "name", "netid"))
    return json_array


def asciify(str):
    return re.sub(r'[^\x00-\x7F]',' ', str).encode('ASCII')


# Given a CSV phoneme string, return a corresponding phoneme list
# phonemeList is a canonical list of the canonical phonemes to be used to create the string
def csvPhonemesToGlyphList(csvStr, phonemeList):
    csvStr  = csvStr.replace(PHONEME_DELIMITER, "")
    csvList = csvStr.split(INNER_DELIMITER)

    # Iterate over canonical list and match against csvList
    glyphList = [p for p in csvList if p in phonemeList]
    return glyphList

# Given a csvStr representing a csv formatted list of consonants, return
# the corresponding list of consonants, using consonants.GLYPHS as the
# canonical list
def csvConsonantsToGlyphList(csvStr):
    return csvPhonemesToGlyphList(csvStr, consonants.GLYPHS)

# Given a csvStr representing a csv formatted list of vowels, return
# the corresponding list of vowels, using vowels.GLYPHS as the
# canonical list
def csvVowelsToGlyphList(csvStr):
    return csvPhonemesToGlyphList(csvStr, vowels.GLYPHS)


# A better metric to use than "longest match" might be "largest percentage of phrase matched
##
# A function for reducing complex phrases into a predefined set of strings...wwwwww
# Given phrase, a string, and matchDict (a str-> list dictionary), search phrase
# for occurences of any of the strings in the lists of matchDict.
# Return the key associated with the list of the longest match detected
# If no match is detected, ensure that none of the strings in failList are matched
# If they are, raise an error indicating the parsing dict was not strong enough
# Syntactic sugar: If matchDict contains:
#  str: []   (a string associated with an empty list), then the key str will be
# added to that list automatically (to save typing)
## Could probably be reframed to work with regexps, but that seems a bit much
# The purpose of this function is to protect against needing to change the code every
# time a tiny change is made to the data
# failList: Things that *should* have matched but did not.
def parsePhrase(phrase, matchDict, failList):
    keys = matchDict.keys()
    bestNum = 0
    bestStr = None
    for key in keys:
        matchList = matchDict[key]
        # Add key itself to empty lists (a shorthand to save typing)
        if len(matchList) == 0:
            matchList.append(key)
        matchLen = matchAnyInList(phrase, matchList)
        # Cannot resolve ambiguous matches! Programmer needs better matchDict
        if matchLen != 0 and matchLen == bestNum:
            raise ValueError("Strongly ambiguous match in parsePhrase('%s') : %s, %s" % (phrase, bestStr, key))
        # If this match is unambiguously stronger, it is the new match
        if matchLen > bestNum:
            if bestNum != 0 and VERBOSE:
                print("Resolving semiambiguous match in parsePhrase('%s') : %s, %s" % (phrase, bestStr, key))
            bestNum = matchLen
            bestStr = key
    # Ensure the fail-safe list was not triggered
    # The fail-safe acts as a primitive canary for changing data
    # If the program detects unfamiliar situations that it knows it *should* be able to handle,
    # it fails immediately to alert the programmer
    if bestStr is None and failList is not None:
        for f in failList:
            if f in phrase:
                raise ValueError("Fail-safe triggered during phrase parsing: '%s' in '%s'" % (f, phrase))
    if (DEBUG):
        print("Parsing... %s \n==> %s" % (phrase, bestStr))
    return bestStr


# Given a string str and list lst, return the length of the longest string in lst
# that was contained in str, or 0 if no match was found.
# Comparisons are case insensitive
def matchAnyInList(str, lst):
    str = str.lower()
    best = 0
    for s in lst:
        if s.lower() in str:
            best = max(best, len(s))
    return best

# Given a CSV reader, return a dictionary whose keys are anonymized versions of
# each student in the CSV's netid, and whose values are the associated student's
# data
# Additionally, write the anonymized CSV to the file specified by outFilename,
# if it is not None
def anonymize(csvReader, dataset, outFilename=None):

    if (outFilename):
        outFile = open(DATASET_PATH.format(dataset, outFilename), "w", encoding="utf-8")
        outCSV = csv.writer(outFile)

    dataDict = {}
    for i, row in enumerate(csvReader):
        # If this is the header row, skip anonymization. Print as-is if printing enabled
        if i == 0:
            if outFilename:
                outCSV.writerow(row)
            continue
        netid = asciify(row[NETID])
        name  = asciify(row[NAME])

        # Slice off first few chars to make hashes manageable (collisions negligible)
        anon_netid = hashlib.sha3_256(netid).hexdigest()[:HASH_SIZE]
        anon_name  = hashlib.sha3_256(name).hexdigest()[:HASH_SIZE]

        # Replace the original personal info w/ anonymized versions
        row[NETID] = anon_netid
        row[NAME]  = anon_name

        # Put each student's data into the dictionary to be returned
        dataDict[anon_netid] = row

        # If we are writing, write this row to file
        if outFilename:
            outCSV.writerow(row)

    # Finish up
    outFile.flush()
    outFile.close()
    return dataDict

def main():
    """If command line args are provided, treat them as dataset names and convert
    all these datasets from their raw CSV format to more structured JSON, outputting
    a file /data/datasets/<datasetName>/<datasetName>.json for each one. By default,
    if no command line args are provided, convert all known datasets in the same way
    as described above"""

    # If arguments are provided, treat them as dataset names and parse those files only.
    # Note: dataset names are like (F17, S19), without a file extension
    if len(sys.argv) > 1:
        names = sys.argv[1:]
    # Otherwise, parse all known datasets
    else:
        names = datasetNames # from const

    # Convert each file CSV -> JSON and write it to disk.
    for name in names:
        # Names prefixed with _ are for testing purposes only
        if (name[0] == "_"):
            continue

        jsonArr = csvToJSON(name)

        # Open output files (CSV currently unused)
        outName = name + ".json"
        outFile = open(DATASET_PATH.format(name, outName), "w", encoding='utf-8')

        json.dump(jsonArr,
                  outFile,
                  sort_keys=False,
                  ensure_ascii=False,
                  indent=4)

        outFile.flush()
        outFile.close()

if __name__ == '__main__':
    main()
