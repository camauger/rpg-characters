# RPG Character Generator

This Python program is an RPG (Role Playing Game) Character Generator. It provides a simple interface to generate and manage RPG characters. The characters can be either randomly generated or custom-made based on user input. Additionally, the program allows users to manage image resources for the characters and update existing character data.

## Install Requirements

To install requirements:
pip install -r requirements.txt

## Key Components

The key components of the program are:

- `CharacterManager`: This class manages all aspects of character creation and maintenance, including loading, saving, and updating character data, checking if the maximum character count has been reached, and generating unique character IDs. Character data is stored in a JSON file.

- `Character`: This class is used to instantiate new character objects. It includes attributes like ID, age, gender, ethnicity, class, subclass, background, and other parameters.

- `Random Settings`: This includes a suite of functions to select random attributes for characters such as age, gender, ethnicity, subrace, character class, subclass, and background.

## Features

1. **Create Random Characters**: The program can generate random characters using the `Random Settings` functions. A check is performed to ensure that the character count doesn't exceed a certain limit before creating new characters.

2. **Optimize Images**: This feature optimizes images for your characters. It is an efficient tool to reduce the size of the images stored in the `large_images` directory and saves the optimized images in the `static/images` directory.

3. **Create a Specific Character**: The program can create a specific character based on user inputs. The user is prompted to provide input for various character attributes.

4. **Update a Specific Character**: This feature allows users to update the attributes of an existing character. The user provides the character ID and the new attribute values, which are then updated in the character data.

## How to Run

To run this program, navigate to the directory containing the script in your terminal and run the command `python3 filename.py`, replacing "filename.py" with the name of the script file.

The program will print a menu with options, prompting you for what you want to do:

Welcome to the RPG Character Generator!

1. Create random characters
2. Optimize images
3. Create a specific character
4. Update a specific character
5. Exit the program

What do you want to do?

Enter the corresponding number for the task you want to perform.

## Dependencies

This program relies on several modules:

1. `utils.image_optim` - a utility module for optimizing images.
2. `models.character_manager_class` - a module that handles the creation, modification, and management of RPG characters.
3. `settings.random_settings` - a module that contains functions to select random attributes for characters.
4. `models.character_class` - a module that defines the `Character` class used to instantiate new character objects.

Please ensure these modules are present in your project directory before running the script.
