from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from models.character_class import Character
from models.character_manager_class import CharacterManager
from mongoengine import Document, StringField, IntField, connect
from pymongo import MongoClient
from threading import Lock
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json
import os
import logging

# Load .env file
load_dotenv()

# Initialize a thread lock
lock = Lock()

# Flask App
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Connect to your MongoDB database
connection_string = os.environ.get('MONGO_CONNECTION_STRING')
client = MongoClient(connection_string)
db = client.rpg
collection = db.rpgCharacters
connect(db='rpg', host=connection_string)

character_manager = CharacterManager()


class CharacterForm(FlaskForm):
    name = StringField('Character Name', validators=[DataRequired()])
    # Add other fields as necessary
    submit = SubmitField('Generate Character')
    
def handle_db_operations():
    try:
        collection.create_index([("character_id", 1)], unique=True)
    except Exception as e:
        logging.error(f"An error occurred while creating index: {e}")

@app.route('/')
@app.route('/index.html')
def index():
    characters = load_characters()
    return render_template('index.html', characters=characters)



@app.route('/generate', methods=['GET', 'POST'])
def generate_character():
    form = CharacterForm()
    if form.validate_on_submit():
        try:
            # Assuming character_manager.create_character returns a dictionary with character info
            new_character = character_manager.create_character(params=[], is_random=True)

            # Insert the character into MongoDB
            collection.insert_one(new_character)
            
            return redirect(url_for('character_result', id=new_character['id']))

        except Exception as e:
            print(f"An error occurred while inserting the character: {e}")
            # You may want to add more robust error handling here
            
    return render_template('generate_character.html', form=form)



def get_character_data(picture_id):
    characters = load_characters()
    for character in characters:
        if character.get('picture_id') == picture_id:
            return character
    return None


def load_characters():
    try:
        characters = Character.objects.all()  # Using MongoEngine to query all character documents
        return characters
    except Exception as e:
        logging.error(f"Error loading characters from MongoDB: {e}")
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
    handle_db_operations()
    app.run(debug=True)
