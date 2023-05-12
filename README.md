# RPG Character Generator

This code provides a Python script for generating random RPG (Role-Playing Game) characters. It utilizes various modules and classes to create unique character attributes, descriptions, and background stories. The generated characters can be stored in a CSV file and their details can be saved in a JSON file.

## Prerequisites

Before running the script, ensure that you have the following:

- Python 3 installed on your system.
- The required Python packages installed: `requests`, `csv`.

## Setup

1. Download the code files and save them in a directory of your choice.
2. Install the required Python packages using the following command:
   ```
   pip install requests csv
   ```
3. Obtain an API key for the OpenAI GPT-3 language model. Replace the `api_key` variable in the script with your API key.

## Usage

1. Open a terminal or command prompt.
2. Navigate to the directory where the script is saved.
3. Run the script using the following command:
   ```
   python rpg_character_generator.py
   ```
4. Follow the prompts to specify the number of characters you want to create.
5. Once the characters are generated, their details will be saved in the `data/characters_data.csv` file.
6. The character descriptions, including the background stories and image prompts, will be stored in the `characters.json` and `data/image_prompts.txt` files, respectively.

## Extending the Code

- You can modify the character attributes, such as character classes, backgrounds, ethnicities, ages, and genders, by updating the corresponding lists in the `character_settings.py` module.
- To customize the physical description and behavior of characters, you can modify the respective classes in the `physical_description.py` and `character_settings.py` modules.
- The `name_composition.py` module provides methods for generating random first and last names. You can customize the name generation logic in this module.
- To improve the generated background stories, you can experiment with different prompts or modify the `fetch_character_data` function in the script to interact with the OpenAI GPT-3 API differently.

## Credits

The code utilizes the OpenAI GPT-3 language model for generating background stories. The physical descriptions, names, and character attributes are randomly generated using the provided modules.

Note: Ensure that you comply with the terms of service and usage policies of the OpenAI GPT-3 API when utilizing the language model for generating text.

---

