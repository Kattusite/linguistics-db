# linguistics-db

Canonical lists of consonant and vowel phonemes are located in app/phonemes/

Language class is defined in app/lingdb/language.py

app/data is capable of converting CSV to JSON but the code is a mess at the moment


To-Do
========
* Add Headings to the results pane (and generally reorganize - perhaps split into a query tab on the left and a results tab on the right. ) -- Headings for "implicational", "logical", "list"
* BUG: Clicking ".. languages matched .." now RESUBMITS the post request, even if the query terms have changed, so it replaces the entire pane with possibly new (undesired) results.
Instead I should make it so that the language lists are always generated and sent, but they are hidden until the ".. languages matched .." button is clicked. The "Toggle List Mode" button can probably be eliminated entirely.
* Add more info to the replies (Have the server help generate them dynamically) -- FOr instance,
Most languages (28 / 34) contain at least 1 of unrounded high central vowels -->
Most languages (28 / 34) contain at least 1 of unrounded high central vowels (like [a, e, i, o, u])
* Fix the response-generation function to work for edge cases. For example, instead of "Few languages contain at least one of a" could just say "Few languages contain a". Or instead of "Few languages contain at most 0 of p" --> "Few languages do not contain p"/"Few languages contain none of x, y, z"; "languages contain at least/exactly 3 of p,t,k" --> languages contain all of p, t, k
* Add more trait selections such as:
1. number of consonants/vowels/phonemes
2. word order
3. morphological types
4. word formation (and freq)
* Prevent users from sending invalid requests (querying for consonants when none are selected, invalid # for k value) and notify the user of the failed attempt
* Don't let users highlight the text in phoneme/class selector popovers.
* Allow arbitrarily many traits to be selected. (but for usability artificially limit to 3-5 for now)
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
