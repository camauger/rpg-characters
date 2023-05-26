import json
import random
import os

from settings.random_settings import (
    pick_random_age,
    pick_random_gender,
    pick_random_ethnicity,
    pick_random_subrace,
    pick_random_character_class,
    pick_random_subclass,
    pick_random_background,
    get_ethnicity_keywords
)
from models.character_class import Character
from discord_bot import start_discord_bot


class CharacterManager:
    """Class to manage characters"""

    MAX_CHARACTER_ID = 9999  # Maximum character ID
    MAX_CHARACTER_COUNT = 9999  # Maximum number of characters
    FILE_PATH = "characters.json"  # Path to the JSON file containing character data

    def __init__(self):
        """Initialize the CharacterManager class"""
        self.characters = []  # Define the characters attribute as an empty list
        self.load_characters()  # Load existing characters from the JSON file

    def load_characters(self):
        """Load existing characters from the JSON file"""
        try:
            with open(self.FILE_PATH, "r") as json_file:
                character_data = json.load(json_file)
                self.characters = [
                    Character(character['id'], character)
                    for character in character_data
                ]

            print(f"Loaded {len(self.characters)} characters.")
        except (FileNotFoundError, json.JSONDecodeError):
            self.characters = []


    def save_characters(self, characters=None):
        """Append new characters to the existing characters in the JSON file"""
        # If no characters are passed, use the existing characters
        if characters is None:
            characters = self.characters

        # Transform all Character objects into dictionaries
        character_data = [character.to_dict() for character in characters]

        # Load existing data
        try:
            with open(self.FILE_PATH, 'r') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            existing_data = []

        # Append new data
        updated_data = existing_data + character_data

        # Write updated data to file
        with open(self.FILE_PATH, 'w') as json_file:
            json.dump(updated_data, json_file, indent=4)




    def check_character_count(self):
        """Check if the maximum number of characters has been reached"""
        if len(self.characters) >= self.MAX_CHARACTER_COUNT:
            print("There are too many characters. Please delete some characters before creating a new one.")
            return False
        return True

    def generate_character_id(self, existing_ids):
        """Generate a unique character ID"""
        character_id = random.randint(1, self.MAX_CHARACTER_ID)
        while character_id in existing_ids:
            character_id = random.randint(1, self.MAX_CHARACTER_ID)
        return character_id


    def get_character_params(self, is_random):
        """Get parameters for a new character"""
        params = {}
        params['random_class'] = pick_random_character_class() if is_random else input("What class do you want your character to be? ")
        params['random_subclass'] = pick_random_subclass(params['random_class']) if is_random else input("What subclass do you want your character to be? ")
        
        if is_random:
            params['random_ethnicity'] = pick_random_ethnicity()
            params['random_subrace'] = pick_random_subrace(params['random_ethnicity'])
        else:
            ethnicity_input = input("What is your character's ethnicity?")
            # Find the ethnicity based on the input (assuming the input matches a valid ethnicity)
            with open('data/ethnicity_data.json', 'r') as f:
                # Load the JSON string into a Python dictionary
                data = json.load(f)
            params['random_ethnicity'] = next(
                (ethnicity for ethnicity in data['ethnicity'] if ethnicity['race'] == ethnicity_input), None)

            if params['random_ethnicity']:
                params['random_ethnicity_name'] = params['random_ethnicity']['race']
                params['ethnicity_keywords'] = get_ethnicity_keywords(params['random_ethnicity'], params['random_subrace'])
                subrace_input = input("What is your character's subrace?")
                params['random_subrace'] = next((subrace for subrace in params['random_ethnicity'].get('subraces', []) if subrace['name'] == subrace_input), None)
            else:
                print("Invalid ethnicity input!")

        params['age'] = pick_random_age() if is_random else input("How old is your character? ")
        params['gender'] = pick_random_gender() if is_random else input("What is your character's gender?")
        params['background'] = pick_random_background() if is_random else input("What is your character's background?")
        return params

    def create_character(self, is_random):
        """Create a new character"""
        character_count, existing_ids = self.get_character_info()
        if self.check_character_count():
            params = self.get_character_params(is_random)
            character_id = self.generate_character_id(existing_ids)
            new_character = Character(character_id, params)
            existing_ids.append(character_id)  # Update the existing IDs list

            #new_character.update_has_image()
            # create a new text file with the prompt
            with open(f"./data/image_prompts/{new_character.picture_id}.txt", "w") as file:
                file.write(new_character.picture_id + "\n" + new_character.image_prompt + "\n")

            #self.save_characters(characters=[new_character])  # Save the new character to the JSON file
            #self.characters.append(new_character)  # Add the new character to the list
            return new_character
        return None




    def create_characters(self, num_characters):
        """Create multiple characters"""
        new_characters = []
        character_count, existing_ids = self.get_character_info()
        if self.check_character_count():
            for _ in range(num_characters):
                if character_count >= self.MAX_CHARACTER_COUNT:
                    print("There are too many characters. Please delete some characters before creating a new one.")
                    break
                new_character = self.create_character(is_random=True)
                if new_character:
                    new_characters.append(new_character)
                    
        return new_characters


    def create_random_character_option(self):
        """Create a number of random characters"""
        print("This program will create a number of random characters for you.")
        while True:
            num_characters = input("How many characters do you want to create? ")
            while not num_characters.isdigit() or int(num_characters) <= 0:
                num_characters = input("Please enter a valid number greater than 0: ")

            num_characters = int(num_characters)
            new_characters = self.create_characters(num_characters)
            if new_characters:
                self.characters.extend(new_characters)  # Add the new characters to the list
                self.save_characters(new_characters)  # Save the characters after creation

            print(f"Finished creating characters. There are now a total of {len(self.characters)} characters.")
            create_more = input("Do you want to create more characters? (y/n) ").lower()
            if create_more != 'y':
                start_bot = input("Do you want to start the Discord bot? (y/n) ").lower()
                if start_bot == 'y':
                    start_discord_bot()
                else:
                    break  # Exit the loop and continue running the program


    def update_character_prompt(self):
        """Prompt the user to update a character's information"""
        character_id = int(input("What is the ID of the character you want to update? "))
        new_info_input = input("Enter the new information you want to add in the format 'attribute value', separated by commas for multiple updates: ")

        # Convert the user's input into a dictionary
        new_info = {}
        for item in new_info_input.split(","):
            key, value = item.split()
            new_info[key] = value

        self.update_character(character_id, new_info)

    def update_character(self, character_id, new_info):
        """Update a character's information"""
        # Find the character
        character = next((c for c in self.characters if c.id == character_id), None)
        if not character:
            print(f"No character found with ID {character_id}.")
            return

        # Update the character's information
        for key, value in new_info.items():
            if hasattr(character, key):
                setattr(character, key, value)
            else:
                print(f"Invalid attribute: {key}")

        # Save the updated characters to the JSON file
        self.save_characters()

    def get_files_in_folder(self, folder_path):
        """Get list of files in a folder"""
        return [file_name for file_name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file_name))]

    def get_character_info(self):
        """Get information about existing characters"""
        try:
            with open(self.FILE_PATH, "r") as json_file:
                existing_characters = json.load(json_file)
            character_count = len(existing_characters)
            character_ids = [character.get('id') for character in existing_characters]
            return character_count, character_ids
        except (FileNotFoundError, json.JSONDecodeError):
            return 0, []
