import json
import random


background_settings = ['Acolyte', 'Charlatan', 'Criminal', 'Entertainer', 'Folk Hero', 'Guild Artisan', 'Hermit', 'Noble', 'Outlander', 'Sage', 'Sailor', 'Soldier', 'Urchin', 'Anthropologist', 'Archaeologist', 'Haunted One', 'City Watch', 'Clan Crafter', 'Cloistered Scholar', 'Courtier', 'Faction Agent', 'Far Traveler', 'Gladiator', 'Knight', 'Knight of the Order', 'Mercenary Veteran', 'Urban Bounty Hunter', 'Uthgardt Tribe Member', 'Waterdhavian Noble', 'Inheritor', 'Spy']

ethnicity_settings = [
        ('Human', 60),
        ('Elf', 15),
        ('Dwarf', 15),
        ('Halfling', 5),
        ('Dragonborn', 2),
        ('Gnome', 2),
        ('Half-Elf', 1),
        ('Half-Orc', 1),
        ('Tiefling', 1)
    ]

age_settings = [
        ('Infant', 0),
        ('Child', 0),
        ('Teenager', 5),
        ('Young Adult', 35),
        ('Adult', 40),
        ('Middle-aged', 25),
        ('Senior', 15),
        ('Elderly', 10),
        ('Ancient', 5),
        ('Ageless', 2),
        ('Timeless', 2),
        ('Youthful', 5)
    ]

hair_colors_settings = [
    ('White-Blond', 5),
    ('Blond', 30),
    ('Golden', 20),
    ('Sandy', 15),
    ('Light Brown', 25),
    ('Brown', 40),
    ('Ash Brown', 15),
    ('Dark Brown', 35),
    ('Black', 50),
    ('Ashen', 10),
    ('Grey', 10),
    ('Platinum', 10),
    ('White', 15),
    ('Auburn', 20),
    ('Mahogany', 15),
    ('Red', 25),
    ('Orange', 10),
    ('Yellow', 10),
    ('Green', 5),
    ('Teal', 5),
    ('Blue', 15),
    ('Indigo', 10),
    ('Purple', 15),
    ('Lilac', 5),
    ('Pink', 15),
    ('Blush', 5),
    ('Rainbow', 5),
    ('Fluorescent', 5),
    ('Ombre', 10),
    ('Streaked', 10),
]

gender_settings = [
('Male', 50),
('Female', 50),
('Non-binary', 10)
]

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


