import discord
from discord import SyncWebhook
from discord.ext import commands
import requests
from dotenv import load_dotenv
from PIL import Image
import os
import time
from settings.env_settings import WEB_HOOK, DISCORD_TOKEN
import re

load_dotenv()
bot = commands.Bot(command_prefix="*", intents=discord.Intents.all())
directory = os.getcwd()
print(directory)

def get_seed_number(message):
    match = re.search("--seed (\d+)", message)
    if match:
        return match.group(1)
    else:
        print("No seed number found in message.")
        return ""
        
def get_job_id(file_prefix):
    match = re.search(r"([a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12})$", file_prefix)
    if match:
        return match.group(1)
    else:
        print("No job_id found in file_prefix.")

def split_image(image_file):
    with Image.open(image_file) as im:
        # Get the width and height of the original image
        width, height = im.size
        # Calculate the middle points along the horizontal and vertical axes
        mid_x = width // 2
        mid_y = height // 2
        # Split the image into four equal parts
        top_left = im.crop((0, 0, mid_x, mid_y))
        top_right = im.crop((mid_x, 0, width, mid_y))
        bottom_left = im.crop((0, mid_y, mid_x, height))
        bottom_right = im.crop((mid_x, mid_y, width, height))
        return top_left, top_right, bottom_left, bottom_right

async def download_image(url, filename, upscaled=False):
    response = requests.get(url)
    if response.status_code == 200:

        # Define the input and output folder paths
        input_folder = "input"
        output_folder = "output"

        # Check if the output folder exists, and create it if necessary
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Check if the input folder exists, and create it if necessary
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)
        with open(f"{directory}/{input_folder}/{filename}", "wb") as f:
            f.write(response.content)
        print(f"Image downloaded: {filename}")
        input_file = os.path.join(input_folder, filename)
        if len(filename) < 20:
            #static_folder = "large_images"
            static_folder = "static/images"
            os.rename(f"{directory}/{input_folder}/{filename}", f"{directory}/{static_folder}/{filename}")
        elif upscaled:
            os.rename(f"{directory}/{input_folder}/{filename}", f"{directory}/{output_folder}/{filename}")

        else:
            file_prefix = os.path.splitext(filename)[0]
            file_prefix = get_job_id(file_prefix)
            # Split the image
            top_left, top_right, bottom_left, bottom_right = split_image(input_file)
            # Save the output images with dynamic names in the output folder
            top_left.save(os.path.join(output_folder, file_prefix + "_top_left.jpg"))
            top_right.save(os.path.join(output_folder, file_prefix + "_top_right.jpg"))
            bottom_left.save(os.path.join(output_folder, file_prefix + "_bottom_left.jpg"))
            bottom_right.save(os.path.join(output_folder, file_prefix + "_bottom_right.jpg"))
            # Delete the input file
            os.remove(f"{directory}/{input_folder}/{filename}")

@bot.event
async def on_ready():
    print("Bot connected")

def send_message_to_channel(message):
    webhook = SyncWebhook.from_url(WEB_HOOK)
    webhook.send(f"{message}")

@bot.event
async def on_message(message):
    # If only 1 attachment, download it
    if len(message.attachments) == 1:
        for attachment in message.attachments:
            if get_seed_number(message.content) != "":
                seed = get_seed_number(message.content)
                file_name = f"{seed}.png"
                print(file_name)
            else:
                file_name = f"{attachment.filename}"
            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                await download_image(url=attachment.url, filename=file_name, upscaled=True)
    elif len(message.attachments) > 1:
        for attachment in message.attachments:
            if get_seed_number(message.content) != "":
                seed = get_seed_number(message.content)
                file_name = f"{seed}.png"
                print(file_name)
            else:
                file_prefix = ''
                file_name = f"{file_prefix}{attachment.filename}"
            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                await download_image(url=attachment.url, filename=file_name, upscaled=False)


    # use Discord message to download images from a channel history, example: "history:50"
    if message.content.startswith("history:"):
        download_qty = int(message.content.split(":")[1])
        channel = message.channel
        async for msg in channel.history(limit=download_qty):
            for attachment in msg.attachments:
                if "Upscaled by" in message.content:
                    file_prefix = 'UPSCALED_'
                else:
                    file_prefix = ''
                if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                    try:
                        await download_image(attachment.url, f"{file_prefix}{attachment.filename}")
                    except:
                        time.sleep(10)
                        continue

# Start the bot
def start_discord_bot():
    bot.run(DISCORD_TOKEN)


import shutil
import os

source_dir = './output'
target_dir = './archives'
file_names = os.listdir(source_dir)

def move_files():
    for file_name in file_names:
        shutil.move(os.path.join(source_dir, file_name), target_dir)


