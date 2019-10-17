import unittest

from app import responder, query

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

    def testSingleQuery(self):
        q = query.Num("num consonants", query.GT, 5)
        matches = q.query(testdb)


        HTML = responder.generateHTML([matches])
        print(HTML)

        # I have no idea how to automatically check this for correctness
        # (checking for direct equality with a known HTML string would work,
        # but seems fragile)

    def tearDown(self):
        testdb.close()

if __name__ == '__main__':
    unittest.main()
