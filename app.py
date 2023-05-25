import json
import threading
from flask import Flask, render_template, request
import discord
from discord.ext import commands
from models.character_manager_class import CharacterManager
from api_settings import discord_token

# Flask App
app = Flask(__name__, static_folder='static', static_url_path='/static')
character_manager = CharacterManager()

def get_character_data(id):
    with open('characters_with_images.json', 'r') as f:
        characters = json.load(f)
    for character in characters:
        if character.get('id') == id:
            # Replace '\n\n' with '<br>' in all string fields
            for key, value in character.items():
                if isinstance(value, str):
                    character[key] = value.replace('\n\n', '<br>')
            return character
    return None

def load_characters():
    with open('characters_with_images.json', 'r') as f:
        characters = json.load(f)
    return characters

# Route for the home page
@app.route('/')
def index():
    # Render the template
    return render_template('index.html', characters=load_characters())

# Route for the about page
@app.route('/about.html')
def about():
    # Render the template
    return render_template('about.html')

# Route for individual character based on ID
@app.route('/character/<int:id>.html')
def character(id):
    # Retrieve character data based on the ID
    character_data = get_character_data(id)
    # Process character data and render the template
    return render_template('character.html', character=character_data)

# Route for the create page
@app.route('/create', methods=['GET', 'POST'])
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

# Discord Bot
intents = discord.Intents.default()
intents.typing = False

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
