# Redesign plans

First, let's get some terminology out of the way.

LingDB is a collection of `Language` data.

Each `Language` has a variety of `properties`, which each consist of a `name`
and `value`.

For example, "Bardi" is the name of a `Language`.
This is one property of Bardi:
    `Property(name='endangerment level', value='6b')`
We could also represent the property as JSON:
    `{"endangerment level": "6b"}`

Each semester there is a new collection of `Language` data.
The precise set of properties, and structure (or schema) of those properties
may vary from one semester to the next.

For example, the "endangerment level" property may not have been collected one
semester, or its values might have been formatted differently -- say, as integers
instead of as strings.

## Queries

A `Query` is a request to gather some information about `Languages`.

There are two different flavors of `Query`.

### Filter Queries

A Filter Query maps an original set of `Languages` to a filtered subset of `Languages`,
by preserving only those `Languages` that satisfy some `Predicate`.

For example,
    S19 = the set of all `Languages` from S19.
    P = Language.num_consonants >= 15       # type: Predicate
    Filter(S19, P) = the set of all `Languages` from S19,
        that additionally have a `num_consonants` greater than or equal to 15.

### Extraction Queries

An Extraction Query pulls some `Properties` from a set of `Languages`.

For example,
    S19 = the set of all `Languages` from S19.
    X = Language.num_consonants             # type: ????
    Extract(S19, X) = the list of all `num_constants` properties from S19.

    I can't think of a good name for `????`.
    Here's some ideas:
        - Property
        - AbstractProperty
        - PropertyQuery
        - Extractor

        I like Extractor:
            A Filter operation uses a Predicate
            An Extract operation uses an Extractor

    What's a good format for the return value of Extract?
        - A simple list is no good; we need to know which Language that Property
          is associated with.
        - We could add a "Language" reference to each Property.
        - We could consider that "Languages" are actually kinda analagous to "Properties".
            - If we select some languages from a collection of languages,
              we get a new collection with some languages excluded.
            - If we select some properties from a collection of properties (i.e. a language)
              we get a new collection (i.e. Language) with some properties excluded.
        - The basic implementation that we have now would just be to return a mapping,
          from each matching language to the requested property of that language:
            {Language(A): Property(A), Language(B): Property(B), Language(C): Property(C)}
        - But will that scale? Do we want it to be possible to request multiple properties?
        - Like:
            Language.num_consonants().num_vowels()          ???
          Would this return:
            {Language(A): [Property(A1), Property(A2)], ...}
          If property is a dict, we could return:
            {Language(A): {
                PropertyName(A1): PropertyValue(A1),
                PropertyName(A2), PropertyValue(A2),
            }}
          How would multiple properties be displayed to users, though?

          S19 languages -> (num_consonants, num_vowels)

          Language   |   number of consonants   |   number of vowels
          ----------------------------------------------------------
          LanguageA  |           15             |          8
          LanguageB  |           22             |         11



## Query Flow

Standard queries from the website will consist of two stages:
the Filter Stage and Extract Stage.

In the Filter Stage, we find the set of languages that match the predicate.
In the Extract Stage, we find more info about the properties of the language
which caused it to match the predicate.

For example, if our Predicate is:
    Language.consonants.filter(['p', 't', 'k']).length >= 1

In the Filter Stage, we will find all languages which have at least 1 of p,t,k.
In the Extract Stage, we'll find which of 'p', 't', 'k' each language has.

// TODO. How does the extract stage know how to return the list of consonants,
//       and not the LENGTH of the list of consonants, since that was the last
//       thing in the predicate?

// Maybe we can rewrite the predicate?
//  Language.consonants.contains_k_of(['p','t','k'], 1)
//  Language.consonants.

// We need some way to interpret a predicate in two ways:
//  One way in the first "Filter" stage, to return a bool for each language.
//  And a second way in the "Extract" stage, to return some "useful" explanation.

// In principle, the predicate in the filter stage need not be related to the
// "extract" stage. We could say something like:
//      Find all languages where the number of vowels is greater than 10,
//      and return whether each one has stress.

// It'd be nice to support this as an "advanced" mode.
// But it'd also be nice to have a "basic" mode, where the user only needs to
// provide the "Filter" predicate, and the "Extractor" will be guessed intelligently.


## Python or JS?

I'm not sure yet whether I want to do everything natively in JS,
or make REST calls to a Python server.

I should probably write it to be agnostic, and I can wrap all the "REST" calls
in some interface that could in principle be backed by REST or a "fake" REST
server that's still in JavaScript.

## How to encode Predicates or Extractors?

Regardless of whether I use JS or Python, I'll want to have some way that I could
encode a Predicate in a way that it could be serialized into a REST request.

I need some sort of structured format that I can write these in, like a query language
or something.

The structured format might get really complex, especially if I allow arbitrary
chaining of predicates (e.g. P1 AND P2)

Either I can accept that (and try to have some weird deeply nested dict embedding
the structure of the predicate),

Or I can try to simplify predicates to something a little more manageable, like:

    // This is basically just me re-inventing the exact same format I use now,
    // which has some limitations.
    Predicate(
        property_name: consonants
        action: contains_k
        ...
    )

Or, I can accept that I will ONLY handle the filtering and extraction on the JS
side, and all of my problems about encoding predicates go away.

I could either just do EVERYTHING in JS (storing the JSON data directly in a JS file),
or I could expose a very simple Python REST interface that would just dump all the language
data for an entire semester, and then just do the FILTERING in JS.
(but literally at that point, why? the whole rest server could be replaced by a .js file copying the json)

Or I could expand the GET parameters to handle this a bit more gracefully, like:


GET /languages?semester=F19&num_consonants_eq=10&consonants_includes=p,t,k

// This would honestly work, but I'd need multiple parameters for each
// "predicate", like:\

    // num_consonants == 15
    num_consonants=15
    num_consonants_op=eq

    // num_consonants >= 15
    num_consonants=15
    num_consonants_op=geq

    // consonants.find([p,t,k]).length >= 1
    consonants_filter=p,t,k
    consonants_length=1
    consonants_op=geq

    // We can see this is getting a bit cumbersome, but it probably would work.

// Or I could try to encode that info some standard form:

    // consonants.find([p,t,k]).length >= 1
    consonants=">=1:p,t,k"      // html escape correctly

    // or in JSON:
    // once again, this is basically me re-inventing the "mode k" thing I already have.
    consonants = {
        values = [p,t,k]
        num = 1
        mode = "geq"
    }

// it'd also be nice if we could expose some more "advanced" comparisons in the JS console
// (or on the REST endpoint)
// so eg a student could pop open dev tools and do something like:

// Languages.semester(F22).find()


// The further I go, the more I'm convinced that the Python server is utterly useless
// It's a pain in the ass to host it and deploy it.
// It funnels queries over the network, which adds latency and introduces a single point of failure.
// It requires a a server
// It forces me to duplicate a lot of work (e.g. validating params, raising errors, etc. etc.)
// It forces me to serialize predicates, query parameters, etc. that are potentially annoying
// to serialize.
