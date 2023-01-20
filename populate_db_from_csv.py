import csv
import json
from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

client = MongoClient(config['DB_CONNECTION_URL'])
db = client[config['DB_NAME']]
cached_collection = db[config['CACHED_COLLECTION_NAME']]
property_collection = db[config['PROPERTY_COLLECTION_NAME']]
#cached_collection.drop()
#property_collection.drop()


def run_populate_cached_collection():
    with open('./data/cached_avail_1_19_2023.csv', 'r') as cached_avail_file:
        cached_csv_reader = csv.DictReader(cached_avail_file)
        with open('./data/properties_has_rooms_enabled_1_19_2023.csv', 'r') as properties_file:
            properties_csv_reader = csv.DictReader(properties_file)
            property_guids = list(map(lambda x: x['guid'], properties_csv_reader))
            i = 0
            for cached_row in cached_csv_reader:
                property_guid = cached_row['property_guid']
                response = cached_row['response']
                response_dict = json.loads(response)
                effective_date = response_dict['taxPeriods'][0]['effectiveDate']
                if "2023" in effective_date and property_guid in property_guids:
                    row_dict = {"property_guid": property_guid,
                                "response": response,
                                "effective_date": effective_date,
                                }
                    res = cached_collection.insert_one(row_dict)
                    created_entry = cached_collection.find_one({"_id": res.inserted_id})
                    print("cached_entry: ", created_entry)

    return


def run_populate_property_collection():
    with open('./data/properties_has_rooms_enabled_1_19_2023.csv', 'r') as properties_file:
        properties_csv_reader = csv.DictReader(properties_file)
        i = 0
        for property_row in properties_csv_reader:
            res = property_collection.insert_one(property_row)
            created_entry = property_collection.find_one({"_id": res.inserted_id})
            print("property_entry: ", created_entry)

    return


if __name__ == "__main__":
    run_populate_property_collection()
    run_populate_cached_collection()
    pass
