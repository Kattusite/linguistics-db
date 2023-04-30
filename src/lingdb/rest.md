# What will the REST API look like?

- /languages
    - Main endpoint for language queries
    - Name?
        - /query
        - /languages
        - ...
        - The response of the request will be a list of languages, so that seems right.
    - Should support multiple queries in one request
    - POST or GET?
        - If we need a request body, we should use POST:
            https://stackoverflow.com/questions/978061/http-get-with-request-body
        - But POST kinda suggests to me we're trying to change something serverside.
        - GET feels more natural since it's a read-only operation.
        - GET is easier for students to create their own queries
            - just modify the params: /languages?foo=bar&baz=bal
            - whereas POST would require at least some knowledge of curl, fetch, ...
                (or a JS wrapper around one of those things)

        - I prefer GET, if it's possible to shove everything into the request params.

    - Let's imagine how a GET /query might look:
        - We need to include:
            - A query (by name?)
                - Ideally we wouldn't hardcode names, to make it easier for
                    students to make custom queries not implemented by default.
            - Any arguments needed for that query
            - A way to pass additional queries

        - On the backend side, a Query is just a chain of Transformations.
        - Can we represent it the same way on the frontend side?

        - Let's represent it in a normal data structure first, then figure out
            how to URL-encode it

            // contain at least 3 of p, b, t, d, k, g
            queries = [
                [
                    {'Get': ['Consonants']},
                    {'Intersection': ['p', 't', 'k', 'b', 'd', 'g']},
                    {'ExtractContext': []}, // no args, [] or null
                    {'Geq': [3]},
                    {'FilterLanguages': []},
                    {'Get': ['Name']},
                ],
                [
                    ... second query ...
                ]
            ]

            response = [
                {
                    results: ['Goemai', ...]
                    context: [['p', 't', 'k'], ...]
                },
                {
                    ... second query ...
                }
            ]

        - Okay, that seems like a great way to encode a query.
            Admittedly, seems like a POST body would be less ugly.
            But let's give it a shot as a GET request.
            If it sucks, we can use POST.

        - Option 1) Stupid but it works (and therefore it's not stupid):

            JSON encode, then URL encode the whole thing:

                query_params = urllib.parse.quote_plus(json.dumps(query))
                GET /languages?query={query_params}

            Serverside, we'd URL decode, then JSON decode:

                query = json.loads(urllib.parse.unquote_plus(request.params))

                We might be deserializing untrusted JSON, so do be careful.

        - Option 2) Cleverer?
            - We can encode a list by passing the same param multiple times.
            - We can encode a dict by passing key=value
            - But we need to encode a List[List[Dict[str, List]]]
                - Jesus Christ

            - Let's drop the outer List for a sec and pretend we're only allowed
                a single query per GET.

            GET /languages?
                Get=Consonants&
                Intersection=p+t+k+b+d+g&
                ExtractContext=&
                Geq=3&
                FilterLanguages=&
                Get=Name&

            Uhhh wow, that actually looks pretty good.
            Way easier for a student to hack on than the json encoded thing!

            - This urllib expression may be handy for parsing:
                urllib.parse.parse_qsl('foo=bar&baz=&bal&foo=a+b+c', keep_blank_values=True)
                - qsl -- return as a list of tuples instead of a dict (to keep separate queries separate)
                - keep_blank_values -- don't drop singletons like ExtractContext=&
                - Since we used + to separate lists within an argument list, we need to split on spaces
                    in the result (eg 'p+t+k' -> parse_qsl -> 'p t k' -> split() -> ['p', 't', 'k'])

            But what about multiple queries?

            Well, that's not too bad, actually.
            Just add a special token to signify the start of a new query:

            GET /languages?
                Query=&  // if you want you can give a name or something
                Get=Consonants&
                Intersection=p+t+k+b+d+g&
                ExtractContext=&
                Geq=3&
                FilterLanguages=&
                Get=Name&
                Query=&
                ... second query follows ...

            Wowow, that is pretty decent, actually. Let's do that one.

            Let's also add a:
                ?dataset=F22

            Note that all the arguments will be strings, so we need a way to convert each value
            from a str to the appropriate type.
                '' -> [] or None
                'false' -> False
                'true' -> True
                try: int(value) -> int
                try: float(value) -> float  // do we even allow floats? .-.

                But what about lists? Those are tricky! We need some sort of delimiter.
                But what about lists of length 1? By definition those have no delimiter!!

                I think we'll have to parse the key first, look up the associated Transformation,
                figure out that transformation's required argument type, and then convert from str
                to that type.

                e.g. Intersection=p+t+k+b+d+g -> ('Intersection', 'p t k b d g')
                Transformation.get('Intersection').get_argument_type() -> Collection
                try: value.split(list_delimiter)

                But what about Transformations that accept multiple argument types?!
                e.g. I was considering making Geq apply to both Int (where it's a literal Geq)
                    or to Collection (where there's an implied Length first),
                    or maybe even to String (where we'd do something lexicographic)

                I might have to say that the implied Length is disallowed, and force users
                to explicitly state Length if they want it to be included.

                But even if I do, this does nothing for Geq for strings...
                How would I distinguish between Geq=5 (an int) or (a str endangerment level)?

                Could add a separate Geq-like command just for strings, and say Geq is Int only.

                This makes the problem go away, but I wonder if there's a better way?

                We could potentially infer the correct type based on the type of the previous step?
                e.g. if the current result is a list, we need to split str into list first.

                But that sounds really complex to implement, and the benefit is kinda marginal.

                I think we were OK with "force Transformations to be single-type only"

                    Collection Geq 3 -> Collection Length Geq 4  // more explicit anyway
                    Str Geq 4 -> Str EndangermentBetween 4 8  // we only need this for endangerment
                            // it's not an arbitrary string compare anyway.
                    Int Geq 5 -> Int Geq 5 // we can keep the int one as-is.

                How about instead of using + as a separator I just use ; ?
                That seems like it would never appear in a str input, so we can just
                take the presence of ; as evidence the argument is a list.

                That lets us keep our Geq overloading, too.



        Maybe worth taking a step back and asking if this entire strategy is wise.
        The query language seems _really_ expressive, since the client gets to
        request whatever code they like to run on the server
        (so long as the code corresponds to a valid transformation)

        Is that safe?
        If the set of valid transformations is locked down enough, probably?
        Then the client can basically just ensure that the server sends back
        arbitrary results (but in the correctly formatted way).
        That sounds relatively benign.

        Even so, should keep safety in mind when implementing this.
        Some limits on maximum sizes may be a good idea:
            - on number of queries per request
            - on number of transformations per query
            - on size of uri (may already exist)
