""" Read the data from the grammar and typology CSV files,
    converting that data to a JSON format.

    Terminology:
    * A 'survey' is the raw data as it is collected by Google Forms,
      and the CSV files in which this raw data is exported.
    * A 'datapoint' or 'property' is a single aspect of a single language
      that can be captured and assigned a value; for example, country of
      origin, number of consonants, or list of consonants.
    * 'Language data' is a collection of all datapoints for a particular language.
    * A 'dataset' is a collection of language data for each student who collected
      data in a particular semester.
    * A 'survey specification' details which datapoints will appear in a
      particular semester's survey, and how those datapoints will be formatted.
      It includes information about how the specific questions and answers will
      be phrased, and at what index in the CSV row they can be found.

    Usage:
        python data/csv_to_json.py [-vvv] [datasets...]

        # Process all datasets known in const.py
        python data/csv_to_json.py

        # Process just the F21 dataset
        python data/csv_to_json.py F21

        # Process all files, then build the DBs too
        python -m data
"""

import argparse
from collections import defaultdict
import csv
import hashlib
import json
import logging
import operator
import pathlib
import re
import sys
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Type,
    Union,
)

from data import const, phonemes

# e.g. {'consonants': ['p', 't', 'k']}
# Note: the type imposes no restriction on the number of keys,
#       so a single datapoint has the same type as a collection
#       of datapoints. This makes them easy to merge with .update()
Datapoint = Dict[str, Union[str, int, bool, List[str]]]

DATASET_PATH = pathlib.Path('data/datasets/')

