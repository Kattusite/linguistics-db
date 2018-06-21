# TODO rename to avoid name collision

from . import const
import phonemes
import json

jsonFile = open("data/anon-combined.json", "r")
language_data = json.load(jsonFile)
