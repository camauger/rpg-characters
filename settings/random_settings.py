import json
import random
from settings.character_settings import gender_settings, age_settings, hair_colors_settings, physical_settings
from utils.data_utils import pick_random_data_from_file


def pick_random_setting(setting):
    return random.choice(setting)


def pick_random_setting_with_weight(setting):
    setting, setting_weights = zip(*setting)
    return random.choices(setting, weights=setting_weights)[0]


def pick_random_gender():
    return pick_random_setting_with_weight(gender_settings)


def pick_random_age():
    return pick_random_setting_with_weight(age_settings)


def pick_random_hair_color():
    return pick_random_setting_with_weight(hair_colors_settings)


def pick_random_physical_trait():
    return pick_random_setting(physical_settings)


def pick_random_background():
    return pick_random_data_from_file('data/background_data.json', 'backgrounds')


def pick_random_ethnicity():
    return pick_random_data_from_file('data/ethnicity_data.json', 'ethnicity')


def pick_random_ethnicity_fantasy():
    return pick_random_data_from_file('data/ethnicity_fantasy_data.json', 'ethnicity')


def pick_random_character_class():
    return pick_random_data_from_file('data/character_classes.json', 'classes')


def pick_random_subclass(character_class):
    return random.choice(character_class['subclasses'])


def create_physical_description():
    with open('data/physical_description.json', 'r') as f:
        physical_description = json.load(f)
    return physical_description


def create_physical_trait():
    return pick_random_physical_trait()


def create_physical_desc_synonym(key):
    data = create_physical_description()
    random_synonym_element = random.choice(data[key])
    random_synonym = random.choice(random_synonym_element['synonyms'])
    return random_synonym.lower()


def create_body_type():
    return create_physical_desc_synonym('body_types')


def create_hair_style():
    return create_physical_desc_synonym('hair_styles')


def create_hair_color():
    return pick_random_hair_color()


def create_eye_color():
    return create_physical_desc_synonym('eye_colors')

import random

def get_ethnicity_keywords(ethnicity):
    # Get keywords from ethnicity
    total_keywords = ethnicity['keywords']
    
    # Pick up to 5 keywords at random
    keyword_count = min(5, len(total_keywords))
    total_keywords = random.sample(total_keywords, keyword_count)

    # return the keywords in a string
    return ', '.join(total_keywords)

