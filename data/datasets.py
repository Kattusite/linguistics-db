"""Define the different possible datasets that we can query, and some common operations
for datasets"""

import json
from . import const

# See data/const.py for relevant constants (e.g. dataset names)
DATASET_PATH = const.DATASET_PATH
datasetNames = const.datasetNames

# The datasets themselves, uninitialized until needed
datasets = None

def initDatasets():
    """Intialize the datasets when they are needed"""
    global datasets

    # Read datasets from json filess
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
