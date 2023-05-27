import requests
import json
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the API key
key = os.environ.get("STABLE_API_KEY")

def create_image_stable_diffusion(prompt, picture_id):
    url = "https://stablediffusionapi.com/api/v3/text2img"
    key = os.environ.get("STABLE_API_KEY")
    payload = json.dumps({
        "key": f"{key}",
        "prompt": f"{prompt}",
        "negative_prompt": "((out of frame)), ((extra fingers)), mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), (((tiling))), ((naked)), ((tile)), ((fleshpile)), ((ugly)), (((abstract))), blurry, ((bad anatomy)), ((bad proportions)), ((extra limbs)), cloned face, (((skinny))), glitchy, ((extra breasts)), ((double torso)), ((extra arms)), ((extra hands)), ((mangled fingers)), ((missing breasts)), (missing lips), ((ugly face)), ((fat)), ((extra legs)), anime",
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "seed": None,
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "embeddings_model": "embeddings_model_id",
        "webhook": None,
        "track_id": None
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    # Get the URL of the image
    image_url = response.json()['output'][0].replace("\\", "")  # Remove backslashes

    # Download the image
    image_response = requests.get(image_url)

    # Save the image to a file
    with open(f"./static/images/{picture_id}.png", 'wb') as f:
        f.write(image_response.content)


def create_image_stable_diffusion_dreambooth(prompt, picture_id):
    url = "https://stablediffusionapi.com/api/v3/dreambooth"
    key = os.environ.get("STABLE_API_KEY")
    payload = json.dumps({
    "key": f"{key}",
    "model_id": "midjourney",
    "prompt": f"{prompt}",
    "negative_prompt": "",
    "width": "1024",
    "height": "1024",
    "samples": "1",
    "num_inference_steps": "30",
    "safety_checker": "no",
    "enhance_prompt": "no",
    "upscale": "no",
    "guidance_scale": 7.5
})

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    # Get the URL of the image
    image_url = response.json()['output'][0].replace("\\", "")  # Remove backslashes

    # Download the image
    image_response = requests.get(image_url)

    # Save the image to a file
    with open(f"./static/images/{picture_id}.png", 'wb') as f:
        f.write(image_response.content)