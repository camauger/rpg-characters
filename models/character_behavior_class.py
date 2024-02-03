import json
import random


class CharacterBehavior:
    def __init__(self, character):
        self.settings = self.load_settings()
        self.character = character

    def load_settings(self):
        with open('data/character_behavior.json', 'r') as f:
            data = json.load(f)
        return data

    def select_random_attribute(self, attributeName):
        random_attribute = random.choice(self.settings[attributeName])
        return random_attribute.lower()

    def create_behavior(self):
        pronoun = "their"
        if (self.character.gender == "Female"):
            pronoun = "her"
        elif (self.character.gender == "Male"):
            pronoun = "his"

        behaviorDescription = f"{self.character.full_name}'s ideal is {self.select_random_attribute('ideals')}. {pronoun} flaw is {self.select_random_attribute('flaws')}, {pronoun} bond is {self.select_random_attribute('bonds')}, {pronoun} behavior is {self.select_random_attribute('behaviors')}, and {pronoun} nature is {self.select_random_attribute('natures')}."

        return behaviorDescription

    def __str__(self) -> str:
        return f"The character's ideal is {self.select_random_attribute('ideals')}, their flaw is {self.select_random_attribute('flaws')}, their bond is {self.select_random_attribute('bonds')}, their behavior is {self.select_random_attribute('behaviors')}, and their nature is {self.select_random_attribute('natures')}."
