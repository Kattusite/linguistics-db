import unittest

from app import query

import tinydb

# Bogus data for testing
data = [
    {
        "name": "English",
        "netid": "",
        "student": "",
        "consonants": ["p", "t", "k", "b", "d", "g", "m", "n"],
        "stress": True,
        "tone": False,
        "country": "America",
        "num consonants": 33,
    },
    {
        "name": "French",
        "netid": "",
        "student": "",
        "consonants": ["k", "b", "d", "g", "m", "n", "l", "r", "s"],
        "stress": False,
        "tone": False,
        "country": "France",
        "num consonants": 18,
    },
    {
        "name": "Spanish",
        "netid": "",
        "student": "",
        "consonants": ["p", "t", "m", "n", "j", "v", "z", "x", "w", "q"],
        "stress": True,
        "tone": True,
        "country": "Spain",
        "num consonants": 11,
    },
]

testdb = None

class TestQuery(unittest.TestCase):

    def setUp(self):
        global testdb
        testdb = tinydb.TinyDB("testdb.json")
        testdb.purge()

        for lg in data:
            testdb.insert(lg)

    def testBasic(self):
        res = testdb.all()
        self.assertEqual(len(res), 3)

    def testString(self):
        q = query.String("country", query.EQ, "France")
        matches = q.query(testdb)
        self.assertEqual(len(matches), 1)
        m = matches[0]
        self.assertEqual(m.language.name(), "French")
        self.assertEqual(m.cause, "France")

    def queryHelper(self, q, expCauses):
        """Given a query q, run the query against testdb to ensure
        that it has exactly n matches, where n = len(expCauses), and the causes
        for each match were exactly equal to those provided in expCauses.
        Both lists of causes will be sorted before comparison.

        Note this may fail if list sorting works in a weird way; e.g. by length
        because the sort order may not be deterministic - look at docs.
        Pretty sure it won't be an issue
        """
        matches = q.query(testdb)
        n = len(expCauses)
        self.assertEqual(len(matches), n)
        causes = [m.cause for m in matches]

        # If this is a
        if q.type == query.LIST:
            causes = [set(c) for c in causes]
            expCauses = [set(c) for c in expCauses]

        self.assertEqual(sorted(causes), sorted(expCauses))

    # Num queries
    def testNum1(self):
        q = query.Num("num consonants", query.GT, 5)
        self.queryHelper(q, [11, 18, 33])

    def testNum2(self):
        q = query.Num("num consonants", query.LT, 5)
        self.queryHelper(q, [])

    def testNum3(self):
        q = query.Num("num consonants", query.GT, 11)
        self.queryHelper(q, [18, 33])

    def testNum4(self):
        q = query.Num("num consonants", query.GEQ, 18)
        self.queryHelper(q, [18, 33])

    def testNum5(self):
        q = query.Num("num consonants", query.NEQ, 33)
        self.queryHelper(q, [11, 18])

    def testNum6(self):
        q = query.Num("num consonants", query.EQ, 18)
        self.queryHelper(q, [18])

    # List queries
    def testList1(self):
        q = query.List("consonants", query.GT, 2, ["p", "t", "k"])
        self.queryHelper(q, [["p", "t", "k"]])

    def testList2(self):
        q = query.List("consonants", query.LT, 3, ["p", "t", "k"])
        self.queryHelper(q, [["k"], ["p", "t"]])

    # Bool queries
    def testBool1(self):
        q = query.Bool("stress", False)
        results = q.query(testdb)
        self.assertEqual(results[0].language.name(), "French")

    def tearDown(self):
        testdb.close()

if __name__ == '__main__':
    unittest.main()
