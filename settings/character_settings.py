
import json

def transform_background_settings(background_settings):
    background_data = []

    # Sort the background_settings array
    sorted_background_settings = sorted(background_settings)

    # Transform the background_settings array into a list of dictionaries
    for index, background_name in enumerate(sorted_background_settings, start=1):
        background_data.append({
            "name": background_name,
            "id": str(index).zfill(3)
        })

    # Write the background data to a JSON file
    with open('./settings/background_data.json', 'w') as f:
        json.dump(background_data, f, indent=4)

background_settings = ['Acolyte', 'Charlatan', 'Criminal', 'Entertainer', 'Folk Hero', 'Guild Artisan', 'Hermit', 'Noble', 'Outlander', 'Sage', 'Sailor', 'Soldier', 'Urchin', 'Anthropologist', 'Archaeologist', 'Haunted One', 'City Watch', 'Clan Crafter', 'Cloistered Scholar', 'Courtier', 'Faction Agent', 'Far Traveler', 'Gladiator', 'Knight', 'Knight of the Order', 'Mercenary Veteran', 'Urban Bounty Hunter', 'Uthgardt Tribe Member', 'Waterdhavian Noble', 'Inheritor', 'Spy']

# Call the function and pass the background_settings array as an argument
#transform_background_settings(background_settings)



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
    ('Red', 15),
    ('Orange', 10),
    ('Yellow', 10),
    ('Green', 1),
    ('Teal', 1),
    ('Blue', 1),
    ('Indigo', 10),
    ('Purple', 15),
    ('Lilac', 1),
    ('Pink', 1),
    ('Blush', 1),
    ('Rainbow', 1),
    ('Fluorescent', 1),
    ('Ombre', 10),
    ('Streaked', 5),
]

gender_settings = [
('Male', 45),
('Female', 50),
('Non-binary', 5)
]

physical_settings = ["Tall", "Short", "Slender", "Muscular", "Lean", "Athletic", "Curvy", "Voluptuous", "Stocky", "Chiseled", "Petite", "Plump", "Stout", "Bulky", "Svelte", "Lithe", "Solid", "Broad-shouldered", "Delicate", "Lanky", "Sinewy", "Compact", "Shapely", "Ripped", "Toned", "Angular", "Gorgeous", "Handsome", "Pretty", "Attractive", "Exotic", "Elegant", "Graceful", "Striking", "Radiant", "Youthful", "Aging", "Weathered", "Wrinkled", "Wizened", "Scarred", "Fierce", "Intimidating", "Fierce", "Commanding", "Mysterious", "Enigmatic", "Alluring", "Seductive", "Mesmerizing", "Majestic", "Regal", "Noble"]




