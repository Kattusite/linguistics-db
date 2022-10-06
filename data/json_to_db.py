"""Given a standard JSON file, organized as an array of JSON objects, write out
another JSON file representing the same data, but in TinyDB format.

(This format is also a JSON file, but it has special headers and structure)

Files of this form are given the .db extension

Usage:
$ python data/json_to_db.py <dataset>

"""
import argparse
import json
from typing import (
    List,
)

from tinydb import TinyDB

from data import datasets
from data.const import Datasets

def convert(semester: str):
    """The first command line argument should be the name of the dataset to
    convert (e.g. S19, F17). The name of the input JSON file and output db file
    will be constructed in a systematic way from the dataset name"""

    inPath = datasets.datasetFilename(semester)
    outPath = datasets.databaseFilename(semester)

    with open(inPath, "r", encoding="utf-8") as inFile:
        data = json.load(inFile)

    db = TinyDB(outPath, encoding="utf-8")
    # Delete existing records
    db.purge()
    for d in data:
        db.insert(d)

def main():
    """If command line args are provided, treat them as dataset names and convert
    all these datasets from their raw JSON format to TinyDB-formatted JSON.
    Outpu a file /data/datasets/<datasetName>/<datasetName>.json for each one.
    By default, if no command line args are provided, convert all known datasets
    in the same way as described above"""

    # If arguments are provided, treat them as dataset names and parse those files only.
    # Note: dataset names are like (F17, S19), without a file extension
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='increase output verbosity')
    parser.add_argument('semesters', nargs='*',
                        help="which semesters' datasets to be converted")
    args = parser.parse_args()

    # If no semesters requested, process all known semesters.
    # HMM?: For some reason we don't skip test semesters here...
    semesters: List[str] = args.semesters or Datasets.names()

    # Convert each file CSV -> JSON and write it to disk.
    for semester in semesters:
        convert(semester)

if __name__ == '__main__':
    main()
