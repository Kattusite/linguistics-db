# Merge and anonymize the grammar/typology csv,
# Then convert it to a json file
# NOTE: I apologize in advance to any future developer (including myself)
# This whole file is a glorious mess, but last I checked it does work
# It would probably be worth streamlining significantly at some point
# (or rewriting entirely), as this is far from the best way

import csv, json, hashlib, re
from operator import itemgetter, attrgetter
from phonemes import consonants, vowels
from .const import * # todo make this clutter my namespace less (don't import *)
from . import selectors

########################################
DEBUG = False
VERBOSE = False
#########################################

DICT = selectors.DICT

#BUG Doesn't read correct encoding from csv, causing nonstandard chars to fail
# Read in the CSV files from the declared constant filenames, and then
# Return a JSON object representing that csv data
def csvToJSON():
    grammarCSV = open(DATA_PATH + "unanon-grammar.csv", "r", newline='', encoding='utf-8')
    grammarReader = csv.reader(grammarCSV)

    typologyCSV = open(DATA_PATH + "unanon-typology.csv", "r", newline='', encoding='utf-8')
    typologyReader = csv.reader(typologyCSV)

    # Anonymize netids and names
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
        # Just construct the JSON for now
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
            order = t_list[T_WORD_ORDER]
            orderDict = selectors.WORD_ORDER[DICT]
            parsedOrder = parsePhrase(order, orderDict, ["free", "seemingly free"])
            json_obj[T_STR[T_WORD_ORDER]] = parsedOrder

            ### Parse headedness into a short-name
            # NOTE "mixed" & "headedness" must occur together-  "mixed head-initial" (eg) makes no sense
            head = t_list[T_HEADEDNESS]
            hFreqDict = {
                "consistently": [],
                "mostly": [],
                "mixed": ["mixed", "equal", "roughly equal"]
            }
            hFreq = parsePhrase(head, hFreqDict, None)

            hModeDict = {
                "head-initial": [],
                "head-final": [],
                "headedness": ["mixed", "equal", "roughly equal"]
            }
            hMode = parsePhrase(head, hModeDict, None)
            json_obj[T_STR[T_HEADEDNESS]] = "%s %s" % (hFreq, hMode)

            ### Parse case and agreement into short-names
            case = t_list[T_CASE]
            agree = t_list[T_AGREEMENT]

            caDict = {
                "none": ["doesn't have", "none"],
                "ergative/absolutive": [],
                "nominative/accusative": [],
                "other": ["other", "some other", "other sort"]
            }

            json_obj[T_STR[T_CASE]]      = parsePhrase(case,  caDict, ["Has case"])
            json_obj[T_STR[T_AGREEMENT]] = parsePhrase(agree, caDict, ["Has agreement"])


        json_array.append(json_obj)
        # print(json_obj)

    # Sort the array by language, then name, netid hashes (for convenience)
    json_array = sorted(json_array, key=itemgetter("language", "name", "netid"))
    return json_array



def main():
    json_array = csvToJSON()

    # Open output files (CSV currently unused)
    # outputCSV = open(DATA_PATH + "anon-combined.csv", "w", newline='')
    # outputCSVWriter = csv.writer(outputCSV)

    outputJSON = open(DATA_PATH + "anon-combined.json", "w", encoding='utf-8')

    json.dump(json_array,
              outputJSON,
              sort_keys=False,
              ensure_ascii=False,
              indent=4)


def asciify(str):
    return re.sub(r'[^\x00-\x7F]',' ', str)


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
    # Ensure the fail-deadly list was not triggered
    # The fail-deadly acts as a primitive canary for changing data
    # If the program detects unfamiliar situations that it knows it *should* be able to handle,
    # it fails immediately to alert the programmer
    if bestStr is None and failList is not None:
        for f in failList:
            if f in phrase:
                raise ValueError("Fail-deadly triggered during phrase parsing: '%s' in '%s'" % (f, phrase))
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

main()
