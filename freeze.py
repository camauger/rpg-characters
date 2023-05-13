import os
from flask_frozen import Freezer
import json
from app import app

freezer = Freezer(app)

def configure_app(app):
    app.config['FREEZER_RELATIVE_URLS'] = True
    app.config['FREEZER_BASE_URL'] = os.environ.get('FREEZER_BASE_URL', '')
    app.config["FREEZER_DESTINATION"] = "../build"
    # app.config['FREEZER_BASE_URL'] = 'https://zippy-rabanadas-30839c.netlify.app'
freezer = Freezer(app)

@freezer.register_generator
def character():
    with open('characters_with_images.json', 'r') as f:
        characters = json.load(f)
    for character in characters:
        yield {'id': character.get('id')}

if __name__ == '__main__':
    configure_app(app)
    freezer.freeze()


