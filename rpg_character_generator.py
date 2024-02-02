from dotenv import load_dotenv
from models.character_manager_class import CharacterManager
from mongoengine import connect
from pymongo import MongoClient
from utils.image_optim import optimize_images
import logging
import os
from mongoengine import disconnect

# Load .env file
load_dotenv()

# Check if environment variable is set
if not 'MONGO_CONNECTION_STRING' in os.environ:
    logging.error('Missing MONGO_CONNECTION_STRING! Ensure file .env has correct data')
    exit(1)

try:
    # Connect to your MongoDB database
    client = MongoClient(os.getenv('MONGO_CONNECTION_STRING'))
    db = client.rpg
    collection = db.rpgCharacters
    print("Connected to MongoDB")
except Exception as e:
    logging.error(f"An error occurred while connecting to MongoDB with the following details:\n{str(e)}")



# Setting up logging
logging.basicConfig(level=logging.INFO)

MENU_OPTIONS = {
    "1": {"message": "Create random characters", "method": "create_character"},
    "2": {"message": "Optimize images", "method": None},
    "3": {"message": "Create a specific character", "method": "create_character", "args": [False]},
    "4": {"message": "Update a specific character", "method": "update_character_prompt"},
    "5": {"message": "Create a fantasy character", "method": "create_character", "args": [False, True]},
    "0": {"message": "Exit the program", "method": None}
}


class RPGCharacterGenerator:
    def __init__(self):
        self.character_manager = CharacterManager()

    @staticmethod
    def print_menu():
        for option, details in MENU_OPTIONS.items():
            print(f"{option}. {details['message']}")

    def user_choice(self, choice):
        if choice in MENU_OPTIONS:
            if choice == "2":
                optimize_images("./large_images", "./static/images")
                print("Images optimized!")
                return True

            if choice == "0":
                disconnect()
                print("Goodbye!")
                return False

            method = getattr(self.character_manager,
                             MENU_OPTIONS[choice]['method'])
            args = MENU_OPTIONS[choice].get('args', [])

            method(*args)

        else:
            print("Invalid choice!")

        return True

    def main_loop(self):
        while True:
            self.print_menu()
            choice = input("What do you want to do? ")
            if not self.user_choice(choice):
                break


if __name__ == "__main__":
    rpg_gen = RPGCharacterGenerator()
    rpg_gen.main_loop()