logging.basicConfig(stream=sys.stderr, level=logging.WARNING,
                    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger('csv_to_json')

################################################################################
#                                  HELPERS
################################################################################

def assert_type(x: Any, expected: Type) -> None:
    """ Raise a ValueError if x is not of the expected type. """
    if type(x) != expected:
        raise ValueError(f'Argument must have type {expected} not {type(x)} ({x})')

################################################################################
#                               LanguageData
################################################################################

Glyph = str

def get_glyph_list(s: str, phonemes: List[Glyph] = phonemes.GLYPHS) -> List[Glyph]:
    """ Given s, a CSV-formatted field consisting of many concatenated phonemes,
        split the list apart and return a list of the phoneme glyphs it contains.

        `phonemes` serves as the canonical list of which phonemes are considered valid.
    """
    # Note: some of the strings have "extra" information besides just the glyph,
    # such as: "including dental, alveolar, or postalveolar"

    # "/p/ ;/t/ (including dental, ...);/k/" -> ["/p/", "/t/ (incl...)", "/k/"]
    raw_glyphs = [glyph.strip() for glyph in s.split(const.INNER_DELIMITER)]

    # Remove selections like "None of the above"
    raw_glyphs = list(filter(lambda s: "None" not in s, raw_glyphs))

    # ["/p/", "/t/ (incl...)", "/k/"] -> [<match (/p/)>, <match (/t/)>, match (/k/)]
    # match at least one and at most 5 consecutive characters enclosed in /./
    # This isn't a perfect heuristic but should come close.
    matches = [re.search('/(.{1,5})/', g) for g in raw_glyphs]

    # If any glyphs weren't enclosed in /./ we cannot continue, as
    # there's a good chance the format of the data has changed.
    if not all(matches):
        raise ValueError("Survey contained phoneme without surrounding slashes: %s" % raw_glyphs)

    # [<match (/p/), ...] -> ['p', 't', 'k']
    glyphs = [match.group(1).replace(const.PHONEME_DELIMITER, '').strip() for match in matches]

    # Hardcode special case conversions (/Œ/ ==> /ɶ/)
    # This is because Google Forms had trouble rendering ɶ, and Œ was a fallback
    if "Œ" in glyphs:
        glyphs.remove("Œ")
        glyphs.append("ɶ")

    # Filter out any glyphs that don't appear in the canonical list
    filtered_glyphs = list(filter(lambda g: g in phonemes, glyphs))

    # It's OK to continue if some glyphs are filtered out;
    # maybe we just don't care about them this semester.
    removed_glyphs = set(glyphs).difference(set(filtered_glyphs))
    if removed_glyphs:
        logger.warning("Unrecognized glyphs were removed: %s", removed_glyphs)

    logger.debug("get_glyph_list mapped %s --> %s", repr(s), filtered_glyphs)
    return filtered_glyphs

def parse_phrase(phrase: str, spec: const.SurveySpecification) -> Optional[str]:
    """ Distill a complex phrase written in natural english down into one of a
        predefined set of strings, and return that predefined string.

        Operates according to a set of fuzzy matching rules determined by
        the parse_dict and fail_list attributes of the provided spec.

        Each key in parse_dict maps to a list of "search terms".
        For each search term, we compute a score equal to the length of the
        longest common substring between the phrase and search term.
        Each key inherits the score of its highest-scoring search term,
        and the highest-scoring key is declared the winner and returned.

        As syntactic sugar, a key is allowed to define an empty list of search
        terms, in which case the key itself will be offered as a search term.
        This is almost entirely a way to save typing when defining parse_dicts.

        The returned value will always be one of the keys of parse_dict.
        If two keys tie, this function will raise an error, as this indicates
        the parse_dict is ambiguous, and this algorithm cannot resolve that scenario.

        fail_list is used as a primitive canary to guard against subtle
        changes to survey questions.

        If no key earns any points, the function will check each entry in
        fail_list to determine if it appears in the phrase. If it does,
        the function will raise an error indicating that it believes it
        *should* have found a match, but was unable to. If fail list is not
        provided, or there is no match, return None.

        The motivation is that if the program detects unfamiliar or ambiguous
        situations that it knows it *should* be able to handle, it fails
        immediately to alert the programmer. """

    def generate_score_for_search_term(search_term: str, haystack: str) -> int:
        """ Return the score for a single search term against a given haystack. """
        return len(search_term) if search_term.lower() in haystack.lower() else 0

    def generate_score_for_key(key: str, spec: const.SurveySpecification, haystack: str) -> int:
        """ Return the highest score achieved by any of key's search terms. """
        # The key itself is a search term if no others are provided (shorthand to save typing)
        search_terms = spec.parse_dict.get(key) or [key]
        return max(generate_score_for_search_term(term, haystack) for term in search_terms)

    keys = spec.parse_dict.keys()
    scores = {key: generate_score_for_key(key, spec, phrase) for key in keys}
    max_score = max(scores.values())

    # Compute candidates for debugging, and to filter out entries with score 0.
    # This prevents all search terms from having a tie at 0 points.
    candidates = {key: score for key, score in scores.items() if score > 0}
    if len(candidates) > 1:
        logger.debug('Minor parse_phrase ambiguity: "%s" could be any of: %s', phrase, candidates)

    winners = [key for key, score in candidates.items() if score == max_score]
    if len(winners) > 1:
        raise RuntimeError(f'Severe parse_phrase ambiguity! "{phrase}" could be any of: {winners}')

    # If nothing won, check the fail list to see if we should abort.
    if not winners and spec.fail_list and any(f in phrase for f in spec.fail_list):
        raise RuntimeError(f'parse_phrase triggered fail-safe! "{phrase}" matched: {spec.fail_list}')

    winner = winners[0] if winners else None
    logger.debug('parse_phrase mapped %s --> %s', repr(phrase), repr(winner))

    return winner

class LanguageData(dict):
    """ A LanguageData object stores data about a single particular language.

        Contains the logic formerly known as parseDict, which is responsible
        for performing string matching and processing against the raw CSV data
        in order to coerce it into a standard format which will remain largely
        unchanged year-to-year, despite variations in the survey questions.
    """

    def extract_data_from_row(self, row: List[str], spec: const.SurveySpecification) -> Datapoint:
        """ Process the provided row according to the survey specification,
            extracting and returning a new Datapoint to be merged into self.
        """

        # Add a placeholder key to the language data to keep output nicely ordered.
        if spec.type == const.PLACEHOLDER:
            return {spec.key: const.PLACEHOLDER} # to be overwritten later.

        handlers = {
            const.ONE_TO_ONE:   self.process_one_to_one_mapping,
            const.SPLIT:        self.process_one_to_many_mapping,
            const.MERGE:        self.process_many_to_one_mapping,
        }
        return handlers[spec.mapping](row, spec)

    def process_one_to_one_mapping(self, row: List[str], spec: const.SurveySpecification) -> Datapoint:
        """ Process a one-to-one mapping in which a single column in the CSV maps
            to a single JSON key. Return the datapoints to be added to self. """
        assert_type(spec.key, str)
        assert_type(spec.index, int)

        # Get the single field from the CSV
        value = row[spec.index].strip()

        if spec.type == const.NUM:
            value = int(value)

        elif spec.type == const.STRING:
            # If there's a parse_dict, we need to do more advanced processing
            # Otherwise it's good as-is.
            if spec.parse_dict:
                value = parse_phrase(value, spec)

        elif spec.type == const.LIST:
            # If there's a parse_dict, parse each item individually
            if spec.parse_dict and spec.parse_dict != const.PHONEMES:
                selected_items = value.split(const.INNER_DELIMITER)
                value = [parse_phrase(item, spec) for item in selected_items]
            # If the parse_dict is absent or equal to const.PHONEMES, assume it's a phoneme list.
            else:
                # TODO: This should likely be torn out in favor of `get_glyph_list()`
                value = value.replace(const.PHONEME_DELIMITER, "")
                selected_items = value.split(const.INNER_DELIMITER)
                # Trim whitespace and filter out "None of the above"
                value = [s.strip() for s in selected_items if "None" not in s]

        else:
            raise NotImplementedError(f'this function cannot yet handle {spec.type=}')

        return {spec.key: value}

    def process_many_to_one_mapping(self, row: List[str], spec: const.SurveySpecification) -> Datapoint:
        """ Process a many-to-one mapping in which multiple columns in the CSV are
            merged into a single JSON key. Return the datapoints to be added to self. """
        assert_type(spec.key, str)
        assert_type(spec.index, list)

        # Currently this method is only used to combine multiple phoneme lists
        # into a larger phoneme list.
        if spec.type == const.LIST:
            assert spec.parse_dict in (None, const.PHONEMES), "this function cannot handle non-phoneme lists"

            # Append to the existing list of phonemes if one exists; start a new one otherwise.
            # TODO: Would there ever be an existing one??
            ret = {spec.key: self.get(spec.key, [])}
            if ret[spec.key]:
                logger.debug('many_to_one (%s) found existing entry: %s', spec.key, ret[spec.key])
                # I'm pretty sure there'd never be a case where this can happen, and I want to remove
                # the logic for it, so I'm adding this exception here so I notice if it ever does.
                # It's not *bad* if this exception comes up, it should be fine, but I'm just surprised.
                # If it raises, figure out why and replace the error with an explanatory comment.
                raise NotImplementedError("I assumed this case would be impossible. Figure out why it's not and remove this error.")
            for index in spec.index:
                selected_items = row[index]
                ret[spec.key] += get_glyph_list(selected_items, phonemes.GLYPHS)

        else:
            raise NotImplementedError(f'this function cannot yet handle {spec.type=}')

        return ret

    def process_one_to_many_mapping(self, row: List[str], spec: const.SurveySpecification) -> Datapoint:
        """ Process a one-to-many mapping in which a single column in the CSV is split
            across multiple JSON keys. Return the datapoints to be added to self. """
        assert_type(spec.key, list)
        assert_type(spec.index, int)

        # Currently this method is only used to pull each of a list of checkboxes into their own bools.
        selected_items = row[spec.index].strip().split(const.INNER_DELIMITER)

        if spec.type == const.BOOL:
            # Set a key's value to True if that key appears in the text of any selected item.
            # This is quick and dirty but it works (so far...)
            # e.g. "tone" appears in ['The language has tone ...', 'The language has complex consonants']
            ret = {key: any(key in text for text in selected_items)
                        for key in spec.key}
        else:
            raise NotImplementedError(f'this function cannot yet handle {spec.type=}')

        return ret


    @classmethod
    def from_csv_row(cls: 'LanguageData', row: List[str],
                     survey_specs: List[const.SurveySpecification]) -> 'LanguageData':
        """ Process the data from a single CSV row into a standardized format
            by feeding each item into the format specification for this semester.
        """
        logger.info('----- Parsing %s with netid %s -----',
                    row[const.LANGUAGE], row[const.NETID])

        data = cls()

        # Extract all raw data from the row
        # Each spec represents a datapoint to be extracted from this row.
        for spec in survey_specs:
            datapoint = data.extract_data_from_row(row, spec)
            data.update(datapoint)

        # Apply post-processing, sorting, etc.


        # Compute all derived properties for this row.
        # (Properties that can be derived from existing raw data,
        #  e.g. counting # of manners, # of places)

        # Only derive consonant counts for the grammar survey, not the typology survey
        if const.K_CONSONANTS in data:
            consonant_glyphs = data[const.K_CONSONANTS]
            data[const.K_NUM_CONSONANT_MANNERS] = phonemes.consonants.getNumMannersFromGlyphs(consonant_glyphs)
            data[const.K_NUM_CONSONANT_PLACES] = phonemes.consonants.getNumPlacesFromGlyphs(consonant_glyphs)

        return data

################################################################################
#                                 Dataset
################################################################################

def get_path(semester: str, survey: str, anonymized: bool = True) -> Optional[pathlib.Path]:
    """ Return the Path to the CSV data file for the given inputs, or None if no such file exists. """
    # Note: data.datasets defines helpers like this as well... Maybe I should have used those?
    prefix = "anon" if anonymized else "unanon"
    return DATASET_PATH / semester / f'{prefix}-{survey}.csv'

class Dataset:
    """ A Dataset consists of a collection of LanguageData for a given semester.

        There will be one LanguageData entry per language studied.
    """
    def __init__(self, languages: Iterable[LanguageData]):
        self.languages = list(languages)

        # Sort from A-Z by language name, then student / netid hashes.
        self.languages.sort(key=operator.itemgetter(const.K_LANGUAGE, const.K_NAME, const.K_NETID))

    @classmethod
    def from_semester(cls: 'Dataset', semester: str) -> 'Dataset':
        """ Read the CSV files for the requested semester, using them
            to construct a Dataset containing the results.

            Return the newly constructed Dataset.
        """

        logger.info('===== Processing semester %s =====', semester)

        # Map netids to the LanguageData collected by that netid.
        # We start with a blank LanguageData for each netid
        netid_to_language_data = defaultdict(lambda: LanguageData())

        # For test datasets, use the specs of the corresponding non-test dataset.
        _semester = semester.replace("test", "")

        # If we haven't defined a format spec for this semester we won't know
        # how to process any of its data. Don't even attempt to continue.
        if _semester not in const.PARAMS:
            raise KeyError(f'Could not find format specification for {semester} in const.PARAMS')

        logger.info('Using SurveySpecification: %s', _semester)
        survey_specs = const.PARAMS[_semester]

        # Merge in grammar data first, followed by typology data.
        # It's not guaranteed we'll have both for each language.
        for survey in const.SURVEYS:
            path = get_path(semester, survey)
            if not path.exists():
                logger.warning('%s semester: no anon CSV found for %s survey. Continuing without it...',
                               semester, survey)
                continue

            with open(path, 'r', newline='', encoding='utf-8') as f:
                rows = list(csv.reader(f))

            # Skip first row as it's just a header.
            languages = [LanguageData.from_csv_row(row, survey_specs[survey]) for row in rows[1:]]

            for language_data in languages:
                # Merge data from this survey into any other data we
                # may have for the same language from other surveys.
                try:
                    netid = language_data[const.K_NETID]
                except KeyError:
                    raise KeyError('language_data had no netid field: %s' % language_data)
                existing_data = netid_to_language_data[netid]

                # Warn if any old data is being clobbered by new (non-identical) data.
                for key, new_value in language_data.items():
                    old_value = existing_data.get(key)
                    if old_value and old_value != new_value:
                        logger.warning('conflict: netid %s had multiple %s values (old: %s, new: %s)',
                                       netid, key, old_value, new_value)

                        # Remain consistent with legacy behavior, which was to give priority
                        # to the new value. (I think this is the default, but be explicit)
                        language_data[key] = new_value

                existing_data.update(language_data)

        # We need the netids map to allow us to aggregate all of a student's
        # data across multiple surveys. Once we're done processing, though,
        # all we really care about are the values.
        return cls(netid_to_language_data.values())

    def dump(self, path: Union[str, pathlib.Path]):
        """ Dump the contents of this Dataset to a JSON file at the provided path. """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.languages, f, sort_keys=False, ensure_ascii=False, indent=4)

