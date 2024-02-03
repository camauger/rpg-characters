import random
from mongoengine import connect
from mongoengine import Document, StringField, IntField, BooleanField, ListField, DictField
from models.character_behavior_class import CharacterBehavior
from models.image_prompt_class import ImagePrompt
from models.physical_description_class import PhysicalDescription
from settings.name_composition import generate_random_first_name, generate_random_last_name
from settings.random_settings import create_eye_color, create_hair_color, create_hair_style, create_physical_trait, get_ethnicity_keywords, pick_random_age, pick_random_background, pick_random_character_class, pick_random_ethnicity, pick_random_gender, pick_random_subclass
from utils.indefinite_article import indefinite_article
import openai
import os
from dotenv import load_dotenv


# Load .env file
load_dotenv()
connect(host=os.environ.get('MONGO_CONNECTION_STRING'))

# Get the OpenAI API key
api_key = os.environ.get('API_KEY')

# Create a background story for an RPG character


def fetch_character_data(prompt):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a RPG character in the world of Forgotten Realms. Write a background story for your character. Include their upbringing, key events in their life, and their motivations. Conclude the background story by including a potential adventure hook or a mystery that the character seeks to unravel. Please write three paragraphs with a total word count of around 300 words. Write output in JSON format."},
                {"role": "user", "content": f"{prompt}"},
            ]
        )
        return response.choices[0].message.content

    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None


def file_exists(folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    return os.path.exists(file_path)


class Character(Document):
    # Basic character information
    id = IntField(primary_key=True)
    first_name = StringField()
    last_name = StringField()
    full_name = StringField()
    gender = StringField()

    # Character class and subclass information
    character_class = DictField()
    character_class_id = StringField()
    character_class_name = StringField()
    character_subclass = DictField()
    character_subclass_name = StringField()
    character_subclass_id = StringField()

    # Background information
    background = DictField()
    background_id = StringField()
    background_name = StringField()
    background_setting = StringField()

    # Ethnicity and subrace information
    ethnicity = DictField()
    ethnicity_id = StringField()
    ethnicity_keywords = ListField(StringField())
    ethnicity_name = StringField()

    # Other character attributes
    age = StringField()
    background_story = StringField()
    behavior = StringField()
    eye_color = StringField()
    hair_color = StringField()
    hair_style = StringField()
    has_image = BooleanField(default=False)
    image_prompt = StringField()
    personality_description = StringField()
    physical_description = DictField()
    physical_trait = StringField()
    picture_id = StringField()

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return data

    def update_has_image(self):
        self.has_image = file_exists('static/images', f"{self.picture_id}.png")

    def create_picture_id(self):
        # Use a dictionary to map genders to IDs
        gender_map = {'Male': '1', 'Female': '0'}
        
        # Create the ID components with conditional expressions 
        ids = [
            gender_map.get(self.gender, '2') if self.gender else '',
            self.ethnicity_id or '',
            self.character_subclass_id or self.character_class_id or '',
            self.background_id or '',
            str(self.id) or ''
        ]
        ids = ''.join(ids)
        if ids == '':
            ids = random.randint(1, 9999)
        

        # Join all the IDs into one string
        return ids



    def create_physical_description_text(self):
        physical_description = f"{indefinite_article(self.physical_trait)} {self.gender.lower()} {self.ethnicity_name}. {self.full_name} has {self.hair_color.lower()} {self.hair_style} hair and {self.eye_color} eyes"
        return f"{self.full_name} is {physical_description}."

    def create_physical_description(self):
        return PhysicalDescription()

    def create_background_story(self):
        prompt = f"Write a background story for an RPG character named {self.full_name}, a {self.character_class} in the world of Forgotten Realms. The character is a {self.background_name} with {self.ethnicity} heritage. Describe their upbringing, key events in their life, and their motivations. Please write three paragraphs with a total word count of around 300 words. Conclude the background story by including a potential adventure hook or a mystery that the character seeks to unravel."
        background_story = fetch_character_data(prompt)
        return background_story

    def create_behavior(self):
        behavior = CharacterBehavior(character=self)
        behavior_text = behavior.create_behavior()
        return behavior_text

    def create_personality_description(self):
        prompt = f"Make a description of a character's personality based on this sentence: {self.behavior}"
        personality = fetch_character_data(prompt)
        return personality

    def create_image_prompt(self):
        image_prompt = ImagePrompt(character=self)
        prompt = image_prompt.craft_image_prompt()
        print(prompt)
        return prompt

    def create_character(self, params, is_random=False):
        # Simplified the code here
        if is_random:
            self.gender = pick_random_gender()
            self.first_name = generate_random_first_name(self.gender)
            self.last_name = generate_random_last_name()
        else:
            self.first_name = params.get("first_name", "")
            self.last_name = params.get("last_name", "")

        self.full_name = f"{self.first_name} {self.last_name}"

        # Additional fields could be set here similarly, example:
        self.id = int(random.randint(1, 9999)),
        self.character_class = pick_random_character_class()
        self.character_class_id = self.character_class['id']
        self.character_class_name = self.character_class['name']
        self.character_subclass = pick_random_subclass(self.character_class)
        self.character_subclass_id = self.character_subclass['id']
        self.character_subclass_name = self.character_subclass['name']

        # Background
        self.background = pick_random_background()
        self.background_id = self.background['id']
        self.background_name = self.background['name']
        self.background_setting = self.background['setting']
        self.background_story = self.create_background_story()

        # Traits
        self.age = pick_random_age( )
        self.physical_trait = create_physical_trait()
        self.hair_color = create_hair_color()
        self.hair_style = create_hair_style()
        self.eye_color = create_eye_color()
        self.behavior = self.create_behavior()
        self.image_prompt = self.create_image_prompt()
        self.personality_description = self.create_personality_description()

        # Race
        self.ethnicity = pick_random_ethnicity()
        self.ethnicity_id = self.ethnicity['id']
        self.ethnicity_name = self.ethnicity['name']
        self.ethnicity_keywords = get_ethnicity_keywords(
            self.ethnicity)
        
        # Image
        self.picture_id = self.create_picture_id()
        self.update_has_image()
        

        return self

    def description(self):
        return f"{self.full_name} is a {self.gender} {self.ethnicity_name} {self.character_class_name} ({self.character_subclass_name}) and a {self.background_name}"

    # Duplicate but to test
    def __str__(self):
        return f"{self.full_name} is a {self.gender} {self.ethnicity_name} {self.character_class_name} ({self.character_subclass_name}) and a {self.background_name}"

     


