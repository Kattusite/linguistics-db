# Merge and anonymize the grammar/typology csv,
# Then convert it to a json file
# NOTE: I apologize in advance to any future developer (including myself)
# This whole file is a glorious mess, but last I checked it does work
# It would probably be worth streamlining significantly at some point
# (or rewriting entirely), as this is far from the best way

# Usage:
# python -m data

import csv, json, hashlib, re, sys
from operator import itemgetter, attrgetter
from phonemes import consonants, vowels, phonemes
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

    # Get the CSV -> JSON parameters for this dataset from const.py
    # If "test" is in the dataset name, use the params for the non-test version
    if "test" in datasetName:
        params = PARAMS[datasetName.replace("test", "")]
    else:
        params = PARAMS[datasetName]

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
            g_params = params[GRAMMAR]
            json_obj = convertRow(g_list, g_params, json_obj)

            # Now this lang's grammar CSV data is all in the standardized JSON format
            # Set the values of derived fields (e.g. counting # of manners, places)
            json_obj[K_NUM_CONSONANT_PLACES]  = consonants.getNumPlacesFromGlyphs(json_obj[K_CONSONANTS])
            json_obj[K_NUM_CONSONANT_MANNERS] = consonants.getNumMannersFromGlyphs(json_obj[K_CONSONANTS])

        if t_list is not None:
            # NOTE: "Language" field may be overwritten, so if data is inconsistent on
            # spelling there will be potential issues
            t_params = params[TYPOLOGY]
            json_obj = convertRow(t_list, t_params, json_obj)

        json_array.append(json_obj)
        # print(json_obj)

    # Sort the array by language, then name, netid hashes (for convenience)
    json_array = sorted(json_array, key=itemgetter("name", "student", "netid"))
    return json_array


# Convert a single row of a CSV file into a json object, given parameters specifying
# how to interpret that row, then return the json as a python dictionary.
# If an old_json is provided, modify the existing one instead of starting from scratch
def convertRow(row, params, old_json=None):

    json_obj = old_json if old_json else {}

    # Iterate over params for this dataset, building a json obj.
    for param in params:
        key   = param[KEY]

        # Add a placeholder key to JSON to keep the output nicely ordered
        if param[TYPE] == PLACEHOLDER:
            json_obj[key] = PLACEHOLDER # To be overwritten later
            continue

        index = param[INDEX]

        # Get the field if there is a single unique field described
        field = row[index] if type(index) == type(1) else None

        # If one to one mapping, one question ==> one key in json
        if param[MAPPING] == ONE_TO_ONE:
            assert type(key)   == type("str") # single key
            assert type(index) == type(1)     # single index

            # If TYPE is string...
            #     If no DICT provided, store value as is
            #     If DICT provided, match this string against it, store result
            if param[TYPE] == STRING:
                if DICT in param:
                    failDict = param.get(FAIL_DICT)
                    parseDict = param[DICT]
                    val = parsePhrase(field, parseDict, failDict)
                else:
                    val = field.strip()

            # If TYPE is num, cast value to int, then store it
            if param[TYPE] == NUM:
                val = int(field)

            # If TYPE is bool, undefined (currently unused)
            if param[TYPE] == BOOL:
                val = None
                raise NotImplementedError("csvtojson: one-to-one bools not yet supported")

            # If TYPE is list...
            #     If DICT is provided, store all keys in DICT whose arrays match value
            #     If DICT not provided (or == "phonemes"), assume phoneme list
            if param[TYPE] == LIST:
                if DICT not in param or param[DICT] == PHONEMES:
                    # delete this. already have a function
                    selected = field.replace(PHONEME_DELIMITER, "")
                    selected = selected.split(INNER_DELIMITER)
                    # Remove whitespace and "None of the above"
                    val = [s.strip() for s in selected if "None" not in s]
                else:
                    failDict = param.get(FAIL_DICT) # may not exist, thats OK
                    parseDict = param[DICT]         # should def. exist
                    selected = field.split(INNER_DELIMITER)
                    val = [parsePhrase(sel, parseDict, failDict) for sel in selected]

            # Store the result
            json_obj[key] = val


        # If split mapping, one question ==> many keys in json
        elif param[MAPPING] == SPLIT:
            assert type(key)   == type([])  # many keys
            assert type(index) == type(1)   # single index

            # If TYPE is string, undefined (currently unused)
            # If TYPE is num,    undefined (currently unused)
            # If TYPE is list,   undefined (currently unused)
            if param[TYPE] != BOOL:
                val = None
                raise NotImplementedError("csvtojson: split not yet supported for non-bools")

            # If TYPE is bool...
            #     Iterate over keys, setting the ith val to True
            #     if the ith search term (of DICT?) appears in value
            if param[TYPE] == BOOL:
                selected = field.split(INNER_DELIMITER)
                # All false to start
                for k in key:
                    json_obj[k] = False

                # If a key appears in any of the selected strings, set that key's val to true
                for sel in selected:
                    for k in key:
                        if k in sel:
                            json_obj[k] = True


        # If merge mapping many questions ==> one key in json
        elif param[MAPPING] == MERGE:
            assert type(key)   == type("str")  # single key
            assert type(index) == type([])     # many indices

            # If TYPE is string, undefined (currently unused)
            # If TYPE is num,    undefined (currently unused)
            # If TYPE is bool,   undefined (currently unused)
            if param[TYPE] != LIST:
                val = None
                raise NotImplementedError("csvtojson: merge not yet supported for non-lists")

            # If TYPE is list...
            #     If DICT is provided, store all keys in DICT whose arrays match value
            #     If DICT not provided or == "phonemes", assume phoneme list
            #     In either case, append the newly added values to the existing val
            if param[TYPE] == LIST:
                val = json_obj.get(key, []) # Get existing list, or new one if none exists

                if DICT not in param or param[DICT] == PHONEMES:

                    for i in index:
                        field = row[i]
                        val += csvPhonemesToGlyphList(field, phonemes.GLYPHS)

                else:
                    raise NotImplementedError("csvtojson: merge not yet supported for non-phoneme lists")

                json_obj[key] = val

    # All params have been read from this row. Return the updated json obj
    return json_obj