################################################################################
#                               Preprocessing
################################################################################

def str_hash(s: str) -> str:
    """ Convert s to a standard normal form and return a hash for it. """
    # Remove extra spaces and standardize capitalization.
    s = s.strip().lower()

    # Convert to ASCII bytes.
    b = re.sub(r'[^\x00-\x7F]',' ', s).encode('ASCII')

    # Generate a hash and trim off just the front for brevity.
    # The risk of collisions should still be negligible.
    return hashlib.sha3_256(b).hexdigest()[:const.HASH_SIZE]

def anonymize_semester_data(semester: str) -> None:
    """ Convert the given semester's "unanon" CSV files to "anon" ones.
        Log a warning and return gracefully if an "unanon" file doesn't exist. """
    logger.info('Anonymizing semester data...')
    for survey in const.SURVEYS:
        path = get_path(semester, survey, anonymized=False)
        if not path.exists():
            logger.info('%s semester: no unanon CSV found for %s survey. Continuing without it...',
                               semester, survey)
            continue

        logger.info('Anonymizing %s ...', str(path))

        # Files will be pretty small, so we just read the whole thing into memory.
        with open(path, 'r', newline='', encoding='utf-8') as f:
            rows = list(csv.reader(f))

        path = get_path(semester, survey)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write the first row as-is, since it's just headers.
            writer.writerow(rows[0])
            for row in rows[1:]:
                # Anonymize sensitive data and write back to file.
                row[const.NETID] = str_hash(row[const.NETID])
                row[const.NAME] = str_hash(row[const.NAME])
                writer.writerow(row)

