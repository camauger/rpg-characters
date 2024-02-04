from mongoengine import connect
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from models.character_class import Character
from models.character_manager_class import CharacterManager
from mongoengine import StringField, IntField, connect
from pymongo import MongoClient, errors
from threading import Lock
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import json
import os
import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Load .env file
load_dotenv()
try:
    # Connect to your MongoDB database
    connection_string = os.environ.get('MONGO_CONNECTION_STRING')
    client = MongoClient(connection_string)
    db = client.rpg
    collection = db.rpgCharacters
    connect(db='rpg', host=connection_string)
    print("Connected to MongoDB")
except Exception as e:
    logging.error(f"An error occurred while connecting to MongoDB: {e}")


# Initialize a thread lock
lock = Lock()

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Flask App
app = Flask(__name__, static_folder='static')

character_manager = CharacterManager()


class CharacterForm(FlaskForm):
    name = StringField('Character Name', validators=[DataRequired()])
    submit = SubmitField('Generate Character')


def handle_db_operations():
    try:
        collection.create_index([("character_id", 1)], unique=True)
    except Exception as e:
        logging.error(f"An error occurred while creating index: {e}")


@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    characters = load_characters()
    return render_template('index.html', characters=characters)


@app.route('/generate', methods=['GET', 'POST'])
def generate_character():
    form = CharacterForm()
    if form.validate_on_submit():
        try:
            new_character = character_manager.create_character(
                params=[], is_random=True)
            collection.insert_one(new_character)
            return redirect(url_for('character_result', id=new_character['id']))
        except errors.PyMongoError as e:
            logging.error(
                f"An error occurred while inserting the character: {e}")
    return render_template('generate_character.html', form=form)


def load_characters():
    try:
        characters = Character.objects.all()
        return characters
    except Exception as e:
        logging.error(f"Error loading characters from MongoDB: {e}")
        return []


@app.route('/about.html', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/character/<string:picture_id>.html', methods=['GET'])
def character(picture_id):
    character_data = Character.objects(picture_id=picture_id).first()
    return render_template('character.html', character_data=character_data)


@app.route('/create-character.html', methods=['GET', 'POST'])
def create_character():
    if request.method == 'POST':
        try:
            new_character = character_manager.create_character(is_random=True)
            if new_character is not None:
                character_manager.save_characters(characters=[new_character])
            return render_template('character.html', character_data=new_character)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
    else:
        return render_template('create-character.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        with lock:  # Ensure thread safety during file writes
            try:
                with open('subscribers.json', 'a') as file:
                    data = {'subscribers': [email]}
                    json.dump(data, file)
            except IOError:
                logging.error("Error updating subscribers file")
    return redirect(url_for('index'))


if __name__ == '__main__':
    handle_db_operations()
    app.run(debug=True)
