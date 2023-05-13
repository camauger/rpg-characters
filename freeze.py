from flask_frozen import Freezer
import json
from app import app

freezer = Freezer(app)

@freezer.register_generator
def character():
    with open('characters_with_images.json', 'r') as f:
        characters = json.load(f)
    for character in characters:
        yield {'id': character.get('id')}

if __name__ == '__main__':
    freezer.freeze()