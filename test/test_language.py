import unittest

from app.language import Language, InvalidDataError

# Limited dataset, but has all required components
data1 = {
    "name": "Goemai",
    "student": "664ab8c0",
    "netid": "131eec04",
    "stress": True,
    "consonants": ["p", "t", "k", "m", "n"],
    "num consonants": 33,
}

# Incomplete dataset; illegal to construct Language with it
data2 = {
    "name": "Goemai",
    "stress": True,
}

class TestLanguage(unittest.TestCase):

    def test_1(self):
        lang = Language(data1)
        self.assertEqual(str(lang), "<Goemai language>")

    def test_2(self):
        lang = Language(data1)
        self.assertEqual(lang.name(), "Goemai")
        self.assertEqual(lang.student(), data1["student"])
        self.assertEqual(lang.netid(), data1["netid"])

    def test_3(self):
        lang = Language(data1)
        self.assertTrue(lang.stress)
        self.assertEqual(lang.consonants, data1["consonants"])

    def test_4(self):
        lang = Language(data1)
        with self.assertRaises(KeyError):
            x = lang.nonexistantField

    def test_5(self):
        with self.assertRaises(InvalidDataError):
            lang = Language(data2)


if __name__ == '__main__':
    unittest.main()
