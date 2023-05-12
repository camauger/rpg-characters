import json
import random

character_classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger']
background = ['Acolyte', 'Charlatan', 'Criminal', 'Entertainer', 'Folk Hero', 'Guild Artisan', 'Hermit', 'Noble', 'Outlander', 'Sage', 'Sailor', 'Soldier', 'Urchin']
ethnicity = ['Human', 'Dwarf', 'Elf', 'Halfling', 'Dragonborn', 'Gnome', 'Half-Elf', 'Half-Orc', 'Tiefling']
age = ['Young', 'Middle-aged', 'Old']
gender = ['Male', 'Female', 'Non-binary']

class CharacterBehavior:
    def __init__(self):
        self.settings = self.load_settings()

    def load_settings(self):
        with open('data/character_behavior.json', 'r') as f:
            data = json.load(f)
        return data

    def ideal(self):
        random_ideal = random.choice(self.settings['ideals'])
        return random_ideal.lower()
    
    def flaw(self):
        random_flaw = random.choice(self.settings['flaws'])
        return random_flaw.lower()
    
    def bond(self):
        random_bond = random.choice(self.settings['bonds'])
        return random_bond.lower()
    
    def behavior(self):
        random_behavior = random.choice(self.settings['behaviors'])
        return random_behavior.lower()
    
    def nature(self):
        random_nature = random.choice(self.settings['natures'])
        return random_nature.lower()


