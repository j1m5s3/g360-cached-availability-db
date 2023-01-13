import csv
import json
from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

client = MongoClient(config['DB_CONNECTION_URL'])
db = client[config['DB_NAME']]
collection = db[config['COLLECTION_NAME']]
collection.drop()


def run():

    with open('./data/cached_avail_1_12_2023.csv', 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        i = 0
        for row in csv_reader:
            row_keys_list = list(row.keys())
            property_guid = row_keys_list[0]
            response = json.loads(row_keys_list[1])
            effective_date = response['serviceChargePeriods'][0]['effectiveDate']
            row_dict = {"property_guid": property_guid,
                        "response": response,
                        "effective_date": effective_date}

            res = collection.insert_one(row_dict)
            created_entry = collection.find_one({"_id": res.inserted_id})
            print("created_entry: ", created_entry)


if __name__ == "__main__":
    run()
    pass
