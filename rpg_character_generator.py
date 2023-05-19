import json, random
from settings.random_settings import pick_random_age, pick_random_gender, pick_random_ethnicity, pick_random_character_class, pick_random_subclass, pick_random_background, get_ethnicity_keywords
from models.character_class import Character
from utils.image_optim import optimize_images
from discord_bot import move_files, start_discord_bot
import os

MAX_CHARACTER_ID = 9999
MAX_CHARACTER_COUNT = 9999

def check_character_count():
    existing_characters = load_characters()
    if len(existing_characters) > MAX_CHARACTER_COUNT:
        print("There are too many characters. Please delete some characters before creating a new one.")
        return False
    else:
        return True
    
# Get the number of characters and their IDs from the JSON file
# Usage:
#character_count, existing_ids = get_character_info()
def get_character_info():
    try:
        with open("characters.json", "r") as json_file:
            existing_characters = json.load(json_file)
        character_count = len(existing_characters)
        character_ids = [character.get('id') for character in existing_characters]
        return character_count, character_ids
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle file not found or invalid JSON error
        return 0, []

# Generate a random character ID
def generate_character_id(existing_ids):
    while True:
        # Generate a random number as the character ID
        character_id = random.randint(1, MAX_CHARACTER_ID)
        
        # Check if the generated ID already exists in the list
        if character_id not in existing_ids:
            return character_id


# Create a non random character
def create_specific_character():
    character_count, existing_ids = get_character_info()
    params = {}
    params["random class"] = input("What class do you want your character to be? ")
    params['random_subclass'] = input("What subclass do you want your character to be? ")
    params['random_class_name'] = params['random_class']
    params['random_ethnicity']= input("What is your character's ethnicity?")
    params['random_ethnicity_name'] = params['random_ethnicity'].get('race')
    params['ethnicity_keywords'] = get_ethnicity_keywords(params['random_ethnicity'])
    params['age'] = input("How old is your character? ")
    params['gender'] = input("What is your character's gender?")
    params['background'] = input("What is your character's background?")
    new_character = Character(generate_character_id(existing_ids), params)
    return new_character
   

# Create a random character
def create_random_params():
    params = {}
    params['random_class'] = pick_random_character_class()
    params['random_subclass'] = pick_random_subclass(params['random_class'])
    params['random_class_name'] = params['random_class']
    params['random_ethnicity'] = pick_random_ethnicity()
    params['random_ethnicity_name'] = params['random_ethnicity'].get('race')
    params['ethnicity_keywords'] = get_ethnicity_keywords(params['random_ethnicity'])
    params['age'] = pick_random_age()
    params['gender'] = pick_random_gender()
    params['background'] = pick_random_background()
    return params

def create_random_character():
    params = create_random_params()
    character_count, existing_ids = get_character_info()
    if check_character_count():
        new_character = Character(generate_character_id(existing_ids), params)
        print(new_character.image_prompt)
        return new_character
    else:
        None


#Load the characters from the json file
def load_characters():
    try:
        with open("characters.json", "r") as json_file:
            existing_characters = json.load(json_file)
        return existing_characters
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle file not found or invalid JSON error
        return []

# Save the characters to a json file
def save_characters(characters):
    with open("characters.json", "w") as json_file:
        json.dump(characters, json_file, indent=4, default=lambda o: o.__dict__)

# Create a number of random characters
def create_characters(num_characters, characters):
    for _ in range(num_characters):
        new_character = create_random_character()
        characters.append(new_character)
        # print(new_character.image_prompt)
    return characters

# Manage the creation of random characters
def create_random_character_option():
    print("This program will create a number of random characters for you.")
    existing_characters = load_characters()
    characters = []
    while True:
        num_characters = input("How many characters do you want to create? ")
        while not num_characters.isdigit() or int(num_characters) <= 0:
            num_characters = input("Please enter a valid number greater than 0: ")
        
        num_characters = int(num_characters)
        characters = create_characters(num_characters, characters)
        print(f"Created {len(characters)} character(s).")

        create_more = input("Do you want to create more characters? (y/n) ").lower()
        if create_more != 'y':
            break
    existing_characters.extend(characters)
    save_characters(existing_characters)
    print(f"Finished creating characters. There are now a total of {len(existing_characters)} characters.")


characters = []

def manage_characters():
    # Load existing characters from the JSON file
    existing_characters = load_characters()
    print(len(existing_characters))

    # Convert Character instances to dictionaries
    character_dicts = [character.__dict__ for character in characters]

    # Append new characters to the existing list
    existing_characters.extend(character_dicts)

    # Write the updated characters to the JSON file
    with open("characters.json", "w") as json_file:
        json.dump(existing_characters, json_file, indent=4, default=lambda o: o.__dict__)

    # Create a list of image prompts
    prompts = []
    for character_data in existing_characters:
        image_prompt = character_data.get('image_prompt')
        prompts.append(image_prompt + '\n\n')

    # Write the image prompts to a text file
    with open('data/image_prompts.txt', 'w') as file:
        file.writelines(prompts)

# Final data


def get_files_in_folder(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        # Check if the path is a file (not a directory)
        if os.path.isfile(os.path.join(folder_path, file_name)):
            files.append(file_name)
    return files


# Get all the characters with an image in images folder
def get_characters_with_image():
    existing_characters = load_characters()
    folder_path = "./static/images/"
    files_in_folder = get_files_in_folder(folder_path)
    characters_with_images = []
    for character in existing_characters:
        image_name = f"{character.get('id')}.png"
        if image_name in files_in_folder:
            characters_with_images.append(character)

    # Write the characters with images to a JSON file
    with open("characters_with_images.json", "w") as json_file:
        json.dump(characters_with_images, json_file, indent=4, default=lambda o: o.__dict__)
        if len(characters_with_images) > 0:
            print(f"There are {len(characters_with_images)} characters with images.")
        else:
            print("There are no characters with images.")


# Get all the characters without an image in images folder
def get_characters_without_image():
    existing_characters = load_characters()
    files_in_folder = get_files_in_folder("./static/images/")
    characters_without_images = []
    for character in existing_characters:
        image_name = f"{character.get('id')}.png"
        if image_name not in files_in_folder:
            characters_without_images.append(character)

    # Write the characters without images to a JSON file
    with open("characters_without_images.json", "w") as json_file:
        json.dump(characters_without_images, json_file, indent=4, default=lambda o: o.__dict__)
        if len(characters_without_images) > 0:
            print(f"There are {len(characters_without_images)} characters without images.")
        else:
            print("There are no characters without images.")

    # Create a list of image prompts of the characters without images
    prompts = []
    for character_data in characters_without_images:
        image_prompt = character_data.get('image_prompt')
        prompts.append(image_prompt + '\n\n')

    # Write the image prompts to a text file
    with open('data/characters_without_images.txt', 'w') as file:
        file.writelines(prompts)


# Create a list of unique characters
existing_characters = load_characters()
characters = []
print("Welcome to the RPG Character Generator!")

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
    if check_character_count():
        create_random_character_option()
elif choice == "2":
    optimize_images("./large_images", "./static/images")
    print("Images optimized!")
    exit()
elif choice == "3":
    if check_character_count():
        create_specific_character()
elif choice == "4":
    move_files()
    print("Files moved!")
    exit()
elif choice == "5":
    manage_characters()
    get_characters_with_image()
    get_characters_without_image()
    print("Characters managed!")
    exit()
elif choice == "6":
    print("Starting the Discord bot...")
    start_discord_bot()
elif choice == "0":
    print("Goodbye!")
    exit()