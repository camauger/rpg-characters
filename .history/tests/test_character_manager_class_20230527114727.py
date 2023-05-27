import unittest
from unittest.mock import patch, mock_open
from models.character_class import Character
from character_manager_class import CharacterManager


class TestCharacterManager(unittest.TestCase):
    def setUp(self):
        self.character_manager = CharacterManager()

    def test_load_characters(self):
        # Test that the characters attribute is an empty list if the JSON file doesn't exist
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = FileNotFoundError
            self.character_manager.load_characters()
            self.assertEqual(self.character_manager.characters, [])

        # Test that the characters attribute is an empty list if the JSON file is empty
        with patch('builtins.open', mock_open(read_data='[]')) as mock_file:
            self.character_manager.load_characters()
            self.assertEqual(self.character_manager.characters, [])

        # Test that the characters attribute is a list of Character objects if the JSON file contains character data
        with patch('builtins.open', mock_open(read_data='[{"id": 1, "name": "Test Character"}]')) as mock_file:
            self.character_manager.load_characters()
            self.assertIsInstance(self.character_manager.characters[0], Character)

    def test_save_characters(self):
        # Test that the JSON file is created and characters are saved to it
        with patch('builtins.open', mock_open()) as mock_file:
            self.character_manager.save_characters([Character(1, {"name": "Test Character"})])
            mock_file.assert_called_once_with('characters.json', 'w')
            mock_file().write.assert_called_once_with('[{"id": 1, "name": "Test Character"}]')

    def test_check_character_count(self):
        # Test that the method returns True if the number of characters is less than the maximum
        self.character_manager.characters = [Character(i, {}) for i in range(10)]
        self.assertTrue(self.character_manager.check_character_count())

        # Test that the method returns False if the number of characters is equal to the maximum
        self.character_manager.characters = [Character(i, {}) for i in range(9999)]
        self.assertFalse(self.character_manager.check_character_count())

    def test_generate_character_id(self):
        # Test that the method generates a unique ID
        existing_ids = [1, 2, 3]
        character_id = self.character_manager.generate_character_id(existing_ids)
        self.assertNotIn(character_id, existing_ids)

    def test_create_character(self):
        # Test that the method returns None if the maximum number of characters has been reached
        self.character_manager.characters = [Character(i, {}) for i in range(9999)]
        self.assertIsNone(self.character_manager.create_character(is_random=True))

        # Test that the method returns a Character object if the maximum number of characters has not been reached
        self.assertIsInstance(self.character_manager.create_character(is_random=True), Character)

    def test_create_characters(self):
        # Test that the method returns an empty list if the maximum number of characters has been reached
        self.character_manager.characters = [Character(i, {}) for i in range(9999)]
        self.assertEqual(self.character_manager.create_characters(1), [])

        # Test that the method returns a list of Character objects if the maximum number of characters has not been reached
        self.assertIsInstance(self.character_manager.create_characters(1)[0], Character)

    def test_update_character(self):
        # Test that the method updates a character's information
        character = Character(1, {"name": "Test Character"})
        self.character_manager.characters = [character]
        self.character_manager.update_character(1, {"name": "Updated Name"})
        self.assertEqual(character.name, "Updated Name")

    def test_get_files_in_folder(self):
        # Test that the method returns a list of file names in a folder
        self.assertIn("test.txt", self.character_manager.get_files_in_folder("./test_folder"))

if __name__ == '__main__':
    unittest.main()