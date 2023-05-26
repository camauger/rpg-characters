from models.character_behavior_class import CharacterBehavior
from models.physical_description_class import PhysicalDescription
from models.image_prompt_class import ImagePrompt
from settings.name_composition import generate_random_first_name, generate_random_last_name
from settings.random_settings import create_eye_color, create_hair_color, create_hair_style, create_physical_trait, get_ethnicity_keywords
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

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()

        if response.status_code == 200:
            return response_json['choices'][0]['text']
        else:
            raise Exception(f"Failed to fetch data from ChatGPT: {response_json}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error occurred during API request: {e}")

    except (KeyError, IndexError) as e:
        raise Exception(f"Invalid response received from ChatGPT: {e}")

"""
This code is defining a class called Character.

The __init__ method is used to initialize the class with various parameters such as character_class, background, ethnicity, age, gender, api_key, and image_type.

It also assigns each instance of the class a unique id, generates a random first and last name, and creates a full name for the character.

Additionally, it creates physical and psychological descriptions for the character, as well as a background story.

Finally, the __str__ method is used to return a string representation of the character.
"""
import os
def file_exists(folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    return os.path.exists(file_path)
class Character:
    def __init__(self, character_id, params):
        # Initialize the Character object with the provided ID and parameters
        try:
            # Assign basic character information
            self.id = character_id
            self.first_name = generate_random_first_name(params['gender'])
            self.last_name = generate_random_last_name()
            self.full_name = f"{self.first_name} {self.last_name}"
            self.gender = params['gender']
        
            # Assign character class information
            random_class = params.get('random_class', {})
            self.character_class = random_class.get('name')
            self.character_class_id = random_class.get('id')

            # Assign character subclass information
            random_subclass = params.get('random_subclass', {})
            self.character_subclass = random_subclass.get('name')
            self.character_subclass_id = random_subclass.get('id')
        
            # Assign background information
            self.background = params.get('background', {})
            self.background_name = self.background.get('name')
            self.background_id = self.background.get('id')

            # Assign ethnicity information
            random_ethnicity = params.get('random_ethnicity', {})
            self.ethnicity = random_ethnicity.get('race')
            self.ethnicity_name = random_ethnicity.get('race')
            self.ethnicity_id = random_ethnicity.get('id')

            # Assign subrace information
            self.subrace = params.get('random_subrace', {})
            self.subrace_name = self.subrace.get('name', '')
            self.subrace_id = self.subrace.get('id', '')
        
            # Assign ethnicity keywords
            self.ethnicity_keywords = get_ethnicity_keywords(random_ethnicity, self.subrace)
            
            # Assign other character attributes
            self.age = params.get('age')
            self.physical_description = self.create_physical_description()
            self.physical_trait = create_physical_trait()
            self.hair_color = create_hair_color()
            self.hair_style = create_hair_style()
            self.eye_color = create_eye_color()
            self.behavior = self.create_behavior()
            self.picture_id = self.create_picture_id()
            self.image_prompt = self.create_image_prompt()
            self.personality_description = self.create_personality_description()
            self.background_story = self.create_background_story()

            self.has_image = file_exists('static/images', f"{self.picture_id}.png")
            
        
        except (KeyError, TypeError) as e:
           raise Exception(f"Invalid parameter format: {e}")

    def to_dict(self):
        """Convert the character object to a dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'gender': self.gender,
            'character_class': self.character_class,
            'character_class_id': self.character_class_id,
            'character_subclass': self.character_subclass,
            'character_subclass_id': self.character_subclass_id,
            'background': self.background,
            'background_name': self.background_name,
            'background_id': self.background_id,
            'ethnicity': self.ethnicity,
            'ethnicity_name': self.ethnicity_name,
            'ethnicity_id': self.ethnicity_id,
            'subrace': self.subrace,
            'subrace_name': self.subrace_name,
            'subrace_id': self.subrace_id,
            'ethnicity_keywords': self.ethnicity_keywords,
            'age': self.age,
            'physical_description': {
                'trait': self.physical_trait,
                'hair_color': self.hair_color,
                'hair_style': self.hair_style
            },
            'physical_trait': self.physical_trait,
            'hair_color': self.hair_color,
            'hair_style': self.hair_style,
            'eye_color': self.eye_color,
            'behavior': self.behavior,
            'picture_id': self.picture_id,
            'image_prompt': self.image_prompt,
            'personality_description': self.personality_description,
            'background_story': self.background_story,
            'has_image': self.has_image
        }
    
    def update_has_image(self):
        self.has_image = file_exists('static/images', f"{self.picture_id}.png")


    def get_subrace_name(self):
        if self.subrace is not None:
            return self.subrace['name']
        else:
            return ''

    def create_picture_id(self):
        gender_id = ""
        if self.gender == 'Male':
            gender_id = '1'
        elif self.gender == 'Female':
            gender_id = '0'
        else:
            gender_id = '2'            

        race_id = ""
        if self.subrace is not None and len(self.subrace_id) > 0:
            race_id = self.subrace_id
        elif self.ethnicity_id and len(self.ethnicity_id) > 0:
            race_id = self.ethnicity_id
        else:
            race_id = ''

        class_id = ""
        if self.character_subclass_id and len(self.character_subclass_id) > 0:
            class_id = self.character_subclass_id
        elif self.character_class_id and len(self.character_class_id) > 0:
            class_id = self.character_class_id
        else:
            class_id = ''

        return (gender_id or '') + (race_id) + (class_id) + (self.background_id or '') + str(self.id)


    def create_physical_description_text(self):
        physical_description = f"{indefinite_article(self.physical_trait)} {self.gender.lower()} {self.ethnicity}. {self.full_name} has {self.hair_color.lower()} {self.hair_style} hair and {self.eye_color} eyes"
        return f"{self.full_name} is {physical_description}."

    def create_physical_description(self):
        return PhysicalDescription()

    def create_background_story(self):
        prompt = f"Write a background story for an RPG character named {self.full_name}, a {self.character_class} in the world of Forgotten Realms. The character is a {self.background_name} with {self.ethnicity} heritage. Describe their upbringing, key events in their life, and their motivations. Please write three paragraphs with a total word count of around 300 words. Conclude the background story by including a potential adventure hook or a mystery that the character seeks to unravel."
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

