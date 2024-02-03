from dotenv import load_dotenv
from pymongo import MongoClient
import os
import logging
import json
import random
from models.character_class import Character



class CharacterManager:

    MAX_CHARACTER_ID = 9999  # Maximum character ID

    def __init__(self):
        load_dotenv()
        self.MONGO_DB_URI = os.getenv('MONGO_DB_URI')
        self.MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
        self.MONGO_DB_COLLECTION = os.getenv('MONGO_DB_COLLECTION')

        client = MongoClient(self.MONGO_DB_URI)
        db = client[self.MONGO_DB_NAME]
        self.characters_collection = db[self.MONGO_DB_COLLECTION]

    def create_character(self, params={}, is_random=True, is_fantasy=False):
        character_id = random.randint(1, self.MAX_CHARACTER_ID)
        # Check if character with generated ID already exists
        while self.characters_collection.find_one({'id': character_id}):
            # Generate a new ID if the previous one exists
            character_id = random.randint(1, self.MAX_CHARACTER_ID)
        params = self.get_character_params(is_random, is_fantasy)
        character = Character(id=character_id, **params)
        character.save()
        return character

    def load_characters(self):
        try:
            self.characters = list(self.characters_collection.find({}))
        except Exception as e:
            logging.error(f"An error occurred while loading characters: {e}")

    def save_characters(self, characters=None):
        if characters is None:
            characters = self.characters
        try:
            for character in characters:
                # Assuming Character class has a method to_dict() for serialization
                character_dict = character.to_dict() if hasattr(
                    character, 'to_dict') else character
                self.characters_collection.insert_one(character_dict)
                print(f"Character {character_dict['id']} saved successfully.")
        except Exception as e:
            logging.error(f"An error occurred while saving characters: {e}")

    def get_character_params(self):
        params = {
            'full_name': input("Character name: "),
            'ethnicity': input("Character ethnicity: "),
            'subrace': input("Character subrace: "),
            'character_class': input("Character class: "),
            'character_subclass' : input("Character subclass: "),
            'age': input("Character age: "),
            'gender': input("Character gender: "),
            'background': input("Character background: "),

        }

            #self.user_defined_ethnicity_and_subrace(params)
        return params

    def user_defined_ethnicity_and_subrace(self, params):
        """Helper function to handle user input for ethnicity and subrace"""
        ethnicity_input = input("Character ethnicity: ")
        with open('data/ethnicity_data.json', 'r') as file:
            data = json.load(file)
            params['random_ethnicity'] = next(
                (e for e in data['ethnicity'] if e['race'] == ethnicity_input), None)
            if params['random_ethnicity']:
                params['random_subrace'] = next((subrace for subrace in params['random_ethnicity'].get(
                    'subraces', []) if subrace['name'] == input("Character subrace: ")), None)
            else:
                print("Invalid ethnicity input!")

    def create_characters(self, num_characters):
        new_characters = []

        for _ in range(num_characters):
            new_character = self.create_character(
                params=[], is_random=True)
            if new_character:
                new_characters.append(new_character)
                print("Character created successfully.")

        return new_characters

    def create_random_character_option(self):
        print("This program will create a number of random characters for you.")
        while True:
            num_characters = input(
                "How many characters do you want to create? ")
            while not num_characters.isdigit() or int(num_characters) <= 0:
                num_characters = input(
                    "Please enter a valid number greater than 0: ")

            num_characters = int(num_characters)
            new_characters = self.create_characters(num_characters)
            if new_characters:
                # convert the characters to a list of dictionaries
                new_characters = [c.to_dict() for c in new_characters]
                self.save_characters(new_characters)

            print(
                f"Finished creating characters.")
            create_more = input(
                "Do you want to create more characters? (y/n) ").lower()
            if create_more != 'y':
                break  # Exit the loop and continue running the program

    def update_character_prompt(self):
        """Prompt the user to update a character's information"""
        character_id = int(
            input("What is the ID of the character you want to update? "))
        new_info_input = input(
            "Enter the new information you want to add in the format 'attribute value', separated by commas for multiple updates: ")

        # Convert the user's input into a dictionary
        new_info = {}
        for item in new_info_input.split(","):
            key, value = item.split()
            new_info[key] = value

        self.update_character(character_id, new_info)

    def update_character(self, character_id, new_info):
        """Update a character's information"""
        # Find the character
        character = next(
            (c for c in self.characters if c.id == character_id), None)
        if not character:
            print(f"No character found with ID {character_id}.")
            return

        # Update the character's information
        for key, value in new_info.items():
            if hasattr(character, key):
                setattr(character, key, value)
            else:
                print(f"Invalid attribute: {key}")

        self.save_characters()

