import requests
import json
from api_settings import api_key
# Create a background story for an RPG character

def fetch_character_data(prompt, api_key):
    url = "https://api.openai.com/v1/engines/text-davinci-002/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "prompt": prompt,
        "max_tokens": 200,
        "n": 1,
        "stop": None,
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from ChatGPT: {response_json}")

    return response_json['choices'][0]['text']

class BackgroundStory():
    def __init__(self, character):
        self.character = character

    def create_background_story(self):
        prompt = f"Create a background story for a RPG character named {self.character.full_name} who is a {self.character.background} {self.character.character_class} in the world of Forgotten Realms. {self.character.physical_description_text} {self.character.psychological_description} Make the story no longer than 200 words."
        background_story = fetch_character_data(prompt, api_key)
        return background_story
    