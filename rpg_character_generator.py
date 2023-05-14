import random, json, csv
import requests
from character_settings import character_classes, ethnicity, background, age_settings, gender
from character_class import Character
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

# Create a background story for an RPG character

def fetch_character_data(prompt, api_key):
    url = "https://api.openai.com/v1/engines/text-davinci-002/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "prompt": prompt,
        "max_tokens": 200,
        "n": 1,
        "stop": None,
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from ChatGPT: {response_json}")

    return response_json['choices'][0]['text']


# Create a random character
def random_gender():
    return random.choices(gender, weights=(40, 50, 10))[0]

import random

def pick_random_age():
    age_options = age_settings
    age_weights = [0, 0, 15, 25, 35, 25, 15, 10, 5, 2, 2, 10]  # Adjust the weights based on desired distribution

    random_age = random.choices(age_options, weights=age_weights)[0]
    return random_age


def create_random_character():
    return Character(random.choice(character_classes), random.choice(background), random.choice(ethnicity), pick_random_age(), random_gender(), api_key)

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
        json.dump(characters, json_file, indent=4)


# Create a list of unique characters

characters = []
num_characters = input("How many characters do you want to create? ")

# Exit if 0 or less
if int(num_characters) <= 0:
    print("No characters created.")

    while not num_characters.isdigit():
        num_characters = input("Please enter a number: ")
    num_characters = int(num_characters)
    while len(characters) < num_characters:
        new_character = create_random_character()
        characters.append(new_character)
    print(f"Created {len(characters)} characters.")

# Create a csv file with the characters
with open("data/characters_data.csv", "a", newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=["First Name", "Last Name", "Class", "Background", "Ethnicity", "Age", "Image", "Physical description", "Physical description Text","Background Story", "Image Prompt"])
    if csv_file.tell() == 0:
        csv_writer.writeheader()
    for character in characters:
        csv_writer.writerow({
            "First Name": character.first_name,
            "Last Name": character.last_name,
            "Class": character.character_class,
            "Background": character.background,
            "Ethnicity": character.ethnicity,
            "Age": character.age,
            "Image": character.physical_description.image,
            "Physical description": character.physical_description.__dict__,
            "Physical description Text": character.physical_description_text,
            "Background Story": character.background_story,
            "Image Prompt": character.image_prompt
        })

# Load existing characters from the csv file and convert them to the json file
# Load existing characters from the JSON file
existing_characters = load_characters()
print(len(existing_characters))

# Convert Character instances to dictionaries
character_dicts = [character.__dict__ for character in characters]
print(character_dicts)


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

# Example usage
folder_path = "./static/images/"
files_in_folder = get_files_in_folder(folder_path)

# Get all the characters with an image in images folder
characters_with_images = []
for character in existing_characters:
    image_name = character.get('physical_description').get('image')
    if image_name in files_in_folder:
        characters_with_images.append(character)

# Write the characters with images to a JSON file
with open("characters_with_images.json", "w") as json_file:
    json.dump(characters_with_images, json_file, indent=4, default=lambda o: o.__dict__)
    print(f"There are {len(characters_with_images)} characters with images.")


# Get all the characters without an image in images folder
characters_without_images = []
for character in existing_characters:
    image_name = character.get('physical_description').get('image')
    if image_name not in files_in_folder:
        characters_without_images.append(character)

# Write the characters without images to a JSON file
with open("characters_without_images.json", "w") as json_file:
    json.dump(characters_without_images, json_file, indent=4, default=lambda o: o.__dict__)
    print(f"There are {len(characters_without_images)} characters without images.")

# Create a list of image prompts of the characters without images
prompts = []
for character_data in characters_without_images:
    image_prompt = character_data.get('image_prompt')
    prompts.append(image_prompt + '\n\n')

# Write the image prompts to a text file
with open('data/characters_without_images.txt', 'w') as file:
    file.writelines(prompts)

