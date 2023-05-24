import json
import random
from settings.random_settings import pick_random_age, pick_random_gender, pick_random_ethnicity, pick_random_subrace, pick_random_character_class, pick_random_subclass, pick_random_background, get_ethnicity_keywords
from models.character_class import Character
from utils.image_optim import optimize_images
from discord_bot import move_files, start_discord_bot
import os


class CharacterManager:
    """Class to manage characters"""
    """
    The CharacterManager class is used to manage characters in a game. It has several methods that can be used to create, save, and manage characters.
    The __init__ method initializes the class by loading existing characters from a JSON file.
    The load_characters method reads the JSON file and returns a list of existing characters.
    The save_characters method saves characters to a JSON file. The check_character_count method checks if the maximum number of characters has been reached.
    The get_character_info method gets information about existing characters. The generate_character_id method generates a unique character ID.
    The get_character_params method gets parameters for a new character.
    The create_character method creates a new character.
    The create_characters method creates multiple characters.
    The create_random_character_option method creates a number of random characters.
    The manage_characters method manages existing characters.
    The get_characters_with_image method gets characters with images.
    The get_characters_without_image method gets characters without images.
    The get_files_in_folder method gets a list of files in a folder.
    """
    MAX_CHARACTER_ID = 9999  # Maximum character ID
    MAX_CHARACTER_COUNT = 9999  # Maximum number of characters
    FILE_PATH = "characters.json"  # Path to the JSON file containing character data

    def __init__(self):
        """Initialize the CharacterManager class"""
        self.characters = self.load_characters(
        )  # Load existing characters from the JSON file

    def load_characters(self):
        """Load existing characters from the JSON file"""
        try:
            with open(self.FILE_PATH, "r") as json_file:
                existing_characters = json.load(json_file)
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
            json.dump(characters, json_file, indent=4,
                      default=lambda o: o.__dict__)

    def check_character_count(self):
        """Check if the maximum number of characters has been reached"""
        existing_characters = self.load_characters()
        if len(existing_characters) > self.MAX_CHARACTER_COUNT:
            print(
                "There are too many characters. Please delete some characters before creating a new one.")
            return False
        return True

    def get_character_info(self):
        """Get information about existing characters"""
        try:
            with open("characters.json", "r") as json_file:
                existing_characters = json.load(json_file)
            character_count = len(existing_characters)
            character_ids = [character.get('id')
                             for character in existing_characters]
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
        params['random_class'] = pick_random_character_class() if is_random else input(
            "What class do you want your character to be? ")
        params['random_subclass'] = pick_random_subclass(params['random_class']) if is_random else input(
            "What subclass do you want your character to be? ")
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
                subrace_input = input("What is your character's subrace?")
                params['random_subrace'] = next((subrace for subrace in params['random_ethnicity']['subraces'] if subrace['name'] == subrace_input), None)
            else:
                print("Invalid ethnicity input!")


        params['age'] = pick_random_age() if is_random else input(
            "How old is your character? ")
        params['gender'] = pick_random_gender() if is_random else input(
            "What is your character's gender?")
        params['background'] = pick_random_background() if is_random else input(
            "What is your character's background?")
        return params

    def create_character(self, is_random):
        """Create a new character"""
        character_count, existing_ids = self.get_character_info()
        if self.check_character_count():
            params = self.get_character_params(is_random)
            new_character = Character(self.generate_character_id(existing_ids),
                                      params)
            print(new_character.image_prompt)
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
        existing_characters = self.load_characters()
        characters = []
        while True:
            num_characters = input(
                "How many characters do you want to create? ")
            while not num_characters.isdigit() or int(num_characters) <= 0:
                num_characters = input(
                    "Please enter a valid number greater than 0: ")

            num_characters = int(num_characters)
            self.create_characters(num_characters)
            self.save_characters(self.characters)
            existing_characters = self.load_characters()
            print(f"Created {num_characters} character(s).")
            print(
                f"Finished creating characters. There are now a total of {len(existing_characters)} characters.")
            create_more = input(
                "Do you want to create more characters? (y/n) ").lower()
            if create_more != 'y':
                start_bot = input(
                    "Do you want to start the Discord bot? (y/n) ").lower()
                if start_bot == 'y':
                    start_discord_bot()
                else:
                    break
            

    def manage_characters(self):
        """Manage existing characters"""
        characters_dicts = [
            character.__dict__ for character in self.characters]
        self.characters.extend(characters_dicts)
        self.save_characters(self.characters)
        prompts = [character_data.get(
            'image_prompt') + '\n\n' for character_data in self.characters]
        with open('data/image_prompts.txt', 'w') as file:
            file.writelines(prompts)

    def get_characters_with_image(self):
        """Get characters with images"""
        folder_path = "./static/images/"
        files_in_folder = self.get_files_in_folder(folder_path)
        characters_with_images = [
            character for character in self.characters if f"{character.get('id')}.png" in files_in_folder]
        self.save_characters(characters_with_images,
                             "characters_with_images.json")
        print(f"There are {len(characters_with_images)} characters with images." if characters_with_images else "There are no characters with images.")

    def get_characters_without_image(self):
        """Get characters without images"""
        files_in_folder = self.get_files_in_folder("./static/images/")
        characters_without_images = [
            character for character in self.characters if f"{character.get('id')}.png" not in files_in_folder]
        self.save_characters(characters_without_images,
                             "characters_without_images.json")
        prompts = [character_data.get(
            'image_prompt') + '\n\n' for character_data in characters_without_images]
        with open('data/characters_without_images.txt', 'w') as file:
            file.writelines(prompts)

    def get_files_in_folder(self, folder_path):
        """Get list of files in a folder"""
        return [file_name for file_name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file_name))]


def main():
    print("Welcome to the RPG Character Generator!")
    character_manager = CharacterManager()

    # Menu
    print("1. Create random characters")
    print("2. Optimize images")
    print("3. Create a specific character")
    print("4. Archive files")
    print("5. Manage characters")
    print("6. Start the Discord bot")
    print("0. Exit the program")

    choice = input("What do you want to do? ")

    if choice == "1":
        if character_manager.check_character_count():
            character_manager.create_random_character_option()
    elif choice == "2":
        optimize_images("./large_images", "./static/images")
        print("Images optimized!")
        exit()
    elif choice == "3":
        if character_manager.check_character_count():
            character_manager.create_character(is_random=False)
    elif choice == "4":
        move_files()
        print("Files moved!")
        exit()
    elif choice == "5":
        character_manager.manage_characters()
        character_manager.get_characters_with_image()
        character_manager.get_characters_without_image()
        print("Characters managed!")
        exit()
    elif choice == "6":
        print("Starting the Discord bot...")
        start_discord_bot()
    elif choice == "0":
        print("Goodbye!")
        exit()


if __name__ == "__main__":
    main()
