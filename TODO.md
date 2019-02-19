# linguistics-db

Pardon the mess! This is a work in progress...

Canonical lists of consonant and vowel phonemes are located in app/phonemes/

Language class is defined in app/lingdb/language.py

app/data is capable of converting CSV to JSON but the code is a mess at the moment


To-Do
========
* The MODE strings defined in selectors.py don't make any sense ... what
is it that they are actually supposed to be checking? all of the selectors are
PICK_K, but some are classed as PICK_MULTI instead? If I really meant to say
PBOX/LBOX/CLBOX/IPABOX, etc. then I should have just defined those instead.
* More metaclasses! (Especially place-based ones) -- see the cheat sheet
* More constants need to be shared btwn js/python. Specificially mode list (at least, all, none..) and some others I'll add as I remember
* Introduce more types to enforce properties of arguments. E.g. phonemes should be a type, queries should be a type
* Also I need to rewrite the pretty-string to make it shorter for large numbers of Consonants
e.g. (ptk -> unvoiced stops)
* also i need to add a button for voiced/unvoiced
* The front.js file has been itching for a rewrite for some time
* Add a proper navbar, meager as it may be (with an about / contact info page)
* Split the frequency selectors into two separate categories for smarter querying. i.e. allow queries for "languages that use exclusively a single strategy to form words" no matter the strategy, or queries for "languages that use prefixing to form words, regardless of exclusivity"
* BUG: There is currently no way to tell the difference between "No Data Available" and "Query matched available data, but no context / additional info is available" in the list display.
* BUG: For k-mode comparisons, results are not always accurate for < or <=. For example, 0 is always <= k, but languages with 0 matches are NOT returned as results (?). Actually investigate this further.
It seems as though 0 is in fact handled correctly, and this effect only happens for languages with missing data, making it a subset of the bug described immediately below.
* BUG: Creek & Kukama-Kukamaria	yield surprising (perhaps inaccurate) results. For example, "About half of languages (15 / 34) use at most 1 of affixation, prefixation to form words" even though these two languages use neither (They have missing data).
* BUG: Language lists are truncated / drop down awkwardly to the next line if they contain strings that are too long.
* The data is imperfect. (Pipil occurs twice, Creek & Kukama-Kukamaria lack typology)
* Change "Few languages have none agreement" -> "Few languages have no agreement"
* Standardize the names of functions in the Language.py class. contains should be
reserved for phonemes/natural classes. "has" should be for booleans? or perhaps "is"
* Move a lot of the functionality of handleSubmit from front.js to the python, so it can rely much more heavily on defined constants in data.const.py. For example, it would be dramatically easier if the client did not generate its own reply string, but instead let the server do so.
* Split front.js into two pieces. One that needs to be changed to add new traits and one that doesn't.
* Make it easier to add new questions. Currently the following must all be done: Add an item to the HTML dropdown. Add a corresponding template div. Initialize the popovers (if needed). Add a language.py function. Add a handler in routes/lingdbclient. Add functions to querySubmit / handleSubmit in front.js. front.js need new constants to support submitting queries.
* In the long term, I should try to reduce reliance on things like cbox/pbox classes... it is confusing to have so many HTML classes. Just rely on primitive ones like pbox/clbox/lbox, or if possible, a single class encapsulating all three. ("trait-box")
* Refactor front.js 2.0: In this same vein, introduce way more modularity + abstraction --> A function just for selecting/deselecting, a function just for generating the link text to be displayed, a function just for getting/setting the popover HTML from outerHTML.
* Refactor front.js so that the pbox/clbox/lbox handlers share significantly more code. The current form is unmaintinable. Side note: The HTML structure of pbox differs from the other clbox/lbox for no good reason... It is currently <tr><td><div></div></td></tr>, but clbox/lbox lack the innermost div as it serves no real purpose.
* Long term style goal: Go through all files and standardize debugging statements (possibly w debug logger). Standardize all return types, add type annotations, ensure that exceptions are raised in the appropriate places when
bad data is passed. (Possibly use asserts)
* Simplify the process of adding/parsing new questions.  In data.const, create
a master list of all "question" objects, where each object contains some useful data:
  - What type of question? (pick k phonemes, pick k from a list, pick 1 from a list, open response, enter a single value, etc. )
  - What is the name of the variable/value being obtained? (How should we refer to it in the JSON?)
  - If picking from a list, should we allow multiple selections to be chosen? This can be used in allgen.py to automatically create the list popovers.
  - If a parse-dict is necessary to read the question/answers from the data,
  provide the parse-dict.
Ideally we can iterate over all registered question objects, and auto-generate
the HTML for the selector boxes. We can also use this to simplify the parsing of the data.
* Condense my awful CSS structure into a more concise description -- e.g.
Use .pbox.label.active instead of .pbox-label.pbox-label-active  -- Many of my CSS classes should overlap but I end up copy-pasting them instead
* Add Headings to the results pane (and generally reorganize - perhaps split into a query tab on the left and a results tab on the right. ) -- Headings for "implicational", "logical", "list"
Also add prefix-type headings to each result so it is immediately obvious which each does-- for instance (AND), (OR), (A->B), (B->A)
* Add more info to the replies (Have the server help generate them dynamically) -- FOr instance,
Most languages (28 / 34) contain at least 1 of unrounded high central vowels -->
Most languages (28 / 34) contain at least 1 of unrounded high central vowels (like [a, e, i, o, u])
* Fix the response-generation function to work for edge cases. For example, instead of "Few languages contain at least one of a" could just say "Few languages contain a". Or instead of "Few languages contain at most 0 of p" --> "Few languages do not contain p"/"Few languages contain none of x, y, z"; "languages contain at least/exactly 3 of p,t,k" --> languages contain all of p, t, k; "Few languages contain less than one of [...]" --> Few languages do not contain any of [...]
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


* Acknowledgments: Inspired in part by www.ipachart.com
 Some phonetics data from https://commons.wikimedia.org/wiki/General_phonetics and https://www.internationalphoneticassociation.org/content/full-ipa-chart
