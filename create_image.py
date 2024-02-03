from dotenv import load_dotenv
import openai
import requests
import os
# Get the OpenAI API key
# Load .env file
load_dotenv()

# Get the OpenAI API key
api_key = os.environ.get('API_KEY')

def create_image(prompt, id):
    openai.api_key = api_key
    try:
        response = openai.Image.create(
        model="dall-e-3",
        prompt= f"I NEED to test how the tool works with extremely simple prompts. DO NOT add any detail, just use it AS-IS: {prompt}",
        size="1024x1024",
        quality="standard",
        n=1,
        )
        image_url = response['data'][0]['url']

        # Download the image to the static folder
        r = requests.get(image_url, stream=True)

        if r.status_code == 200:
            # Write to file in chunks (better for large files)
            with open(f'static/images/{id}.png', 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        else:
            print(f"Unable to download image. HTTP Status Code: {r.status_code}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
