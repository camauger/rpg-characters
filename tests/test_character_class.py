import random
from name_composition import generate_random_first_name, generate_random_last_name
from physical_description import PhysicalDescription
from character_settings import CharacterBehavior
from image_prompt import craft_image_prompt
from character_class import Character
# You will have to create your own api_settings.py file with your OpenAI API key
from api_settings import api_key
import unittest

class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.character = Character("warrior", "noble", "human", 20, "male")

    def test_init(self):
        self.assertIsNotNone(self.character.id)
        self.assertIsNotNone(self.character.first_name)
        self.assertIsNotNone(self.character.last_name)
        self.assertEqual(self.character.full_name, f"{self.character.first_name} {self.character.last_name}")
        self.assertEqual(self.character.gender, "male")
        self.assertEqual(self.character.character_class, "warrior")
        self.assertEqual(self.character.background, "noble")
        self.assertEqual(self.character.ethnicity, "human")
        self.assertEqual(self.character.age, 20)
        self.assertIsNotNone(self.character.physical_description)
        self.assertIsNotNone(self.character.nature)
        self.assertIsNotNone(self.character.ideal)
        self.assertIsNotNone(self.character.bond)
        self.assertIsNotNone(self.character.flaw)
        self.assertIsNotNone(self.character.behavior)
        self.assertIsNotNone(self.character.psychological_description)
        self.assertIsNotNone(self.character.physical_description_text)
        self.assertEqual(self.character.image_type, "photo")
        self.assertIsNotNone(self.character.image_prompt)
        self.assertIsNotNone(self.character.background_story)

    def test_str(self):
        self.assertEqual(str(self.character), f"{self.character.full_name} is a {self.character.ethnicity} {self.character.character_class} and a {self.character.background}")

if __name__ == '__main__':
    unittest.main()