import json
from flask import Flask, render_template

def get_image_url(filename):
    base_url = 'https://zippy-rabanadas-30839c.netlify.app'
    return f'{base_url}/static/{filename}'

app = Flask(__name__, static_folder='static', static_url_path='/static')

def get_character_data(id):
    with open('characters_with_images.json', 'r') as f:
        characters = json.load(f)
    for character in characters:
        if character.get('id') == id:
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

# Route for individual character based on ID
@app.route('/character/<int:id>.html')
def character(id):
    # Retrieve character data based on the ID
    character_data = get_character_data(id)
    # Process character data and render the template
    return render_template('character.html', character=character_data)


if __name__ == '__main__':
    app.run(debug=False)
