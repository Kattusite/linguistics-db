# transformations

I'd like to make a list of all the different types of Queries a user might
want to make about a language.

I want the list to be as close to exhaustive as possible.

The hope is that then I can abstract out some common patterns I can use to
design UI elements and a backend encoding for the transformation chain.

## The List

- x ContainedIn Collection
    - has an endangerment level in [1,2,3]
    - has a headedness of one of [mixed, head-initial, head-final]
    - a special case of the below:
        x Intersection(Collection) Geq 1
- x Intersection(Collection) Compare Int
    - has >= 3 of [p,t,k]
    - has == 2 of [a,e,i]
    - has < 3 of [breathy, voiceless] vowels
    - has == 2 of [palatalized, clicks]
    - has >= 1 of [CV, CCV, CCCV]
    - has >= 1 of [analytic, agglutinating]
    - has >= 1 of [compounding, suffixation, suppletion]
    - has >= 1 of [tense, mood, case]
    - has >= 1 of [SVO, OVS, free]
- x Filter(Predicate) Compare Int
    - has >= 3 vocalic
    - has == 1 mid vowel
    - has < 4 nasals
    - similar to above, but the list is not explicitly defined
    - instead it's just a property that must be true of members
- x Compare Int
    - has >= 3 places of consonant articulation
- x Compare GetInt Str
    - has == 10 vowels
    - has <= 4 consonants
    - similar to above, but the choice of which Int to compare against is
        determined by a Str argument.
- x (Bool)
    - has complex consonants
- x (Bool) GetBool Str
    - has predictable stress
    - has some stress
    - similar to above, but the choice of which Bool to check is determined
        by a Str argument
- x Equals Str
    - affixation freq is exclusively suffixing
    - word formation freq is mostly affixal
    - similar to above, but the "Bool" is comparing a single value against
        a Str provided as argument.


## Others

Those are the currently supported queries.
What about new ones I'd have _liked_ to add?

- x Equals Str
    - but with arbitrary text input
    - country = ...
    - language family =
    - also add x Compare Str
        - x Equals
        - x NotEquals
        - x HasSubstring    $ Str in x
        - x IsSubstring     # x in Str
- x ContainedIn Collection
    - but wth arbitrary text input
    - country in USA, China, Russia,
- x SubstringContainedIn Collection
    - with arbitrary text input
    - any(x in item for item in Collection)
    - e.g. "United States" is substring of something contained in ["What is now the United States"]
- x IgnoreCase
    - e.g. for ContainedIn
    - casefold everything (or just .lower() it?)
- x Between Int,Int
    - number of consonants in [3,5]
    - excludes endpoints
- x InRange Int,Int
    - includes endpoints

How about Compare / InRange for endangerment levels?
- x InRange EndangermentLevel,EndangermentLevel
    - endangerment level in [4, 6b]
    - need to create some custom type / mixin for comparable, maybe?
    - Could just subclass str and then define a:
        - x InRange Str,Str

# Graphs

We might want to filter our dataset a bit first, and then extract an arbitrary data field.

For example,
    - Among languages with less than 5 vowels, how many places of consonant articulation are there?

Or we might want to graph a numerical property across the unfiltered dataset:
    - How many consonants does each language have?

Or we might want to place languages into discrete categories and count how many fall into each:
    - How many languages have each endangerment level?