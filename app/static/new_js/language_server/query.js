/** query.js
 *
 * Provide a mechanism to execute queries against the underlying language data.
 *
 */
ALL_LANGUAGES = []
CURRENT_SEMESTER_LANGUAGES = []

// TODO: For symmetry, we'll prolly want to add "semester" as a property of each language.
//  Then we can initialize the set of starting languages to something like
//  Language.semester('F19');
// TODO: remove all spaces from keys of JSON files, in favor of underscores.
//      Otherwise it'll be a PITA to work with in JS.
// TODO: Generate one .json file for each semester's langauge data, same as we do now.
//  That one will be for human testing, etc.
//  But ALSO, generate one single .js file that contains all of the semesters' language
//  data smushed together. We can minify that one file to reduce download size.
//  (But honestly, the file will be cached after the first time, so not too bad).
// For reference, just a simple minification of one semester's JSON brings it from
// 24Kb to 11Kb, pretty much just by removing whitespace.
// We could do even better by compressing the repeated properties down.
// zipping that same 24kb gives just 4kb !!!

// TODO: This should be in its own file
// A Language is a relatively dumb wrapper around the raw JSON for a particular language.
// It consists of several properties.
// TODO: Languages should be immutable / frozen so we can pass around references
//      to them without fear of them being mutated. This lets us avoid some expensive
//      copy operations.
//  Languages should implement useful helper operations like equals() or toString()
class Language {

}

// TODO: Do I want properties to look like A or B?
// A:   {name: NAME, value: VALUE}
// B:   {NAME: VALUE}
// With A I can predictably look up `name`, but I might have to do linear scans for things
// instead of direct hash map lookups.
// In other words, I'd need a list of properties, not a dict where I merge all the properties together.
// Consider:
// merge({name: NAME1, value: VALUE1}, {name: NAME2, value: VALUE2}) =>
//      [{name: NAME1, value: VALUE1}, {name: NAME2, value: VALUE2}
// vs.
// merge({NAME1: VALUE1}, {NAME2: VALUE2}) =>
//      {NAME1: VALUE1, NAME2: VALUE2}
// I think I prefer B tbh.
class Property {
    constructor(name, value) {
        this.name = name;
        this.value = value;
    }
}

class Query {
    constructor(initial_languages = null) {
        if (initial_languages === null) {
            initial_languages = CURRENT_SEMESTER_LANGUAGES;
        }
        this.languages = initial_languages;

        // Which property is being inspected by this query?
        // (consonants, name, endangerment_level, ...)
        this.curr_property = null;

        // Which operation is being performed by this query on its property?
        // (compare, contains, length, ...)
        this.curr_operation = null;

        // The evaluation of the current query.
        // To start out, this just evaluates to a list of all the matched languages.
        this.evaluation = this.languages;
    }

    // Return a deep copy of this Query
    copy() {
        // todo

    }

    // Find the property p of all current languages.
    // Return a new Query focused on that property.
    property(p) {
        new_query = this.copy();

        // Operations act on properties, so we need to reset the operation
        // if we're changing to a new property.
        new_query.curr_property = p;
        new_query.curr_operation = null;

        // Update evaluation in the new query.
        // TODO.
        // 
        new_query.evaluate();

        return new_query;
    }

    // Update this query's current evaluation based on its curr_property and curr_operation.
    _evaluate(p) {
        // By the end of this function, this.evaluation will reflect the value
        // of this query.
        
        // There are a few cases.

        // 1. If this Query() is selecting a property, the evaluation will be a
        //      mapping from languages to the value of the property for that language.

        // e.g. Query().property('name') => [
        //          Result(language=Language(...), value='English'),
        //          Result(language=Language(...), value='Spanish'),
        //          Result(language=Language(...), value='French'),
        //      ]

        // 2. If this Query() is an operation that returns a bool, the evaluation
        //      will be this.languages, which will be updated to reflect the results of a filter.

        // e.g. Query().property('num_consonants').compare('geq', 10) => [
        //          Language(...) // num_cons = 20
        //          Language(...) // num_cons = 11
        //          Language(...) // num_cons = 10
        //          Language(...) // num_cons = 45
        //      ]

        // 3. If this Query() is an operation that returns a non-bool, the evaluation
        //      will apply that operation to each value of the previous evaluation.

        // e.g. Query().consonants().length() => [
        //          Result(language=Language(...), value=20),
        //          Result(language=Language(...), value=11),
        //          Result(language=Language(...), value=10),
        //          Result(language=Language(...), value=45),
        //      ]

        //this.evaluation = // TODO;
    }
}

// What do I want the caller to look like?
/**
 *  Language = Query();
 * 
 *  Language.semester('F19')
 * 
 *  Language.num_consonants().gt(5)
 *  Language.num_consonants().compare('gt', 5)
 *  Language.property('num_consonants').compare('gt', 5)
 *
 *  Language.consonants().contains('geq', 1, ['p', 't', 'k'])
 *  Language.consonants().filter(['p', 't', 'k']).length().geq(1)
 *  Language.consonants().intersection(['p', 't', 'k']).length().geq(1)
 *  Language.consonants().filter()
 *
 *  Language.tone().isTrue()
 *  Language.has('tone')
 *  Language.property('tone').eq(true);
 *
 *  Language.name().eq('Marui')
 *  Language.property('name').eq('Marui')
 *
 *  Language.endangerment_level().contained_in(['5', '6', '7', '8', '9'])
 *  Language.property('endangerment_level').contained_in(['5', '6', '7', '8', '9'])
 * 
 *  Language.num_consonants().between(4, 56)    // this could get a double-ended slider UI element
 *  Language.num_consonants().gt(4).lt(56)      // Should chaining work like this?
 *                                              // We'd need to keep track of which property was being checked last
 *                                              // and let lt(), gt() compare based on that property's value.
 * 
 *  Language.consonants().union(['p', 't', 'k'])\
 * (
 *  
 * 
 * 
 * 
 * 
 * 
 * Based on that, some ideas.
 * Query() creates a class that maintains some internal state about the query,
 * along with a running set of results.
 * 
 * Some of the state includes:
 *  - property being evaluated
 *  - operation being done on that property (compare, contains, contained_in, gt, lt), ...
 *  - the current set of matched languages
 *  - the current "evaluation" or "result" of the query, if it were to stop now.
 *      - if the last query asked for geq(4), this is a list of bools indicating which
        of the currently matched languages satisfy geq(4)
        - if the last query asked for .name(), this is a list of the namesof all currently
        matched languages.
    - we could get at the "evaluation" with a helper named something like "evaluate()" or "eval()"
      or "execute()" or "exec()" or "run()".. or just make it implied by the fact that we don't chain again.

 * 
 * Chaining Rules:
 *  - Chaining a new operation copies the previous query and overwrites operation.
 *  - Chaining a new property copies the previous query and overwrites the property (and nulls out the operation)
 */



class Language {
    constructor() {

    }

    // TODO: Eventually dynamically generate these.
    // IDK how rn so let's limit the scope to something manageable:
    // Let's just start implementing and see how far we get.

    name() {

    }

    num_consonants() {

    }

    consonants() {

    }

    consonant_types() {

    }

    num_consonant_places() {

    }

    tone() {

    }

    syllables() {

    }

}
