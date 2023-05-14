import random, json
from settings.character_settings import gender_settings, age_settings, ethnicity_settings, hair_colors_settings, background_settings


def pick_random_setting(setting):
    setting, setting_weights = zip(*setting)
    return random.choices(setting, weights=setting_weights)[0]

def pick_random_gender():
    return pick_random_setting(gender_settings)

def pick_random_background():
    return random.choic(background_settings)

def pick_random_age():
    age, age_weights = zip(*age_settings)
    return random.choices(age, weights=age_weights)[0]

def pick_random_ethnicity():
    ethnicity, ethnicity_weights= zip(*ethnicity_settings)
    return random.choices(ethnicity, weights=ethnicity_weights)[0]

def pick_random_hair_color():
    hair_color, hair_weights= zip(*hair_colors_settings)
    return random.choices(hair_color, weights=hair_weights)[0]

# Pick a random class
def pick_random_character_class():
    with open('data/character_classes.json', 'r') as f:
        # Load the JSON string into a Python dictionary
        data = json.load(f)
        random_character_class = random.choice(data['classes'])
        return random_character_class

       