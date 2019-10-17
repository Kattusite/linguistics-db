import unittest

from app import querier, query

payload = """[
    {
        "mode":"at least",
        "k":"1",
        "selList":["voiced"],
        "trait":"metaclass-selector",
        "reply":"have at least 1 phoneme that is voiced"
    },
    {"trait":"tone-selector","reply":"have tone"},
    {
        "mode":"at least",
        "k":"1",
        "selList":["mostly head-final"],
        "trait":"headedness-selector",
        "reply":"are at least 1 of mostly head-final"
    },
    {
        "mode":"at least",
        "k":"28",
        "selList":["vowels"],
        "sel":"vowels",
        "trait":"phoneme-inventory-size-selector",
        "reply":"have a phoneme inventory with at least 28 vowels"
    }
]"""


class ExampleRequest():
    def __init__(self, form):
        self.form = {
            "payload": payload,
        }

class TestQuery(unittest.TestCase):



    def testSingleQuery(self):

        req = ExampleRequest(payload)

        queries = querier.queriesFromRequest(req)
        print(queries)



if __name__ == '__main__':
    unittest.main()
