import random, json
from settings.character_settings import gender_settings, age_settings, ethnicity_settings, hair_colors_settings, background_settings, physical_settings


def pick_random_setting(setting):
    setting, setting_weights = zip(*setting)
    return random.choices(setting, weights=setting_weights)[0]

def pick_random_gender():
    return pick_random_setting(gender_settings)

def pick_random_background():
    with open('data/background_data.json', 'r') as f:
    # Load the JSON string into a Python dictionary
        data = json.load(f)
        return random.choice(data['backgrounds'])

def pick_random_age():
    age, age_weights = zip(*age_settings)
    return random.choices(age, weights=age_weights)[0]

def pick_random_ethnicity():
    ethnicity, ethnicity_weights= zip(*ethnicity_settings)
    return random.choices(ethnicity, weights=ethnicity_weights)[0]

def pick_random_hair_color():
    hair_color, hair_weights= zip(*hair_colors_settings)
    return random.choices(hair_color, weights=hair_weights)[0]

def pick_random_physical_trait():
    return random.choice(physical_settings)


# Pick a random ethnicity
def pick_random_ethnicity():
    with open('data/ethnicity_data.json', 'r') as f:
        # Load the JSON string into a Python dictionary
        data = json.load(f)
        random_race = random.choice(data['ethnicity'])
        return random_race

def get_ethnicity_keywords(ethnicity, subrace):
    return ethnicity['keywords'] + subrace['keywords']

def pick_random_subrace(race):
    # If race has no subrace
    if race.get('subraces') is None:
        return race
    return random.choice(race['subraces'])


# Pick a random class
def pick_random_character_class():
    with open('data/character_classes.json', 'r') as f:
        # Load the JSON string into a Python dictionary
        data = json.load(f)
        random_class = random.choice(data['classes'])
        return random_class

def pick_random_subclass(character_class):
    return random.choice(character_class['subclasses'])


def create_physical_description():
    with open('data/physical_description.json', 'r') as f:
        physical_description = json.load(f)
    return physical_description


# Create a physical trait of the character
def create_physical_trait():
    return pick_random_physical_trait()

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
    return pick_random_hair_color()


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