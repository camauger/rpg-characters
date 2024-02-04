from flask import Flask, render_template
import os

# Flask App
app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    # The characters are now loaded via a serverless function with AJAX on the frontend
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate_character():
    # The character generation is now handled by a serverless function
    # This route can serve a static form that submits to the serverless function endpoint
    return render_template('generate_character.html')

@app.route('/about.html', methods=['GET'])
def about():
    # Static page, no changes needed
    return render_template('about.html')

@app.route('/create-character.html', methods=['GET', 'POST'])
def create_character():
    # Assuming this also moves to serverless function for character creation
    return render_template('create-character.html')

@app.route('/character/<string:picture_id>.html', methods=['GET'])
def character(picture_id):
    # Character details might now be fetched via AJAX using serverless functions
    # This route could be adjusted to pass only the ID to a template
    # And then use JavaScript to fetch the character data from a serverless function
    return render_template('character.html', picture_id=picture_id)

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't'])
