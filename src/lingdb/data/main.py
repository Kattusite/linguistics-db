from . import json_to_db
from . import csv_to_json

def main():
    csv_to_json.main()
    print("csv to json conversion complete.")

    json_to_db.main()
    print("json to db conversion complete.")
