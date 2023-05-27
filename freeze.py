import os
from flask_frozen import Freezer
import json
from app import app

freezer = Freezer(app)

def configure_app(app):
    app.config['FREEZER_RELATIVE_URLS'] = True
    app.config['FREEZER_BASE_URL'] = os.environ.get('FREEZER_BASE_URL', '')
    app.config["FREEZER_DESTINATION"] = './build'
    
@freezer.register_generator
def index():
    yield '/'

@freezer.register_generator
def character():
    with open('characters.json', 'r') as f:
        characters = json.load(f)
    for char in characters:
        yield {'picture_id': str(char.get('picture_id'))}


if __name__ == '__main__':
    configure_app(app)
    freezer.freeze()


