from pymongo import MongoClient
from models.character_class import Character
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')

# Connect to MongoDB
client = MongoClient(mongo_connection_string)
db = client[os.getenv('MONGO_DB_NAME')]  # This should be the name of your database

# Get the OpenAI API key
api_key = os.environ.get('API_KEY')

if __name__ == "__main__":
    # Create a new character
    new_character = Character()
    print("Let's create a random character!")
    new_character.create_character(params={
    }, is_random=True)
    #print(new_character.to_json())

    try:
        new_character.save()
        print("Character saved!")
    except Exception as e:
        print(f"An error occurred: {e}")
    print(new_character.__str__() + "\n")
