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

physical_settings = ["Tall", "Short", "Slender", "Muscular", "Lean", "Athletic", "Curvy", "Voluptuous", "Stocky", "Chiseled", "Petite", "Plump", "Stout", "Bulky", "Svelte", "Lithe", "Solid", "Broad-shouldered", "Delicate", "Lanky", "Sinewy", "Compact", "Shapely", "Ripped", "Toned", "Angular", "Gorgeous", "Handsome", "Pretty", "Attractive", "Exotic", "Elegant", "Graceful", "Striking", "Radiant", "Youthful", "Aging", "Weathered", "Wrinkled", "Wizened", "Scarred", "Fierce", "Intimidating", "Fierce", "Commanding", "Mysterious", "Enigmatic", "Alluring", "Seductive", "Mesmerizing", "Majestic", "Regal", "Noble"]




