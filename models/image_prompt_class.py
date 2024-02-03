import random
from create_image import create_image
from settings.image_prompt_settings import colors
from utils.data_utils import pick_random_item
from utils.indefinite_article import indefinite_article
import json
import openai
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# Get the OpenAI API key
api_key = os.environ.get('API_KEY')


def choose_two_and_join(elements):
    choices = random.sample(elements, 2)
    return ' and '.join(str(choice) for choice in choices)


def optimize_prompt(prompt):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            response_format={"type": "text"},
            messages=[
                {"role": "system",
                    "content": "You are a prompt engineer specialized in dall-e."},
                {"role": "user", "content": f"Optimize this prompt for dall-e: {prompt}. Give only the text prompt to use with dall-e, nothing else."},
            ]
        )
        return response.choices[0].message.content

    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None


data_files = ['artists', 'illustrators','accessories', 'angles', 'clothing', 'facial_expressions', 'portraits',
              'genres', 'styles', 'lighting', 'cameras', 'posing']
data = {file: json.load(open(f'data/{file}.json', 'r')) for file in data_files}


class ImagePrompt:
    def __init__(self, character):
        self.character = character
        self.behavior = character.behavior
        self.actor = character.__str__()
        self.portrait_setting = character.background_setting
        self.tags = str(', '.join(self.character.ethnicity_keywords))
        self.tones = ' and '.join(random.sample(colors, 2))
        # Get the description of the artistis style rather than the name
        self.artist = pick_random_item(data, ['illustrators', 'illustrators'], 'description')
        # self.artist = pick_random_item(
        #     data, ['artists', 'artists'], 'description')
        self.style = pick_random_item(data, ['styles', 'styles'], 'name')
        self.lighting = pick_random_item(
            data, ['lighting', 'lighting'], 'name')
        self.clothing = pick_random_item(
            data, ['clothing', 'clothing'], 'name')
        self.portrait = pick_random_item(
            data, ['portraits', 'portraits'], 'name')
        self.camera = pick_random_item(data, ['cameras', 'cameras'], 'name')
        self.angle = pick_random_item(data, ['angles', 'angles'], 'name')
        self.posing = pick_random_item(data, ['posing', 'posing'])
        self.accessories = pick_random_item(
            data, ['accessories', 'accessories'])
        self.facial_expression = pick_random_item(
            data, ['facial_expressions', 'facial_expressions'], 'expression')
        self.genre = pick_random_item(data, ['genres', 'genres'], 'name')

    def craft_image_prompt(self):
        
       
        prompt_properties = {
            'accessories': self.accessories,
            'actor': self.actor,
            'artist': self.artist,
            'behavior': self.behavior,
            'camera': self.camera,
            'clothing': self.clothing,
            'full_name': self.character.full_name,
            'genre': self.genre,
            'lighting': self.lighting,
            'portrait_setting': self.portrait_setting,
            'portrait': self.portrait,
            'posing': self.posing,
            'style': self.style,
            'tags': self.tags,
            'tones': self.tones
        }

        # Now form the prompt string using format_map()
        prompt = "{portrait} in the style of {artist} mixed with {style} | {genre} | {actor} | {behavior} | {full_name} is wearing {clothing} clothing | {tones} tones | {camera} | {posing} | {accessories} | {lighting} | {portrait_setting} | {tags}".format_map(
            prompt_properties)

        # This is the prompt for midjourney
        prompt_midjourney = f"{prompt} , RPG, D&D. --s 1000 --ar 90:160 --seed {self.character.picture_id}"
        # Append prompt to image_prompts.txt
        with open('data/image_prompts.txt', 'a') as f:
            f.write(prompt_midjourney + '\n')
        print(prompt_midjourney)

        # Create the image using the prompt with dall-e
        prompt_dall_e = prompt
        prompt_dall_e = optimize_prompt(prompt_dall_e)

        # Append prompt to image_prompts_dalle.txt
        with open('data/image_prompts_dalle.txt', 'a') as f:
            f.write(prompt_dall_e + '\n')
        print(prompt_dall_e)

        create_image(prompt_dall_e, self.character.picture_id)
        print("Image created successfully.")

        return prompt
