import json
from flask import Flask, render_template, url_for

def get_image_url(filename):
    base_url = 'https://zippy-rabanadas-30839c.netlify.app'
    return f'{base_url}/static/{filename}'


app = Flask(__name__)

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
    characters = load_characters()
    processed_characters = []

    for character in characters:
        image_url = get_image_url(character.get('physical_description').get('image'))
        processed_characters.append({
            'id': character.get('id'),
            'full_name': character.get('first_name') + ' ' + character.get('last_name'),
            'image_url': image_url,
            # Include other character attributes as needed
        })

    return render_template('index.html', characters=processed_characters)


# Route for individual character based on ID
@app.route('/character/<int:id>.html')
def character(id):
    # Retrieve character data based on the ID
    character_data = get_character_data(id)
    
    # Process character data and render the template
    return render_template('character.html', character=character_data, static_url_path='/static')

if __name__ == '__main__':
    app.run(debug=False)
