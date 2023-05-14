
# Using ChatGPT
import requests
import json

def fetch_character_data(prompt, api_key):
    url = "https://api.openai.com/v1/engines/text-davinci-002/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "prompt": prompt,
        "max_tokens": 100,
        "n": 1,
        "stop": None,
        "temperature": 0.7,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from ChatGPT: {response_json}")

    return response_json['choices'][0]['text']

# Create a background story for an RPG character

def create_background_story(name, character_class, api_key):
    prompt = f"Create a background story for a RPG character named {name}.\n\nCharacter class: {character_class}"
    background_story = fetch_character_data(prompt, api_key)
    return background_story

