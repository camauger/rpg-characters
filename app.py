import json
from flask import Flask, render_template, request, redirect, url_for
from models.character_manager_class import CharacterManager
import os
from dotenv import load_dotenv
from threading import Lock

# Load .env file
load_dotenv()

# Initialize a thread lock
lock = Lock()

# Flask App
app = Flask(__name__, static_folder='static', 
                      static_url_path='/static')
character_manager = CharacterManager()

def get_character_data(picture_id):
    characters = load_characters()
    for character in characters:
        if character.get('picture_id') == picture_id:
            return character
    return None

def load_characters():
    try:
        with open('characters.json', 'r') as f:
            characters = json.load(f)
        return characters
    except IOError:
        print("Error loading characters file")
        return []

@app.route('/')
@app.route('/index.html')
def index():
    characters = load_characters()
    return render_template('index.html', characters=characters)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/character/<string:picture_id>.html')
def character(picture_id):
    character_data = get_character_data(picture_id)
    return render_template('character.html', character_data=character_data)

@app.route('/create-character.html', methods=['GET', 'POST'])
def create_character():
    if request.method == 'POST':
        try:
            new_character = character_manager.create_character(is_random=True)

            if new_character is not None:
                character_manager.save_characters(characters=[new_character])
            return render_template('character.html', 
                                  character_data=new_character)
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        return render_template('create-character.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        with lock:  # Ensure thread safety during file writes
            try:
                with open('subscribers.json', 'a+') as file:
                    file.seek(0)  # Go to the first line of the file
                    data = {'subscribers': [email]}
                    if file.read(1):  # Check if the file is not empty
                        file.seek(0)
                        data = json.load(file)
                        data['subscribers'].append(email)
                    file.truncate(0)  # Remove existing contents
                    json.dump(data, file)
            except IOError:
                print("Error updating subscribers file")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
