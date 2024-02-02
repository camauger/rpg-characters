import json
import random

def pick_random_data_from_file(filename, key):
    with open(filename, 'r') as f:
        data = json.load(f)
    return random.choice(data[key])

def pick_random_item(data, attribute_path, key=None):
    items = data
    for attr in attribute_path:
        items = items[attr]
    if key is not None:
        items = [item[key] for item in items]
    return random.choice(items)