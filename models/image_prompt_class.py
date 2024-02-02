import random
from create_image import create_image
from settings.image_prompt_settings import artists_and_photographers, colors, illustrators, lighting, portrait, artists
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

# duplicate of fetch_character_data


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
        # print(response.choices[0].message.content)
        return response.choices[0].message.content

    except openai.error.OpenAIError as e:
        print(f"An error occurred: {e}")
        return None

# Create a class object for the character's image prompt


class ImagePrompt:
    def __init__(self, character):

        # Open the data
        with open('data/accessories.json', 'r') as f:
            self.accessories_data = json.load(f)
        
        with open('data/angles.json', 'r') as f:
            self.angles_data = json.load(f)

        with open('data/clothing.json', 'r') as f:
            self.clothing_data = json.load(f)

        self.character = character
        self.genre = self.genre()
        self.emotion = self.character.behavior
        self.ethnicity = self.character.ethnicity_name
        self.background = self.character.background_name
        self.portrait_setting = self.character.background_setting
        self.scene = self.scene()
        self.tones = self.tones()
        self.artist = self.artist()
        self.style = self.style()
        self.tags = self.tags()
        self.actor = self.actor()
        self.lighting = self.lighting()
        self.clothing = self.clothing()
        self.image_type = self.image_type()
        self.camera = self.camera()
        self.angle = self.angle()
        self.posing = self.posing()
        self.accessories = self.accessories()

    def genre(self):
        with open('data/genres.json', 'r') as f:
            genres = json.load(f)

        # Extract the 'name' from each item in the 'genres' list
        genre_names = [item['name'] for item in genres['genres']]

        # Return a random 'name'
        return random.choice(genre_names)

    def scene(self):
        return f"{indefinite_article(self.background)} {self.ethnicity} {self.character.character_class} named {self.character.full_name}"

    def tones(self):
        return choose_two_and_join(colors)

    def artist(self):
        return random.choice(artists_and_photographers + illustrators + artists)

    def style(self):
        with open('data/styles.json', 'r') as f:
            art_styles = json.load(f)

        # Extract the 'name' from each item in the 'art_styles' list
        style_names = [item['name'] for item in art_styles['styles']]

        # Return a random 'name'
        return random.choice(style_names)

    def tags(self):
        keywords = ', '.join(self.character.ethnicity_keywords)
        return f"{keywords}"

    def actor(self):
        return f"{self.character.create_physical_description_text()}"

    def lighting(self):
        with open('data/lighting.json', 'r') as f:
            lighting_data = json.load(f)

        # Extract the 'name' from each item in the 'lighting' list
        lighting_names = [item['name'] for item in lighting_data['lighting']]

        # Return a random 'name'
        return random.choice(lighting_names)

    def camera(self):
        with open('data/cameras.json', 'r') as f:
            cameras_data = json.load(f)

        # Extract the 'name' from each item in the 'cameras' list
        cameras_names = [item['name'] for item in cameras_data['cameras']]

        # Return a random 'name'
        return random.choice(cameras_names)

    def posing(self):
        with open('data/posing.json', 'r') as f:
            posing_data = json.load(f)

        # Extract the 'name' from each item in the 'posing' list
        posing_names = [item for item in posing_data['posing']]

        # Return a random 'name'
        return random.choice(posing_names)

    def clothing(self):
        clothing_names = [item['name'] for item in self.clothing_data['clothing']]
        return random.choice(clothing_names)

    def accessories(self):
        return random.choice(self.accessories_data['accessories'])

    def image_type(self):
        return random.choice(portrait)
    
    #TODO: Not used for now
    def angle(self):
        angles_names = [item['name'] for item in self.angles_data['angles']]
        return random.choice(angles_names)

    def craft_image_prompt(self):
        #General prompt
        prompt = f"{self.image_type} in the style of {self.artist} and {self.style} | {self.genre} | {self.actor} | {self.character.full_name} is wearing {self.clothing} clothing | {self.tones} tones | {self.camera} | {self.posing} | {self.accessories} | {self.lighting} | {self.portrait_setting} | {self.tags}"


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
