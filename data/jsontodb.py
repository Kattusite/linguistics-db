"""Given a standard JSON file, organized as an array of JSON objects, write out
another JSON file representing the same data, but in TinyDB format.

(This format is also a JSON file, but it has special headers and structure)

Files of this form are given the .db extension

Usage:
$ python data/jsontodb.py <dataset>

"""

from tinydb import TinyDB
from . import datasets

import json, sys

def convert(dataset):
    """The first command line argument should be the name of the dataset to
    convert (e.g. S19, F17). The name of the input JSON file and output db file
    will be constructed in a systematic way from the dataset name"""

    inPath = datasets.datasetFilename(dataset)
    outPath = datasets.databaseFilename(dataset)

    with open(inPath, "r", encoding="utf-8") as inFile:
        data = json.load(inFile)

        db = TinyDB(outPath, encoding="utf-8")
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
    if len(sys.argv) > 1:
        names = sys.argv[1:]
    # Otherwise, parse all known datasets
    else:
        names = datasets.datasetNames # from const

    # Convert each file CSV -> JSON and write it to disk.
    for name in names:
        convert(name)

if __name__ == '__main__':
    main()
