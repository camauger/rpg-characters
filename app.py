import json
from flask import Flask, render_template

app = Flask(__name__)

def get_character_data(id):
    with open('characters_with_images.json', 'r') as f:
        characters = json.load(f)
    for character in characters:
        if character.get('id') == id:
            return character
    return None

# Route for the home page
@app.route('/')
def index():
    with open('characters_with_images.json', 'r') as f:
        characters = json.load(f)
    return render_template('index.html', characters=characters, static_url_path='/static')

# Route for individual character based on ID
@app.route('/character/<int:id>.html')
def character(id):
    # Retrieve character data based on the ID
    character_data = get_character_data(id)
    
    # Process character data and render the template
    return render_template('character.html', character=character_data, static_url_path='/static')

if __name__ == '__main__':
    app.run(debug=False)
