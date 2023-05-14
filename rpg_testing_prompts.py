from models.character_class import Character
from settings.image_prompt import craft_image_prompt_illustration
import random
from settings.character_settings import character_classes, background
from settings.random_settings import ethnicity, pick_random_age, pick_random_ethnicity, pick_random_gender
from api_settings import api_key
# Create a random character

def create_random_character(image_type="illustration"):
    return Character(random.choice(character_classes), random.choice(background), random.choice(ethnicity), pick_random_age(), pick_random_gender(), api_key, image_type=image_type)

random_character = create_random_character()

print(craft_image_prompt_illustration(random_character))