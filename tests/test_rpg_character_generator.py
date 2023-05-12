import unittest
from unittest.mock import patch
from name_composition import generate_random_first_name, generate_random_last_name
from physical_description import PhysicalDescription
from character_settings import CharacterBehavior, character_classes, ethnicity, background, age_settings, gender
from image_prompt import craft_image_prompt
from rpg_character_generator import Character, random_gender, pick_random_age

class TestCharacterFunctions(unittest.TestCase):

    def setUp(self):
        self.character = Character(
            character_classes[0], background[0], ethnicity[0], age_settings[0], gender[0]
        )

    def test_generate_random_first_name(self):
        random_name = generate_random_first_name(gender[0])
        self.assertIsInstance(random_name, str)

    def test_generate_random_last_name(self):
        random_name = generate_random_last_name()
        self.assertIsInstance(random_name, str)

    def test_create_physical_description(self):
        physical_description = self.character.create_physical_description()
        self.assertIsInstance(physical_description, PhysicalDescription)

    def test_create_psychological_description(self):
        psychological_description = self.character.create_psychological_description()
        self.assertIsInstance(psychological_description, str)

    def test_create_physical_description_text(self):
        physical_description_text = self.character.create_physical_description_text()
        self.assertIsInstance(physical_description_text, str)

    def test_create_background_story(self):
        prompt = "Test prompt"
        api_key = "test_api_key"
        with patch("main.fetch_character_data") as mock_fetch_character_data:
            mock_fetch_character_data.return_value = "Test background story"
            background_story = self.character.create_background_story(prompt, api_key)
            mock_fetch_character_data.assert_called_once_with(prompt, api_key)
            self.assertEqual(background_story, "Test background story")

    def test_create_image_prompt(self):
        image_prompt = self.character.create_image_prompt()
        self.assertIsInstance(image_prompt, str)

    def test_random_gender(self):
        random_gender_value = random_gender()
        self.assertIn(random_gender_value, gender)

    def test_pick_random_age(self):
        random_age = pick_random_age()
        self.assertIn(random_age, age_settings)

if __name__ == "__main__":
    unittest.main()
