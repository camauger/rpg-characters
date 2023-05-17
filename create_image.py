import openai
from api_settings import api_key
import requests
openai.api_key = api_key


def create_image(prompt, id):
  response = openai.Image.create(
  prompt=prompt,
  n=1,
  size="1024x1024"
)
  image_url = response['data'][0]['url']
  # download the image to the static folder
  r = requests.get(image_url, allow_redirects=True)
  open(f'static/images/{id}.png', 'wb').write(r.content)



