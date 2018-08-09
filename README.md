# linguistics-db

Canonical lists of consonant and vowel phonemes are located in app/phonemes/

Language class is defined in app/lingdb/language.py

app/data is capable of converting CSV to JSON but the code is a mess at the moment


To-Do
========
* Reorder the default options in dropdowns to be more useful... People will be more likely to select "at least 1" than they are to select "exactly 1"
* Create a "related queries" div containing info about other things the user could have asked. For instance, if a user searches for A and B, inform them about what would have happened if they searched for just A or just B. If a user searches for Exactly 1 of x, y, z, inform them what would have happened if they searched for at least 1 (and so on)
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
