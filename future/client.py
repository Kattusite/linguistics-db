import tinydb

path = "testdb.json"

def main():
    db = tinydb.TinyDB(path)

    lang = tinydb.Query()

    if not db.contains(lang.name == "Goemai"):
        db.insert({
            "name": "Goemai",
            "country": "Nigeria",
            "speakers": 150000,
            "num consonants": 24,
        })

    print(db.all())

main()
