# TODO rename to avoid name collision (data is an extremely common name)

from . import const, datasets
import phonemes
import json

# data Functions
getDataset          = datasets.getDataset
getDatasetNames     = datasets.getDatasetNames
readDataset         = datasets.readDataset
