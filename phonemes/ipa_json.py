"""A collection of tools to help consonants.py and vowels.py read in their input
data from .json files"""

import json

def isEnabled(p):
    """Given a dict p representing the properties of a phoneme, return true
    if the phoneme either has no "disabled" field, or if it has "disabled": False"""
    if "disabled" not in p:
        return True
    if not p["disabled"]:
        return True
    return False

def readIPAFromJson(filename):
    """Read in IPA data from the specified json file, and return it as an array
    of dictionaries containing the properties of each phoneme"""
    file = open(filename, "r", encoding="utf-8")
    data = json.load(file)

    # Some phonemes might not be tracked in a given semester.
    # e.g. F19 didn't collect data for /a^f/.
    # Filter out any phonemes that might be disabled
    enabled = [p for p in data if isEnabled(p)]
    if len(data) != len(enabled):
        print("Excluding %d disabled phonemes from tables..." % (len(data) - len(enabled)))

    return enabled
