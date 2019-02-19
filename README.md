# linguistics-db

## User Info
Use of the website should hopefully be relatively intuitive and straightforward.
The website is based on linguistic data collected by students on several aspects of
a selected list of world languages, covering their phonology, grammar, and typology.

The goal of this web app is to allow users to query this data to find correlations
across languages and discover if there are any properties universal to all (or most)
languages.

To use the site, simply select a trait that you would like to query, such as
which consonants or vowels the language allows, and fill in the relevant parameters.

Possible parameters include:
1. An equality mode:
  * Such as "at least", "exactly", "less than", etc.
  * Specifies how to interpret the numerical parameter.
2. A number:
  * Must be a non-negative integer (0, 1, 2, ...)
  * Specifies how many of the selected properties must match.
3. A selection (or several selections):
  * Which properties (vowels, consonants, word orders, etc.) are of interest for this query.

Additionally, you may query two different traits at the same time, and the app
will try to identify possible correlations or implications between the two traits.
(Technically speaking, the app only reports co-occurences of different traits.
More sophisticated statistical tests would be needed to determine statistical implication.)


## Developer Info

The program is split into several core stages, which are described below. This is
meant to be more a broad overview of the core pieces of the project than a detailed
explanation of the intricacies of every file. (Hopefully) this is enough to orient
any future developers who might get stuck cleaning up after my code.

### Overview
The web app runs in the Flask framework. There is not currently a large enough
volume of data to warrant the overhead of a full database, so data is stored
as simple JSON files. The frontend uses Bootstrap 3, along with jQuery and
your standard vanilla CSS, HTML, and JavaScript. Requests are sent from the
client asynchronously (using XHR) as POST requests, and when the server generates
a reply, the page is updated to reflect the changes. The backend is all implemented
using standard Python 3.7.

### Parsing / Reformatting Data
The data is collected via (two separate) Google Forms, the results of which are
converted to CSV files, and then combined into a single JSON file, which has been
stripped of any personally identifying information that was present in the original
survey data.

The data, as well as the programs responsible for converting it, are stored in /data/.
The program to combine the two CSV files can be run using `python -m data`,
which will produce an output JSON. The relevant code itself resides in `csvtojson.py`.

The process of changing the data from CSV format to JSON format is fragile, as
it relies upon the specific wording of response options on the Google Form, which
may change from year to year.

Generally, the parsing process is handled using dictionaries called "parseDicts",
which are mappings from *desired meanings* (keys) to *possible representations of those meanings, as they appear in the survey* (values).

For example, if parsing a question on which syllable structures are allowed in a
language, let's say we would like to populate the JSON file with values of the form
`V`, `C onset`, `CC onset`, ..., `C coda`, ...; and that these values might be
represented in several equivalent, but non-identical, formats on the original survey:
`CCCV`, `onset of 3`, `3 consonant onset`, `CCC onset`, and so on...

Then, the associated parseDict for this survey question would be:
`syllable_dict = {
    "V":          ["V", "no onset or coda", "onset of 0", ...],
    "C onset":    ["CV", "onset of 1", "C onset", ...],
    ...
 }`


### Building
Due to the very repetitive nature of many of the elements of the web interface,
there are several (hacky but functional) python scripts dedicated to generating
large swatches of static HTML and styling all at the same time, before the user
loads the page. (There is some additional generation that happens in JS when the
user first loads the page, but it is far simpler).

I've found that this strategy works quite well, because it makes sweeping changes
to the overall design of the HTML much easier, requiring only a few changes to
constants, rather than manually changing 1000+ lines of HTML every time. In
hindsight, there was definitely an easier way, such as using Jinja templating to
accomplish the same thing, but this works for my purposes.

The automatic code generation resides in `/gen/`, primarily in `autogen.py`.
This code defines, among other things, the bodies of all of the popover elements,
and the trait selectors. It can be run with `python -m gen`, which will automatically
output all of the HTML, and then splice it into `/app/static/templates/front.html`,
based on the template defined in `/app/static/templates/front_template.html`.

This file also takes care of generating a javascript file containing useful python
constants used frequently serverside, to ensure that the client and server constants
are always in sync, in the event that one needs values defined by the other.

### Sending Queries (Frontend)
The logic for sending queries to the server is all handled clientside, in JavaScript.
The code is located in `/app/static/js/`.

Queries are validated before being sent to prevent malformed queries from reaching
the server, and arbitrarily many traits can be bundled together in a single query,
even though the frontend and UI only supports 2 traits at a time.

A query is represented as a dictionary (or object), with fields of:
* `payload`: a list of queries for specific traits.
  In particular, each entry in the list is itself a dictionary that contains (some of) the following fields:
  * `mode`: The equality mode to be used for comparing a query to a language.
  i.e. "at least", "at most", "less than", "more than", "exactly", "not equal to", "all"
  * `k`: The non-negative integer of items that must match for this query to be satisfied.
  * `selList`: The selected items to be queried for.
  * `sel`: A special case of selList, when selList has only a single item (selList.length == 1)
  * `reply`: A client-generated reply string to be included in the server's response.
  e.g. 34/34 languages **contain at least 4 of p, t, k, d, m**
* `listMode`: a boolean stating whether or not the list of matching languages should
be shown by default.

The complete query is then sent to the server via POST request. Once the server is
done generating a response, the server's response will be rendered on the page
using XHR (specifically via a callback passed to jQuery's $.post()).

### Processing Queries (Backend)
The execution path for requests sent to the server is (typically) as follows:
`/app/routes.py` ==> `/app/lingdb_client.py` ==> `/lingdb/__init__.py` ==> `/lingdb/language.py`.

`routes.py` is responsible for extracting the basic info from the request and passing
it along to `lingdb_client.py`, which processes each request in turn, aggregating the
results and creating an HTML response once they are complete. `/lingdb/` is where
all of the logic for matching requests against the data actually resides. The
`Language` class provides helpful methods for matching queries against single languages,
whereas `LingDB` generalizes these single-language methods to work for arbitrarily
large lists of languages.

### Modifying Selectors (Available Traits)
I've made an effort to rework the code so that adding or removing traits to query
for should be as painless as possible. *In theory*, all that must be modified
in order to add or remove a selector from the list of possible ones shown on
the website is `/data/selectors.py`, which defines the properties of all
the different selector types, and the information required to render them
and handle the query.

*In reality*, it is slightly trickier. If the selector you'd like to add is
very similar to an existing one, it might be as easy as adding a new entry
in `/data/selectors.py`, but if the new selector offers significantly
different functionality, you will likely need (at a minimum) a new
Language method to handle the query, and in the worst case you may have to
hand-roll a new type of popover, or a request with more parameters than just
the typical mode/k/selList trio.


## Acknowledgments

* IPA chart design inspired in part by www.ipachart.com
* Some phonetics data from:
  * https://commons.wikimedia.org/wiki/General_phonetics
  * https://www.internationalphoneticassociation.org/content/full-ipa-chart
