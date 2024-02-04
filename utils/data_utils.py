import json
import random

def pick_random_data_from_file(filename, key):
    with open(filename, 'r') as f:
        data = json.load(f)
    return random.choice(data[key])

def pick_random_item(data, attribute_path, key=None):
    items = data
    # remove id from attribute_path
    if attribute_path[0] == '_id':
        attribute_path.pop(0)
    for attr in attribute_path:
        items = items[attr]
    if key is not None:
        items = [item[key] for item in items]
    return random.choice(items)

def choose_two_and_join(elements):
    choices = random.sample(elements, 2)
    return ' and '.join(str(choice) for choice in choices)