from create_image import create_image
from dotenv import load_dotenv
from models.character_behavior_class import CharacterBehavior
from models.clothing_class import Clothing
from models.physical_description_class import PhysicalDescription
from mongoengine import connect
from mongoengine import Document, StringField, BooleanField, DictField
from settings.image_prompt_settings import colors
from settings.name_composition import generate_random_first_name, generate_random_last_name
from settings.random_settings import create_eye_color, create_hair_color, create_hair_style, create_physical_trait, get_ethnicity_keywords, pick_random_age, pick_random_background, pick_random_character_class, pick_random_ethnicity, pick_random_gender, pick_random_subclass
from utils.data_utils import pick_random_item
from utils.indefinite_article import indefinite_article
import json
import openai
import os
import random


# Load environment variables
load_dotenv()

# Connect to MongoDB
connect(host=os.environ.get('MONGO_CONNECTION_STRING'))

# Get the OpenAI API key
api_key = os.environ.get('API_KEY')




class Character(Document):
    meta = {'collection': 'characters'}

    # Basic character information
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
    ethnicity_keywords = StringField()
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

    # Image prompt attributes
    description = StringField()
    accessories = StringField()
    artist = StringField()
    camera = StringField()
    clothing = StringField()
    facial_expression = StringField()
    genre = StringField()
    lighting = StringField()
    portrait = StringField()
    posing = StringField()
    style = StringField()
    tones = StringField()
    image_prompt = StringField()

    def to_dict(self):
        data = self.to_mongo().to_dict()
        return data

    def update_has_image(self):
        self.has_image = file_exists('static/images', f"{self.picture_id}.png")

    def create_picture_id(self):
        return self.full_name.replace(" ", "_").lower()

 

   



    def assign_random_clothing(self):
        clothing_items = list(Clothing.objects)  # Fetch all clothing items
        if clothing_items:
            selected_clothing = random.choice(
                clothing_items)  # Randomly select one
            # Assign the clothing name to the character
            self.clothing = selected_clothing.name

   
