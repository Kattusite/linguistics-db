# linguistics-db

Canonical lists of consonant and vowel phonemes are located in app/phonemes/

Language class is defined in app/lingdb/language.py

app/data is capable of converting CSV to JSON but the code is a mess at the moment


To-Do
========
* How to represent variable-number-of-trait query payloads?

Will need to transmit:

[
  {
    "trait": "consonant",
    "bitstring": "01001001...0010",
    "quantity": "5",
    "mode": "GEQ"

  },
  {
    "trait": "consonant class",
    "class": "voiced"
    "quantity": "2",
    "mode": "EQ"

  },
  {
    "trait": "boolean",
    "name": "has-stress"

  }

]


* Merging grammar and typology csv's into a single csv, and creating a language object from it

* Investigate vis.js library (visjs.org) or D3.js (d3js.org)
