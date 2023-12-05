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
from collections.abc import Sequence
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

from data import const
from data.const import Datasets, FuzzySearchTerms, JsonKey, Mappings, Semesters, Surveys, ValueType

import phonemes

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
    if not isinstance(x, expected):
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

def fuzzy_match_phrase(phrase: str, spec: const.SurveySpecification) -> Optional[str]:
    """ Fuzzily match a phrase written in natural English against a predefined
    set of strings, and return the predefined string that is the closest match.

    The fuzzy matching process follows a set of rules described below,
    governed by configuration specified in `spec.fuzzy_search_terms` and
    `spec.poisoned_search_terms`.

    `spec.fuzzy_search_terms`:
        The keys of `spec.fuzzy_search_terms` define the set of possible
        "candidate" matches that may be returned. This function's goal is
        to return the candidate which is most "similar" to `phrase`.

        Each value of `spec.fuzzy_search_terms` is a list of "search terms"
        associated with that candidate. We consider `phrase` to be "similar" to a
        candidate if `phrase` is similar to any of that candidate's search terms.

        As syntactic sugar, a candidate may map to an empty list of search terms.
        In this case, the candidate itself is offered as a search term. This is
        purely a convenience, to save typing when defining `fuzzy_search_terms`.

        An example `fuzzy_search_terms` might look like this:

        spec.fuzzy_search_terms = {
            'berry':        ['acai berry',  'blueberry',    'cranberry', ...],
            'fruit':        ['apple',       'banana',       'cherry', ...],
            'vegetable':    ['artichoke',   'broccoli',     'carrot', ...],
        }

        If `phrase` is similar to 'apple', 'banana', or 'cherry', we consider
        `phrase` to be similar to 'fruit' as well. If `phrase` is more similar
        to 'fruit' than any other candidate, 'fruit' is the most similar match,
        and we will return it.


    `spec.poisoned_search_terms`:
        Our fuzzy matching scheme is not perfect, and false negatives may occur;
        that is -- cases where we expect we should have found some candidate match
        that is similar to `phrase`, but we actually found none.
        `poisoned_search_terms` acts as a safeguard against these false negatives.

        Often, this scenario arises when the exact wording of survey questions or
        answers changes from year to year. These changes may make it so that a
        phrase that *would* have found a match in a past semester no longer does
        in a more recent semester, which would result in a false negative.

        The intention is that the poisoned search terms act as a basic canary;
        if `phrase` matches a poisoned search term, but does not match any of the
        fuzzy search terms, we can infer that a false negative has occurred:
        `phrase` was familiar enough that we know we *should* have been able to
        find a matching candidate for it, but for whatever reason we couldn't
        actually identify a suitable match.

        Usually this indicates that `spec.fuzzy_search_terms` is out of sync with
        the current semester's survey questions, and the remedy is to tailor this
        semester's fuzzy search terms more closely to the actual survey.

        An example `poisoned_search_terms` might look like this:

        spec.poisoned_search_terms = [
            'berry',
            'melon',
        ]

        If `phrase` was similar to "berry" or "melon", but we were unable to match
        `phrase` to either the "berry" or "fruit" candidate, something's likely
        gone wrong, even if we're not sure exactly what.

        If we can't tell that "strawberry" matches "berry", or "watermelon" matches
        fruit, maybe we need to take a closer look at refining the fuzzy search terms.


    Similarity:
        Let's rigorously define "similarity" as an integer indicating how closely
        a phrase matches a particular candidate (and its search terms).

        Similarity between `phrase` and a search term is defined as the length of
        the search term, if the search term is a substring of `phrase`, or else 0.

        Similarity between `phrase` and a candidate is defined as the maximum
        similarity between `phrase` and any of the candidate's search terms.

        To determine a match for a given `phrase`, we will find the similarity
        score of that phrase with each candidate. Often there is just one
        candidate with a nonzero similarity score; such cases are "unambiguous".
        If multiple candidates have nonzero similarity scores, but one unique
        candidate has the highest score, there is a "minor ambiguity".
        In either case, the candidate with the highest score is crowned the winner
        and returned.

        If multiple candidates each equally score the highest similarity, there's
        a tie, also known as a "severe ambiguity". The fuzzy algorithm is unable
        to resolve severe ambiguities, so an error is raised.

        If no candidates score any similarity points, no match was found.
        If `phrase` has a non-zero similarity to any poisoned search term, we
        assume a false negative has occurred and return an error.
        Otherwise, return `None` as the matching candidate.

        Example:
            phrase = "black cherry"
            similarities = {
                "berry":     {'acai berry': 0,  'blueberry': 0,    'cranberry': 0},
                "fruit":     {'apple': 0,       'banana': 0,       'cherry': 6},
                "vegetable": {'artichoke': 0,   'broccoli': 0,     'carrot': 0},
            }
            match = "fruit"     # 'cherry' was the most similar search term.

        WIP: Some day, we could use a slightly more refined definition of similarity
            between a phrase and a search term: the length of the longest common
            substring shared between `phrase` and that search term.

        If we were to use this definition, we'd get slightly different numbers:

        Example:
            phrase = "black cherry"
            similarities = {
                "berry":     {'acai berry': 4,  'blueberry': 4,    'cranberry': 4},
                "fruit":     {'apple': 1,       'banana': 1,       'cherry': 6},
                "vegetable": {'artichoke': 2,   'broccoli': 1,     'carrot': 2},
            }
            match = "fruit"     # 'cherry' was the most similar search term.

    NOTE: If this function does not raise an error, it will always return
        either `None`, or a candidate from `spec.fuzzy_search_terms.keys()`.
    """

    def get_search_term_similarity(search_term: str, haystack: str) -> int:
        """ Return the similarity score for a single search term against a given haystack. """
        return len(search_term) if search_term.lower() in haystack.lower() else 0

    def get_candidate_similarity(candidate: str, spec: const.SurveySpecification, haystack: str) -> int:
        """ Return the highest score achieved by any of the candidate's search terms. """
        # The key itself is a search term if no others are provided (shorthand to save typing)
        search_terms = spec.fuzzy_search_terms.get(candidate) or [candidate]
        return max(get_search_term_similarity(term, haystack) for term in search_terms)

    candidates = spec.fuzzy_search_terms.candidates()
    scores = {candidate: get_candidate_similarity(candidate, spec, phrase) for candidate in candidates}
    max_score = max(scores.values())

    # Compute candidates for debugging, and to filter out entries with score 0.
    # This prevents all search terms from having a tie at 0 points.
    candidates = {key: score for key, score in scores.items() if score > 0}
    if len(candidates) > 1:
        logger.debug('Minor fuzzy_match_phrase ambiguity: "%s" could be any of: %s', phrase, candidates)

    winners = [key for key, score in candidates.items() if score == max_score]
    if len(winners) > 1:
        raise RuntimeError(f'Severe fuzzy_match_phrase ambiguity! "{phrase}" could be any of: {winners}')

    # If nothing won, check the poisoned search terms to see if we should abort.
    if not winners and spec.poisoned_search_terms and any(f in phrase for f in spec.poisoned_search_terms):
        raise RuntimeError(
            f'fuzzy_match_phrase triggered fail-safe!\n'
            f'   Phrase:                  {phrase!r}\n'
            f'   Poisoned Search Terms:   {spec.poisoned_search_terms}\n'
            f'   Candidates:              {spec.fuzzy_search_terms.candidates()}\n'
        )

    winner = winners[0] if winners else None
    logger.debug('fuzzy_match_phrase mapped %s --> %s', repr(phrase), repr(winner))

    # We expect this to return None for "None of the above", or similar,
    # but usually returning None is a sign that something has gone wrong.
    if winner is None and "None" not in phrase:
        logger.warning('fuzzy_match_phrase returned None for: %s', phrase)
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
        if spec.value_type == ValueType.PLACEHOLDER:
            # JsonKey is an enum, so we need to extract the str value
            key = spec.json_key.value
            return {key: ValueType.PLACEHOLDER} # to be overwritten later.

        handlers = {
            Mappings.ONE_TO_ONE:   self.process_one_to_one_mapping,
            Mappings.SPLIT:        self.process_one_to_many_mapping,
            Mappings.MERGE:        self.process_many_to_one_mapping,
        }
        return handlers[spec.mapping](row, spec)


    def process_one_to_one_mapping(self, row: List[str], spec: const.SurveySpecification) -> Datapoint:
        """ Process a one-to-one mapping in which a single column in the CSV maps
            to a single JSON key. Return the datapoints to be added to self. """
        assert_type(spec.json_key, JsonKey)
        assert_type(spec.index, int)

        # JsonKey is an enum, so we need to extract the str value.
        key = spec.json_key.value

        # Get the single field from the CSV
        value = row[spec.index].strip()

        if spec.value_type == ValueType.NUM:
            value = int(value)

        elif spec.value_type == ValueType.STRING:
            # If there's a fuzzy_search_terms, we need to do more advanced processing
            # Otherwise it's good as-is.
            if spec.fuzzy_search_terms:
                value = fuzzy_match_phrase(value, spec)

        elif spec.value_type == ValueType.LIST:
            # If there's a fuzzy_search_terms, parse each item individually
            if spec.fuzzy_search_terms and spec.fuzzy_search_terms != const.PHONEMES:
                selected_items = value.split(const.INNER_DELIMITER)
                value = [fuzzy_match_phrase(item, spec) for item in selected_items]

                # Remove falsy entries from the list, such as "None of the above"
                value = list(filter(None, value))

            # If fuzzy_search_terms is absent or equal to const.PHONEMES, assume it's a phoneme list.
            else:
                value = get_glyph_list(value)

        else:
            raise NotImplementedError(f'this function cannot yet handle {spec.value_type=}')

        return {key: value}


    def process_many_to_one_mapping(self, row: List[str], spec: const.SurveySpecification) -> Datapoint:
        """ Process a many-to-one mapping in which multiple columns in the CSV are
            merged into a single JSON key. Return the datapoints to be added to self. """
        assert_type(spec.json_key, JsonKey)
        assert_type(spec.index, Sequence)

        # JsonKey is an enum, so we need to get the str value
        key = spec.json_key.value

        # Currently this method is only used to either:
        #   A) combine multiple phoneme lists into a larger phoneme list
        #   B) combine multiple single fields into a list of fields (e.g. word formation frequencies)
        if spec.value_type == ValueType.LIST:

            # If an existing list exists, append to it. Otherwise start a new one.
            # NOTE: AFAIK There should never be an existing one, but let's handle it anyway.
            ret = {key: self.get(key, [])}
            if ret[key]:
                logger.debug('many_to_one (%s) found existing entry: %s', key, ret[key])
                # I'm pretty sure there'd never be a case where this can happen, and I want to remove
                # the logic for it, so I'm adding this exception here so I notice if it ever does.
                # It's not *bad* if this exception comes up, it should be fine, but I'm just surprised.
                # If it raises, figure out why and replace the error with an explanatory comment.
                raise NotImplementedError("I assumed this case would be impossible. Figure out why it's not and remove this error.")

            # Case A: Combining phoneme lists
            if spec.fuzzy_search_terms == const.PHONEMES:
                for index in spec.index:
                    selected_items = row[index]
                    ret[key] += get_glyph_list(selected_items, phonemes.GLYPHS)

            # Case B: Combining multiple single fields
            else:
                # Fuzzy match each index, and merge results
                for index in spec.index:
                    # NOTE: For now, I'm assuming that each `value` is a single selected string,
                    #   not a list of selections. It should be easy enough to support multiple selections
                    #   later if we want; see the ONE_TO_ONE case for LISTs.
                    value = row[index].strip()
                    selected_item = fuzzy_match_phrase(value, spec)
                    ret[key].append(selected_item)

        # I haven't needed to implement this case yet.
        else: # spec.value_type != ValueType.LIST
            raise NotImplementedError(f'this function cannot yet handle {spec.value_type=}')

        return ret


    def process_one_to_many_mapping(self, row: List[str], spec: const.SurveySpecification) -> Datapoint:
        """ Process a one-to-many mapping in which a single column in the CSV is split
        across multiple JSON keys. Return the datapoints to be added to self.

        One-to-many mappings are currently only implemented for BOOL types.

        For one-to-many BOOL mappings, there are two modes of operation:

        1. Simple Mode:
            In simple mode, `spec.json_key` must be a list of JsonKey objects,
            and `spec.fuzzy_search_terms` must be `None`.

            In this mode, we will check each key to see whether that key appears
            in the text of any of the selected items in this entry on this row.

            If so, a value of `True` will be stored for that key; otherwise `False`.

        2. Advanced Mode:
            In advanced mode, `spec.fuzzy_search_terms` must be a `FuzzySearchTerm`,
            and `spec.json_key` must be `None`.

            In this mode, we will check each candidate key of `fuzzy_search_terms`
            to see if any of the selected items in this entry on this row fuzzily
            match that candidate key, according to `fuzzy_match_phrase`.

            If so, a value of `True` will be stored for that key; otherwise `False`.
        """
        assert_type(spec.index, int)

        if spec.json_key is None and spec.fuzzy_search_terms is None:
            raise TypeError('process_one_to_many_mapping requires a json_key or fuzzy_search_terms')

        if spec.json_key is not None and spec.fuzzy_search_terms is not None:
            raise TypeError('process_one_to_many_mapping cannot accept both a json_key and fuzzy_search_terms')

        # Currently this method is only used to pull each of a list of checkboxes into their own bools.
        selected_items = row[spec.index].strip().split(const.INNER_DELIMITER)

        if spec.value_type == ValueType.BOOL:
            if spec.fuzzy_search_terms is None:
                assert_type(spec.json_key, Sequence)
                # JsonKey is an enum, so we need to pull out the str values
                keys = [json_key.value for json_key in spec.json_key]

                # In simple mode, we just need to set a key's value to True if that key appears
                # in the text of any selected item. This is quick and dirty but often works.
                # e.g. "tone" appears in ['The language has tone ...', 'The language has complex consonants']
                ret = {key: any(key in text for text in selected_items)
                            for key in keys}
            else:
                assert_type(spec.fuzzy_search_terms, FuzzySearchTerms)
                keys = list(spec.fuzzy_search_terms.candidates())
                # In advanced mode, we do something similar, but use `fuzzy_match_phrase`
                # to determine which candidate keys appear in the selected items.
                def is_key_in_selected_items(key: str) -> bool:
                    for text in selected_items:
                        match = fuzzy_match_phrase(text, spec)
                        if key == match:
                            return True

                        # HACK: Special case: Allow backwards compatibility for stress before F22.
                        # Before F22, all "stress" was "predictable stress". D.PHONETIC has entries
                        # for both "stress" and "predictable stress", the latter is always a better
                        # match since it's a longer search term.
                        # Thus, when `key` is "stress", the match will be "predictable stress",
                        # which we'd still like to count as a kind of "stress". In F22 and later,
                        # the same goes for "unpredictable stress".
                        # A more general solution would be great, but lots of work for little gain.
                        if key == const.K.STRESS.value:
                            equivalents = (
                                const.K.PREDICTABLE_STRESS.value,
                                const.K.UNPREDICTABLE_STRESS.value
                            )
                            if match in equivalents:
                                return True
                    return False

                ret = {key: is_key_in_selected_items(key) for key in keys}
        else:
            raise NotImplementedError(f'this function cannot yet handle {spec.value_type=}')

        return ret


    @classmethod
    def from_csv_row(cls: 'LanguageData', row: List[str],
                     survey_specs: List[const.SurveySpecification]) -> 'LanguageData':
        """ Process the data from a single CSV row into a standardized format
            by feeding each item into the format specification for this semester.
        """
        logger.info('----- Parsing %s with netid %s -----',
                    row[const.LANGUAGE], row[const.NETID])

        data: 'LanguageData' = cls()

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
        # NOTE: Convert all enums to strs
        consonants_key = JsonKey.CONSONANTS.value
        if consonants_key in data:
            consonant_glyphs = data[consonants_key]
            data[JsonKey.NUM_CONSONANT_MANNERS.value] = phonemes.consonants.getNumMannersFromGlyphs(consonant_glyphs)
            data[JsonKey.NUM_CONSONANT_PLACES.value] = phonemes.consonants.getNumPlacesFromGlyphs(consonant_glyphs)

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
        language_key = JsonKey.LANGUAGE.value
        name_key = JsonKey.NAME.value
        netid_key = JsonKey.NETID.value
        self.languages.sort(key=operator.itemgetter(language_key, name_key, netid_key))


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

        # The dict is keyed by Semesters enum, but `_semester` is a str; convert it.
        _semester = Semesters(_semester)

        # If we haven't defined a format spec for this semester we won't know
        # how to process any of its data. Don't even attempt to continue.
        if _semester not in const.PARAMS:
            raise KeyError(f'Could not find format specification for {semester} in const.PARAMS')

        logger.info('Using SurveySpecification: %s', _semester)
        survey_specs = const.PARAMS[_semester]

        # Merge in grammar data first, followed by typology data.
        # It's not guaranteed we'll have both for each language.
        for i, survey in enumerate(Surveys):
            path = get_path(semester, survey.value)
            if not path.exists():
                logger.warning('%s semester: no anon CSV found for %s survey. Continuing without it...',
                               semester, survey.value)
                continue

            with open(path, 'r', newline='', encoding='utf-8') as f:
                rows = list(csv.reader(f))

            # Skip first row as it's just a header.
            languages = [LanguageData.from_csv_row(row, survey_specs[survey]) for row in rows[1:]]

            for language_data in languages:
                # Merge data from this survey into any other data we
                # may have for the same language from other surveys.
                try:
                    netid_key = JsonKey.NETID.value
                    netid = language_data[netid_key]
                except KeyError:
                    raise KeyError('language_data had no netid field: %s' % language_data)

                # It's weird if a netid submitted data for the second survey but not the first.
                # It may end up being perfectly fine (e.g. a student joins the class late), but
                # just in case, log a warning.
                if i > 0 and netid not in netid_to_language_data:
                    language_key = JsonKey.LANGUAGE.value
                    language = language_data[language_key]
                    logger.warning('netid %s (lang: %s) did not submit data for earlier survey', netid, language)

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
    for survey in Surveys.names():
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
    semesters: List[str] = args.semesters or Datasets.names()

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
