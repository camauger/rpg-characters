import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

# Load environment variables
load_dotenv()
mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')

# Connect to MongoDB
client = MongoClient(mongo_connection_string)
# This should be the name of your database
db = client[os.getenv('MONGO_DB_NAME')]
collection_name = 'clothing'  # Replace with your collection name
collection = db[collection_name]
data_folder = 'data'


def get_data(filename):
    with open(f'{data_folder}/{filename}.json', 'r') as file:
        data = json.load(file)
    return data


def update_collection_from_json():
    data = get_data(collection_name)

    for item in data:
        print(type(item), item) 
        # Assuming 'id' is the unique identifier in your collection
        # Check if '_id' exists in the item
        if '_id' in item:
            # Convert the string _id to ObjectId
            unique_id = ObjectId(item['_id'])

            # Remove the '_id' from the item before updating
            item_without_id = {key: value for key, value in item.items() if key != '_id'}
            collection.update_one({'_id': unique_id}, {'$set': item_without_id}, upsert=True)

        else:
            # Handle the case where '_id' is missing
            collection.insert_one(item)

        unique_id = item['_id']
        collection.update_one({'_id': unique_id}, {'$set': item}, upsert=True)


# Update collection from JSON
update_collection_from_json()

print("Collection updated successfully.")
