import json
import random
from settings.random_settings import pick_random_age, pick_random_gender, pick_random_ethnicity, pick_random_subrace, pick_random_character_class, pick_random_subclass, pick_random_background, get_ethnicity_keywords
from models.character_class import Character
from discord_bot import start_discord_bot, send_message_to_channel
import os


class CharacterManager:
    """Class to manage characters"""

    MAX_CHARACTER_ID = 9999  # Maximum character ID
    MAX_CHARACTER_COUNT = 9999  # Maximum number of characters
    FILE_PATH = "characters.json"  # Path to the JSON file containing character data

    def __init__(self):
        """Initialize the CharacterManager class"""
        self.characters = self.load_characters()  # Load existing characters from the JSON file

    def load_characters(self):
        """Load existing characters from the JSON file"""
        try:
            with open(self.FILE_PATH, "r") as json_file:
                character_data = json.load(json_file)
                existing_characters = [Character(character['id'], character) for character in character_data]
            return existing_characters
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_characters(self, characters=None, filename=None):
        """Save characters to a JSON file"""
        if characters is None:
            characters = self.characters
        if filename is None:
            filename = self.FILE_PATH
        with open(filename, "w") as json_file:
            json.dump(characters, json_file, indent=4, default=lambda o: o.__dict__)

    def check_character_count(self):
        """Check if the maximum number of characters has been reached"""
        if len(self.characters) > self.MAX_CHARACTER_COUNT:
            print("There are too many characters. Please delete some characters before creating a new one.")
            return False
        return True

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

    def generate_character_id(self, existing_ids):
        """Generate a unique character ID"""
        while True:
            character_id = random.randint(1, self.MAX_CHARACTER_ID)
            if character_id not in existing_ids:
                return character_id

    def get_character_params(self, is_random):
        """Get parameters for a new character"""
        params = {}
        params['random_class'] = pick_random_character_class() if is_random else input("What class do you want your character to be? ")
        params['random_subclass'] = pick_random_subclass(params['random_class']) if is_random else input("What subclass do you want your character to be? ")
        params['random_class_name'] = params['random_class']

        if is_random:
            params['random_ethnicity'] = pick_random_ethnicity()
            params['random_ethnicity_name'] = params['random_ethnicity']['race']
            params['random_subrace'] = pick_random_subrace(params['random_ethnicity'])
        else:
            ethnicity_input = input("What is your character's ethnicity?")
            # Find the ethnicity based on the input (assuming the input matches a valid ethnicity)
            with open('data/ethnicity_data.json', 'r') as f:
                # Load the JSON string into a Python dictionary
                data = json.load(f)
            params['random_ethnicity'] = next((ethnicity for ethnicity in data['ethnicity'] if ethnicity['race'] == ethnicity_input), None)

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
            new_character = Character(self.generate_character_id(existing_ids), params)
            send_message_to_channel(new_character.image_prompt)
            return new_character
        return None

    def create_characters(self, num_characters):
        """Create multiple characters"""
        for _ in range(num_characters):
            new_character = self.create_character(is_random=True)
            self.characters.append(new_character)

    def create_random_character_option(self):
        """Create a number of random characters"""
        print("This program will create a number of random characters for you.")
        while True:
            num_characters = input("How many characters do you want to create? ")
            while not num_characters.isdigit() or int(num_characters) <= 0:
                num_characters = input("Please enter a valid number greater than 0: ")

            num_characters = int(num_characters)
            self.create_characters(num_characters)
            self.save_characters(self.characters)
            existing_characters = self.characters
            print(f"Created {num_characters} character(s).")
            print(f"Finished creating characters. There are now a total of {len(existing_characters)} characters.")
            create_more = input("Do you want to create more characters? (y/n) ").lower()
            if create_more != 'y':
                start_bot = input("Do you want to start the Discord bot? (y/n) ").lower()
                if start_bot == 'y':
                    start_discord_bot()
                else:
                    exit()

    def manage_characters(self):
        """Manage existing characters"""
        prompts = [character_data.image_prompt + '\n\n' for character_data in self.characters if character_data.image_prompt is not None]

        with open('data/image_prompts.txt', 'w') as file:
            file.writelines(prompts)



    def get_characters_by_image(self, has_image=True):
        """Get characters based on whether they have images"""
        folder_path = "./static/images/"
        files_in_folder = self.get_files_in_folder(folder_path)
        
        if has_image:
            characters = [character for character in self.characters if f"{character.picture_id}.png" in files_in_folder]
            filename = "characters_with_images.json"
        else:
            characters = [character for character in self.characters if f"{character.picture_id}.png" in files_in_folder]
            filename = "characters_without_images.json"
        
        self.save_characters(characters, filename)
        
        # If getting characters without images, write image prompts to a file
        if not has_image:
            prompts = [character_data.get('image_prompt') + '\n\n' for character_data in characters]
            with open('data/characters_without_images.txt', 'w') as file:
                file.writelines(prompts)
        
        print(f"There are {len(characters)} characters{' with' if has_image else ' without'} images." if characters else f"There are no characters{' with' if has_image else ' without'} images.")

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