def asciify(str):
    return re.sub(r'[^\x00-\x7F]',' ', str).encode('ASCII')


# Given a CSV phoneme string, return a corresponding phoneme list
# phonemeList is a canonical list of the canonical phonemes to be used to create the string
def csvPhonemesToGlyphList(csvStr, phonemeList):
    csvStr  = csvStr.replace(PHONEME_DELIMITER, "") # remove /../
    csvList = csvStr.split(INNER_DELIMITER)         # str --> list
    csvList = [s.strip() for s in csvList]          # remove whitespace

    # Hardcode special case conversions (/Œ/ ==> /ɶ/)
    # This is because Google Forms had trouble rendering ɶ, and Œ was a fallback
    if "Œ" in csvList:
        csvList.remove("Œ")
        csvList.append("ɶ")

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


def matchSingle(phrase, matchDict, key):
    """Match a single key's matchDict entry against the given phrase, and
    return the longest match in the matchDict[key] list"""

    matchList = matchDict[key]
    # Add key itself to empty lists (a shorthand to save typing)
    if len(matchList) == 0:
        matchList.append(key)
    matchLen = matchAnyInList(phrase, matchList)

    return matchLen

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

        # Find longest match for this key
        matchLen = matchSingle(phrase, matchDict, key)

        # If this match is unambiguously stronger, it is the new match
        if matchLen > bestNum:
            if bestNum != 0 and VERBOSE:
                print("Resolving semiambiguous match in parsePhrase('%s') : %s, %s" % (phrase, bestStr, key))
            bestNum = matchLen
            bestStr = key

    # Once a best match was found, make sure there is no tie.
    # Tie suggests an ambiguously defined parseDict, which this algorithm can't resolve
    for key in keys:
        # Skip the current best -- obviously it would tie with itself
        if key == bestStr:
            continue

        matchLen = matchSingle(phrase, matchDict, key)

        if matchLen != 0 and matchLen == bestNum:
            raise RuntimeError("Strongly ambiguous len %s match in parsePhrase('%s') : %s, %s" % (bestNum, phrase, bestStr, key))


    # Ensure the fail-safe list was not triggered
    # The fail-safe acts as a primitive canary for changing data
    # If the program detects unfamiliar situations that it knows it *should* be able to handle,
    # it fails immediately to alert the programmer
    if bestStr is None and failList is not None:
        for f in failList:
            if f in phrase:
                raise RuntimeError("Fail-safe triggered during phrase parsing: '%s' in '%s'" % (f, phrase))
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
# Slight bug: Note that the anonymized files currently have \r\n line endings
# instead of \n line endings, which causes minor annoyances when displaying CSVs,
# but the parsing process is unaffected.
def anonymize(csvReader, dataset, outFilename=None):

    if (outFilename):
        outFile = open(DATASET_PATH.format(dataset, outFilename), "w", newline='', encoding="utf-8")
        outCSV = csv.writer(outFile)

    dataDict = {}
    for i, row in enumerate(csvReader):
        # If this is the header row, skip anonymization. Print as-is if printing enabled
        if i == 0:
            if outFilename:
                outCSV.writerow(row)
            continue

        # Students sometimes add extra spaces or change capitalization
        # So we need to normalize for this so the hashes will be the same
        netid = asciify(row[NETID].strip().lower())
        name  = asciify(row[NAME].strip().lower())

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
