import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient


# Load environment variables
load_dotenv()
mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')

# Connect to MongoDB
client = MongoClient(mongo_connection_string)
db = client[os.getenv('MONGO_DB_NAME')]  # This should be the name of your database
collection = db['clothing']  # Replace with your collection name

# Fetch data from collection
data = list(collection.find({}))  # This fetches all documents in the collection

# Save data to JSON file
with open('output.json', 'w') as file:
    json.dump(data, file, default=str)  # Using default=str to handle any non-serializable data like ObjectId

print("Data saved to output.json successfully.")
