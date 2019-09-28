"""Define the different possible datasets that we can query, and some common operations
for datasets.

Defines & initializes all of the TinyDB instances that the app will be using.

A note on terminology:
    A "dataset" is the json/dictionary representation of the data, whereas
    a "database" is the TinyDB instance this raw JSON data underlies.

A note on why databases/datasets are lazily generated:

In order to generate the .json and .db files for each dataset, we run
python -m data

This of course runs data's __init__.py, which must import this file.

However, `python -m data` must be able to generate the data the first time,
without datasets being defined or existing yet. It's impossible to initialize
the datasets and databases in advance because the data files underlying them
may not have been generated yet.

"""

import json
import tinydb
from . import const


# See data/const.py for relevant constants (e.g. dataset names)
DATASET_PATH = const.DATASET_PATH
datasetNames = const.datasetNames

# The datasets themselves, uninitialized until needed
datasets = None

# The TinyDB database instances for each dataset
databases = None

def datasetFilename(dataset):
    return DATASET_PATH.format(dataset, "%s.json" % dataset)

def databaseFilename(dataset):
    return DATASET_PATH.format(dataset, "%s.db" % dataset)

def initDatabases():
    """Initialize the databases for this application"""
    global databases

    # Do nothing if DBs already initialized
    if databases is not None:
        return

    databases = {
        dataset: tinydb.TinyDB(databaseFilename(dataset), encoding="utf-8") for dataset in datasetNames
    }

def getDatabase(name):
    """Return the database whose name is the one specified, if it exists"""
    # A bit of a hack: generate databases only the first time they are requested
    # See note at top of file
    if not databases:
        initDatabases()

    return databases[name]

def initDatasets():
    """Intialize the datasets when they are needed"""
    global datasets

    # Read datasets from json files
    datasets = { name: readDataset(name) for name in datasetNames }

def readDataset(name):
    """Reads the specified dataset from a file at /data/datasets/<name>/<name>.json"""

    jsonName = name + ".json"
    jsonFile = open(DATASET_PATH.format(name, jsonName), "r", encoding='utf-8')
    dataset = json.load(jsonFile)
    jsonFile.close()
    return dataset

def getDataset(name):
    """Return the dataset whose name is the one specified, if it exists"""
    # A bit of a hack: generate datasets only the first time they are requested
    # See note at top of file
    if not datasets:
        initDatasets()

    dataset = datasets[name]
    return datasets[name]

def getDatasetNames():
    """Return all known dataset names"""
    return datasetNames
