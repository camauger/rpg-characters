import json
import threading
from flask import Flask, render_template, request, redirect, url_for
import discord
from discord.ext import commands
from models.character_manager_class import CharacterManager
from api_settings import discord_token
import os

def file_exists(folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    return os.path.exists(file_path)

# Flask App
app = Flask(__name__, static_folder='static', static_url_path='/static')
character_manager = CharacterManager()

def get_character_data(picture_id):
    characters = load_characters()
    for character in characters:
        if character.get('picture_id') == picture_id:
            return character
    return None


def load_characters():
    with open('characters.json', 'r') as f:
        characters = json.load(f)
    return characters

# Route for the home page
@app.route('/')
def index():
    characters = load_characters()
    return render_template('index.html', characters=characters)


# Route for the about page
@app.route('/about.html')
def about():
    # Render the template
    return render_template('about.html')

# Route for individual character based on ID
@app.route('/character/<string:picture_id>.html')
def character(picture_id):
    # Retrieve character data based on the ID
    character_data = get_character_data(picture_id)
    # Process character data and render the template
    return render_template('character.html', character_data=character_data)

# Route for the create page
@app.route('/create.html', methods=['GET', 'POST'])
def create_character():
    if request.method == 'POST':
        # Handle the form submission
        name = request.form.get('name', None)
        is_random = request.form.get('is_random', False)

        if is_random == 'true':
            new_character = character_manager.create_character(True)
        else:
            new_character = character_manager.create_character(False, name)

        character_manager.save_characters(characters=[new_character])
        return render_template('character.html', character=new_character)
    else:
        # Display the form
        return render_template('create-character.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        with open('subscribers.json', 'a+') as file:
            file.seek(0)  # Go to the first line of the file
            if file.read(1):  # Check if file is not empty
                file.seek(0)
                data = json.load(file)
                data['subscribers'].append(email)
            else:
                data = {'subscribers': [email]}
            file.seek(0)  # Go back to the first line of the file
            file.truncate()  # Remove existing contents
            json.dump(data, file)
    return redirect(url_for('index'))

# Discord Bot
intents = discord.Intents.all()
intents.typing = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in')

def run_discord_bot():
    bot.run(discord_token)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=app.run, kwargs={'debug': False})
    discord_thread = threading.Thread(target=run_discord_bot)

    flask_thread.start()
    discord_thread.start()

    flask_thread.join()
    discord_thread.join()
