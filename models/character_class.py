from models.character_behavior_class import CharacterBehavior
from settings.image_prompt import craft_image_prompt
from settings.name_composition import generate_random_first_name, generate_random_last_name
from settings.random_settings import create_eye_color, create_hair_color, create_hair_style, create_physical_trait
import random
import requests
import json
from api_settings import api_key
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

"""
This code is defining a class called Character.

The __init__ method is used to initialize the class with various parameters such as character_class, background, ethnicity, age, gender, api_key, and image_type.

It also assigns each instance of the class a unique id, generates a random first and last name, and creates a full name for the character.

Additionally, it creates physical and psychological descriptions for the character, as well as a background story.

Finally, the __str__ method is used to return a string representation of the character.
"""
class Character:
    def __init__(self, character_class, character_subclass, background, ethnicity, age, gender):
        self.id = random.randint(1, 1000)
        self.first_name = generate_random_first_name(gender)
        self.last_name = generate_random_last_name()
        self.full_name = f"{self.first_name} {self.last_name}"
        self.gender = gender
        self.character_class = character_class
        self.character_subclass = character_subclass
        self.background = background
        self.ethnicity = ethnicity
        self.age = age
        self.physical_trait = create_physical_trait()
        self.hair_color = create_hair_color()
        self.hair_style = create_hair_style()
        self.eye_color = create_eye_color()
        self.behavior = self.create_behavior()
        self.image_prompt = self.create_image_prompt()
        # Has to be last!
        self.background_story = self.create_background_story()

    def create_physical_description(self):
        return f"{self.full_name} is a {self.physical_trait} {self.gender} {self.ethnicity}. {self.full_name} has {self.hair_color} {self.hair_style} hair and {self.eye_color} eyes."


    def create_background_story(self):
        prompt = f"Create a background story for a RPG character named {self.full_name} who is a {self.background} {self.character_class} in the world of Forgotten Realms. {self.behavior} Make the story no longer than 200 words."
        background_story = fetch_character_data(prompt, api_key)
        return background_story

    def create_behavior(self):
        return CharacterBehavior().__str__()

    def create_image_prompt(self):
        return craft_image_prompt(self)
    
    def __str__(self):
        return f"{self.full_name} is a {self.ethnicity} {self.character_class} ({self.character_subclass}) and a {self.background}"
