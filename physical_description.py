# Create the physical description of the character
import json
import random

def create_physical_description():
    with open('data/physical_description.json', 'r') as f:
        physical_description = json.load(f)
    return physical_description

# Create the character's body type
def create_body_type():
    with open('data/physical_description.json', 'r') as f:
        # Load the JSON string into a Python dictionary
        data = json.load(f)

       # Get a random body type
        random_body_type = random.choice(data['body_types'])

        # Get a random synonym of the body type
        random_synonym = random.choice(random_body_type['synonyms'])
        return random_synonym.lower()


# Create the character's hair color
def create_hair_color():
    with open('data/physical_description.json', 'r') as f:
        # Load the JSON string into a Python dictionary
        data = json.load(f)

       # Get a random hair color
        random_hair_color = random.choice(data['hair_colors'])

        # Get a random synonym of the hair color
        random_synonym = random.choice(random_hair_color['synonyms'])
        return random_synonym.lower()


# Create the character's hair style
def create_hair_style():
    with open('data/physical_description.json', 'r') as f:
        # Load the JSON string into a Python dictionary
        data = json.load(f)

       # Get a random hair style
        random_hair_style = random.choice(data['hair_styles'])

        # Get a random synonym of the hair style
        random_synonym = random.choice(random_hair_style['synonyms'])
        return random_synonym.lower()

# Create the character's eye color
def create_eye_color():
    with open('data/physical_description.json', 'r') as f:
        # Load the JSON string into a Python dictionary
        data = json.load(f)

       # Get a random eye color
        random_eye_color = random.choice(data['eye_colors'])

        # Get a random synonym of the eye color
        random_synonym = random.choice(random_eye_color['synonyms'])
        return random_synonym.lower()


# Create a sentence with the character's physical description
def create_physical_description_sentence(age = "Young", gender="Male", ethnicity="Human", name="Bob"):
    return f"{name} is a {age} {gender} {ethnicity} with a {create_body_type()} body type. {name} has {create_hair_color()} {create_hair_style()} hair and {create_eye_color()} eyes."


# Create a class object for the character's physical description
class PhysicalDescription:
    def __init__(self, character):
        self.age = character.age
        self.body_type = create_body_type()
        self.hair_color = create_hair_color()
        self.hair_style = create_hair_style()
        self.eye_color = create_eye_color()
        self.gender = character.gender
        self.ethnicity = character.ethnicity
        self.name = character.full_name
        self.image = f"{character.id}.jpg"
  