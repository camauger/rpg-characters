import json
import random

#Create a random first name
def generate_random_first_name(gender):
    data = ''
    
    if (gender == 'Male'):
        data='data/names-mal.txt'
    elif (gender == 'Female'):
        data='data/names-fem.txt'
    else:
        data='data/names.txt'

    with open(data, "r") as file:
        names = [line.strip() for line in file]
        first_name = random.choice(names)
        return first_name.capitalize()

# Create a random character last name
def generate_random_last_name():
    data = random.choice(['data/syllables_fem.json', 'data/syllables_mal.json', 'data/syllables_gen.json'])

    with open(data) as file:
        data = json.load(file)
        
        prefixes = data['syllables']['prefixes']
        middle = data['syllables']['middle']
        suffixes = data['syllables']['suffixes']
        
        last_name = "".join(random.choice(prefixes + middle + suffixes) for _ in range(random.randint(1, 4)))
        
        return last_name.capitalize()

