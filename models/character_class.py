from mongoengine import connect
from mongoengine import Document, StringField, IntField, BooleanField, ListField, DictField
from models.character_behavior_class import CharacterBehavior
from models.physical_description_class import PhysicalDescription
from models.image_prompt_class import ImagePrompt
from settings.name_composition import generate_random_first_name, generate_random_last_name
from settings.random_settings import create_eye_color, create_hair_color, create_hair_style, create_physical_trait, get_ethnicity_keywords, pick_random_background, pick_random_character_class, pick_random_ethnicity, pick_random_gender, pick_random_subclass, pick_random_subrace
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
    return ""
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
        # print(response.choices[0].message.content)
        return response.choices[0].message.content

    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None


def file_exists(folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    return os.path.exists(file_path)


class Character(Document):
    # Basic character information
    id = IntField(required=True, primary_key=True)
    first_name = StringField()
    last_name = StringField()
    full_name = StringField()
    gender = StringField()

    # Character class and subclass information
    character_class = DictField()
    character_class_id = StringField()
    character_subclass = DictField()
    character_subclass_id = StringField()

    # Background information
    background = DictField()
    background_name = StringField()
    background_setting = StringField()
    background_id = StringField()

    # Ethnicity and subrace information
    ethnicity = DictField()
    ethnicity_name = StringField()
    ethnicity_id = StringField()
    subrace = DictField()
    subrace_name = StringField()
    subrace_id = StringField()
    ethnicity_keywords = ListField(StringField())

    # Other character attributes
    age = StringField()
    physical_description = DictField()
    physical_trait = StringField()
    hair_color = StringField()
    hair_style = StringField()
    eye_color = StringField()
    behavior = StringField()
    picture_id = StringField()
    image_prompt = StringField()
    personality_description = StringField()
    background_story = StringField()
    has_image = BooleanField(default=False)

    def to_dict(self):
        data = self.to_mongo().to_dict()
        if self.subrace:
            data['subrace_name'] = self.get_subrace_name()
            data['subrace_id'] = self.subrace_id
        return data

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
        background_story = "" if self.simplified else fetch_character_data(
            prompt)
        # Transform the /n in paragraphs into <br> for HTML
        # background_story = background_story.replace('\n\n', '<br>')
        return background_story

    def create_behavior(self):
        behavior = CharacterBehavior(character=self)
        behavior_text = behavior.create_behavior()
        return behavior_text

    def create_personality_description(self):
        prompt = f"Make a description of a character's personality based on this sentence: {self.behavior}"
        personality = fetch_character_data(prompt)
        # personality = "" if self.simplified else fetch_character_data(prompt)
        return personality

    def create_image_prompt(self):
        image_prompt = ImagePrompt(character=self)
        prompt = image_prompt.craft_image_prompt()
        print(prompt)
        return prompt

    def create_character(self, params, is_random=False):
        if is_random:
            self.first_name = generate_random_first_name()
            self.last_name = generate_random_last_name()
            self.full_name = f"{self.first_name} {self.last_name}"
        else:
            self.first_name = params.get('first_name', '')
            self.last_name = params.get('last_name', '')
            self.full_name = f"{self.first_name} {self.last_name}"

        # Additional fields could be set here similarly, example:
        self.gender = params.get(
            'gender', '') if not is_random else pick_random_gender()
        self.character_class = params.get(
            'character_class', '') if not is_random else pick_random_character_class()
        self.character_subclass = params.get(
            'character_subclass', '') if not is_random else pick_random_subclass(self.character_class)
        self.background = params.get(
            'background', '') if not is_random else pick_random_background()
        self.physical_trait = create_physical_trait()
        self.hair_color = create_hair_color()
        self.hair_style = create_hair_style()
        self.eye_color = create_eye_color()
        self.behavior = self.create_behavior()
        self.background_story = self.create_background_story()
        self.image_prompt = self.create_image_prompt()
        self.personality_description = self.create_personality_description()
        self.picture_id = self.create_picture_id()
        self.update_has_image()
        self.ethnicity = pick_random_ethnicity()
        self.subrace = pick_random_subrace(self.ethnicity)
        self.ethnicity_keywords = get_ethnicity_keywords(
            self.ethnicity, self.subrace)
        return self

    def __str__(self):
        return f"{self.full_name} is a {self.ethnicity} {self.character_class} ({self.character_subclass}) and a {self.background}"

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
            'background_setting': self.background_setting,
            'background_id': self.background_id,
            'ethnicity': self.ethnicity,
            'ethnicity_name': self.ethnicity_name,
            'ethnicity_id': self.ethnicity_id,
            'subrace': self.subrace,
            'subrace_name': self.subrace_name if self.subrace is not None else '',
            'subrace_id': self.subrace_id if self.subrace is not None else '',
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
