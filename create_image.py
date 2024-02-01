import openai
from settings.env_settings import api_key
import requests
openai.api_key = api_key


def create_image(prompt, id):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
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
