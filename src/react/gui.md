# GUI

This readme spells out how the GUI will need to look,
and how it is meant to interface with the API server.

There are a few "big" UI components we'll need


## QueryBuilder

Build a single Query, either by:

1. filling out a QueryTemplate
    (contains ${COMPARE} ${K} of ${CONSONANTS})
2. building an arbitrary Query from the available Query Tokens recognized by the API.

Collapsible.

When collapsed, show just the concise header:
"Contains at least 3 of p, t, k"

When expanded, shows the "full" form, like the IPA consonant picker.

Has a (-) icon on the right that allows you to remove this query from the builder.
Maybe give a way to "deactivate" the query without deleting it entirely?
This way students don't have to re-fill the entire thing every time.

If inactive, grey out the query.

Should it "remember" the state of the last query of this type?
e.g. if I spent five minutes picking all the consonants I wanted, and then accidentally delete it,
should those same consonants be selected when I re-add a new one?


### IPAConsonantPicker

Pick an IPA consonant from the full chart

### IPAVowelPicker

Pick an IPA vowel from the full chart

### StringPicker

Pick a string from a list (optionally mapping the "display" string to an internal "value" string.).

Some will support multi-select, some will not.

### ComparePicker

Special case of StringPicker, for "at least", "at most", ... mapping to "Geq", "Leq", ...

Don't forget a special "all".

Might want to combine ComparePicker with NumberPicker to create a single element.
Afaik NumberPicker never exists anywhere in isolation without a ComparePicker next to it.

### NumberPicker

Pick an integer.

## EndangermentPicker

Special case of StringPicker, arranged horizontally.
May need some way to pick "between X and Y", and a second mode to pick
arbitrary elements.
e.g. start with a begin/end slider, and have a toggle to get rid of the slider
and make it a multiselect list instead.

# SyllablePicker

Similar to EndangermentPicker

Should have a mode for "between X and Y", and a second mode to pick arbitrary elements.
TODO: Make Syllable an OrderedStr like EndangermentLevel.

# NaturalClassPicker

Not quite sure about this.
Similar to a StringPicker, but with multiple columns, and clickable column headings.

# StringEntry

Enter arbitary strings, like for country of origin, language family, ...

# BetweenPicker

Between ints, OrderedStrs, ...

Allow for either endpoint queries (e.g. lo < x < hi)
or arbitrary list contains (e.g. x in (3, 5, 6, 7, 8))

# StringEntryIn

Enter a whole list of arbitrary strings, compare against all of them.


## QueryViewer

View all Query objects currently in the queue.

Contains all the other queries in a list

Includes a button to remove an existing query (or maybe this is attached to the QueryBuilder itself)

Includes a button to add a new Query to the list.


## GraphBuilder

Build a single graph query, which will render a graph when executed.

## QueryResults

Display the results of all active queries.

If there is one query, A, we should display:
- x/N languages satisfy A
  - List them all, plus contexts

If there are two queries A, B, we should display:
- A || B
- A && B
- A -> B
- B -> A

If there are three queries A, B, C, we should display:
- A || B || C
- A && B && C
- Among languages that had A,
  - x had B
  - x had C
- Among languages that had B,
  - x had A
  - x had C
- Among languages that had C,
  - x had A
  - x had B
- Is this too much?

continue like this for up to ~5 queries?

Should be able to display a custom message for "these languages don't have the requested data"
e.g. if you query the DB halfway through the year, queries from the second half of the year
shouldn't choke horribly.


Display a little color-coded percentage or a light-saber graph to visually show at a glance
what percentage of languages matched.

If possible, line up the languages from each category in a table, e.g.

5 Languages have stress  |  3 Languages have at least 1 of p,t,k

Breton                              Breton   p, t
Choctaw
Hamar
Jingulu                             Jingulu  p, t, k
Patwin
                                    Sarazi   p

Note that if a language appears in one column, it's at the same height in every column.

What if instead, I just list all the languages once, and have check boxes for "has stress"
or "consonants":

Breton    ✔    p, t
Choctaw   ✔    -
Hamar     ✔    -
Jingulu   ✔    p, t, k
Patwin    ✖    -
Sarazi    ✖    p

Will this make it harder for students to answer questions like:
"Which languages have at least 1 of p, t, k?", since now they have to scan across the list?

Maybe provide a toggle to switch between the views.

## Other stuff

- Should be some way to copy-paste the GET /languages request to import / export
- Should be some way to encode the query in the URL so you can link others to your results.
- e.g. if you link to /lingdb?Query&HasStress it will show you a single query for languages that have stress
  - stretch goal: add a shorthand for succinct urls that are shorter than just listing all params.
    - shouldn't be too bad; could do something like pick a single char for each query type,
      or convert them to a numeric value and b64 encode it.
- Add some way to store current set of queries in local storage so they survive a page reload.
  - Note that if we update the URL to match the list of queries, we get this for free
- Should be able to select the dataset being queried.
- Need some sort of res


- Should we remove submit button and show results in real time?
    - Or maybe start each new Query as disabled, and enabling it automatically submits the queries?
    - Similar effect for less server load when users are just inputting intermediate values.

- Some sort of venn diagram view?
    - Sort langs into "Only A, Only B, Only C", A & B, B & C, A & C, A & B & C


- Advanced mode toggle
  - Show/hide the "custom query" option.
  - For each query, add buttons allowing user to copy-paste:
    - The GET request
    - The JS API command.
    -
- Dark mode toggle
-