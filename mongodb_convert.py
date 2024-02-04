import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient


# Load environment variables
load_dotenv()
mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')

# Connect to MongoDB
client = MongoClient(mongo_connection_string)
# This should be the name of your database
db = client[os.getenv('MONGO_DB_NAME')]

# Data folder
data_folder = 'data'
# Check if the data folder exists
if not os.path.exists(data_folder):
    print(f"Data folder {data_folder} does not exist.")
    exit()

# The json file should be structured to match the data insertion needs
filename = 'clothing'
# check if the file exists
if not os.path.exists(f'{data_folder}/{filename}.json'):
    print(f"File {filename}.json does not exist.")
    exit()


def read_json_file(filename):
    with open(f'{data_folder}/{filename}.json', 'r') as file:
        data = json.load(file)
    return data  # Assuming the JSON structure provided earlier


def create_collection(filename, data):
    # Assuming 'clothing' is both the filename and collection name; adjust as needed
    collection = db[filename]
    collection.insert_many(data)
    print("Data inserted into MongoDB collection successfully.")


data = read_json_file(filename)
create_collection(filename, data)

print("Data inserted into MongoDB collection successfully.")