################################################################################
#                               Main Processing
################################################################################

def get_log_level(verbosity: int) -> int:
    """ Return the logging level associated with a particular verbosity. """
    levels = [
        logging.WARNING,    # default
        logging.INFO,       # -v
        logging.DEBUG,      # -vv
    ]

    # clamp verbosity to be a legal index
    verbosity = min(verbosity, len(levels))
    verbosity = max(verbosity, 0)
    return levels[verbosity]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='increase output verbosity')
    parser.add_argument('semesters', nargs='*',
                        help="which semesters' datasets to be converted")
    args = parser.parse_args()

    logger.setLevel(get_log_level(args.verbosity))

    # If no semesters requested, process all known semesters, skipping test data.
    semesters: List[str] = args.semesters or const.datasetNames

    # Datasets whose names begin with "_" are for testing only.
    # Exclude them from the conversion process.
    is_production_dataset = lambda s: not s.startswith('_')
    semesters = list(filter(is_production_dataset, semesters))

    for semester in semesters:
        # Create the anon-{survey}.csv file from the unanon-{survey} file.
        # Continue gracefully if the original unanon files are absent.
        anonymize_semester_data(semester)

        # Process the anon-{survey}.csv files for each survey
        dataset = Dataset.from_semester(semester)

        json_path = DATASET_PATH / semester / f'{semester}.json'
        dataset.dump(json_path)


if __name__ == '__main__':
    main()

