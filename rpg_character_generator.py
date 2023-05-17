import json, random
from settings.random_settings import pick_random_age, pick_random_gender, pick_random_ethnicity, pick_random_character_class, pick_random_subclass, pick_random_background, get_ethnicity_keywords
from models.character_class import Character

# You will have to create your own api_settings.py file with your OpenAI API key
from api_settings import api_key

def get_number_of_existing_characters():
    try:
        with open("characters.json", "r") as json_file:
            existing_characters = json.load(json_file)
            json_file.close()
        return len(existing_characters)
    except (FileNotFoundError, json.JSONDecodeError):
        # Handle file not found or invalid JSON error
        return 0
    
def get_existing_character_ids():
    try:
        with open("characters.json", "r") as json_file:
            existing_characters = json.load(json_file)
            json_file.close()
        return [character.get('id') for character in existing_characters]

    except (FileNotFoundError, json.JSONDecodeError):
        # Handle file not found or invalid JSON error
        return 0

existing_ids = get_existing_character_ids()

def generate_character_id(existing_ids):
    while True:
        # Generate a random number as the character ID
        character_id = random.randint(1, 9999)
        
        # Check if the generated ID already exists in the list
        if character_id not in existing_ids:
            return character_id


# Create a random character
def create_random_character():
    random_class = pick_random_character_class()
    random_subclass = pick_random_subclass(random_class)
    random_class_name = random_class.get('name')
    random_ethnicity = pick_random_ethnicity()
    random_ethnicity_name = random_ethnicity.get('race')
    ethnicity_keywords = get_ethnicity_keywords(random_ethnicity)
    id
    new_character = Character(generate_character_id(existing_ids), random_class_name, random_subclass, pick_random_background(), random_ethnicity_name, ethnicity_keywords, pick_random_age(), pick_random_gender())
    print(new_character.image_prompt)
    return new_character

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


def create_random_character_option():
    print("This program will create a number of random characters for you.")
    # Ask for number of characters until valid integer input
    num_characters = input("How many characters do you want to create? ")
    while not num_characters.isdigit():
        num_characters = input("Please enter a number: ")

    num_characters = int(num_characters)
    if num_characters <= 0:
        print("No characters created.")
        exit()
    for _ in range(num_characters):
        new_character = create_random_character()
        characters.append(new_character)
    print(f"Created {len(characters)} characters.")
    # Ask if the user wants to create more characters
    create_more = input("Do you want to create more characters? (y/n) ")
    while create_more.lower() == 'y':
        num_characters = input("How many characters do you want to create? ")
        while not num_characters.isdigit():
            num_characters = input("Please enter a number: ")
            num_characters = int(num_characters)
            if num_characters <= 0:
             print("No characters created.")
             exit()
            for _ in range(num_characters):
                new_character = create_random_character()
                characters.append(new_character)
                print(new_character.image_prompt)
            if num_characters == 1:
                print(f"Created {len(characters)} character.")
            else:
                print(f"Created {len(characters)} characters.")
                create_more = input("Do you want to create more characters? (y/n) ")


# Create a list of unique characters
characters = []
print("Welcome to the RPG Character Generator!")

# Menu
print("1. Create random characters")
print("0. Exit the program")
choice = input("What do you want to do? ")
if choice == "1":
    create_random_character_option()
elif choice == "0":
    print("Goodbye!")
    exit()


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
import os

def get_files_in_folder(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        # Check if the path is a file (not a directory)
        if os.path.isfile(os.path.join(folder_path, file_name)):
            files.append(file_name)
    return files


# Get all the characters with an image in images folder
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
    print(f"There are {len(characters_with_images)} characters with images.")


# Get all the characters without an image in images folder
characters_without_images = []
for character in existing_characters:
    image_name = f"{character.get('id')}.png"
    if image_name not in files_in_folder:
        characters_without_images.append(character)

# Write the characters without images to a JSON file
with open("characters_without_images.json", "w") as json_file:
    json.dump(characters_without_images, json_file, indent=4, default=lambda o: o.__dict__)
    print(f"There are {len(characters_without_images)} characters without images.")

# Create an image for each character without an image
#import create_image
#for character_data in characters_without_images:
#    image_prompt = character.get('image_prompt')
#    image = create_image.create_image(image_prompt, character_data.get('id'))

# Create a list of image prompts of the characters without images
prompts = []
for character_data in characters_without_images:
    image_prompt = character_data.get('image_prompt')
    prompts.append(image_prompt + '\n\n')

# Write the image prompts to a text file
with open('data/characters_without_images.txt', 'w') as file:
    file.writelines(prompts)

