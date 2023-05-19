from models.character_behavior_class import CharacterBehavior
from models.physical_description_class import PhysicalDescription
from models.image_prompt_class import ImagePrompt
from settings.name_composition import generate_random_first_name, generate_random_last_name
from settings.random_settings import create_eye_color, create_hair_color, create_hair_style, create_physical_trait
import requests
import json
from utils.indefinite_article import indefinite_article
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
        "max_tokens": 400,
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
    def __init__(self, id, params):
        self.id = id
        self.first_name = generate_random_first_name(params['gender'])
        self.last_name = generate_random_last_name()
        self.full_name = f"{self.first_name} {self.last_name}"
        self.gender = params['gender']
        self.character_class = params['random_class'].get('name')
        self.character_subclass = params['random_subclass']
        self.background = params['background']
        self.ethnicity = params['random_ethnicity'].get('race')
        self.ethnicity_keywords = params['ethnicity_keywords']
        self.age = params['age']
        self.physical_description = self.create_physical_description()
        self.physical_trait = create_physical_trait()
        self.hair_color = create_hair_color()
        self.hair_style = create_hair_style()
        self.eye_color = create_eye_color()
        self.behavior = self.create_behavior()
        self.image_prompt = self.create_image_prompt()
        # Has to be last!
        self.personality_description = self.create_personality_description()
        self.background_story = self.create_background_story()


    def create_physical_description_text(self):
        physical_description = f"{indefinite_article(self.physical_trait)} {self.gender.lower()} {self.ethnicity}. {self.full_name} has {self.hair_color.lower()} {self.hair_style} hair and {self.eye_color} eyes"
        return f"{self.full_name} is {physical_description}."

    def create_physical_description(self):
        return PhysicalDescription()

    def create_background_story(self):
        prompt = f"Create a background story for a RPG character named {self.full_name} who is {indefinite_article(self.background)} {self.character_class} in the world of Forgotten Realms. {self.behavior} - Make it 3 paragraphs. Make the story no longer than 200 words. End the background story with a potential adventure hook."
        background_story = fetch_character_data(prompt, api_key)
        # Transform the /n in paragraphs into <br> for HTML
        ## background_story = background_story.replace('\n\n', '<br>')
        return background_story

    def create_behavior(self):
        behavior = CharacterBehavior(character=self)
        behavior_text = behavior.create_behavior()
        return behavior_text

    def create_personality_description(self):
        prompt = f"Make a description of a character's personality based on this sentence: {self.behavior}"
        personality = fetch_character_data(prompt, api_key)
        return personality
    
    def create_image_prompt(self):
        image_prompt = ImagePrompt(character=self)
        prompt = image_prompt.craft_image_prompt()
        return prompt
    
    def __str__(self):
        return f"{self.full_name} is a {self.ethnicity} {self.character_class} ({self.character_subclass}) and a {self.background}"
