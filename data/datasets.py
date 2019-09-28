"""Define the different possible datasets that we can query, and some common operations
for datasets.

Defines & initializes all of the TinyDB instances that the app will be using.

A note on terminology:
    A "dataset" is the json/dictionary representation of the data, whereas
    a "database" is the TinyDB instance this raw JSON data underlies.

"""

import json
import tinydb
from . import const


# See data/const.py for relevant constants (e.g. dataset names)
DATASET_PATH = const.DATASET_PATH
datasetNames = const.datasetNames

# The datasets themselves, uninitialized until needed
datasets = None

def initDatabases():
    """Initialize the databases for this application"""
    global databases

    # Do nothing if DBs already initialized
    if databases is not None:
        return

    databases = {
        dataset: tinydb.TinyDB(DATASET_PATH.format(dataset, "%s.json" % dataset)) for dataset in datasetNames
    }

# The TinyDB database instances for each dataset
# TODO: Check if I need to defer the init() until absolutely needed like w/ datasets
databases = None
#initDatabases()


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
    return dataset

def getDataset(name):
    """Return the dataset whose name is the one specified, if it exists"""
    # A bit of a hack: generate datasets only the first time they are requested
    # This should avoid some weird circular dependencies with csvtojson
    if not datasets:
        initDatasets()

    dataset = datasets[name]
    return datasets[name]

def getDatasetNames():
    """Return all known dataset names"""
    return datasetNames
