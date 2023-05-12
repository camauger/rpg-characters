import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    with open('characters_with_images.json', 'r') as f:
        characters = json.load(f)
    return render_template('index.html', characters=characters, static_url_path='/static')

if __name__ == '__main__':
    app.run(debug=False)


def home():
    return "Hello, Flask!"
