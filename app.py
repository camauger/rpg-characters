import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models.character_manager_class import CharacterManager
import os

# Load .env file
load_dotenv()

    
# Flask App
app = Flask(__name__, static_folder='static')
from flask_cors import CORS

# After initializing your Flask app
CORS(app)

# Character manager
character_manager = CharacterManager()


@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    # The characters are now loaded via a serverless function with AJAX on the frontend
    return render_template('index.html')


@app.route('/generate-character', methods=['GET'])
def generate_character():
    # The character generation is now handled by a serverless function
    # This route can serve a static form that submits to the serverless function endpoint
    return render_template('generate-character.html')


@app.route('/about.html', methods=['GET'])
def about():
    # Static page, no changes needed
    return render_template('about.html')


@app.route('/thank-you.html', methods=['GET'])
def about():
    # Static page, no changes needed
    return render_template('thank-you.html')


@app.route('/<string:picture_id>.html', methods=['GET'])
def character(picture_id):
    # Character details might now be fetched via AJAX using serverless functions
    # This route could be adjusted to pass only the ID to a template
    # And then use JavaScript to fetch the character data from a serverless function
    return render_template('character.html', picture_id=picture_id)

from flask import request, jsonify

@app.route('/generate-random-character', methods=['POST'])
def create_character():
    data = request.json  # Access JSON data sent with the POST request
    print(data)
    # Your logic here:
    new_character = character_manager.create_character({}, is_random=True)
    if new_character:
        return jsonify({'message': 'Character created successfully', 'character': new_character.to_dict()})
    else:
        return jsonify({'message': 'Failed to create character'}), 500

DEBUG_MODE = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']


if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)
