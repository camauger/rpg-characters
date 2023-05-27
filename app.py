import json
from flask import Flask, render_template, request, redirect, url_for
from models.character_manager_class import CharacterManager
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

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
@app.route('/create-character.html', methods=['GET', 'POST'])
def create_character():
    if request.method == 'POST':
        try:
            # Handle the form submission
            new_character = None
            new_character = character_manager.create_character(is_random=True)

            if new_character is not None:
                character_manager.save_characters(characters=[new_character])
            return render_template('character.html', character_data=new_character)
     
        except Exception as e:
            return f"An error occurred: {e}"
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


if __name__ == '__main__':
    app.run(debug=True)
