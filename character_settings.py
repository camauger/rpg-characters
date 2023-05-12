import json
import random

character_classes = [
    'Barbarian',
    'Bard',
    'Cleric',
    'Druid',
    'Fighter',
    'Monk',
    'Paladin',
    'Ranger',
    'Rogue',
    'Sorcerer',
    'Warlock',
    'Wizard',
    'Artificer',
    'Blood Hunter',
    'Mystic',
    'Psion',
    'Shaman',
    'Warden',
    'Warlord',
    'Runepriest',
    'Swordmage',
    'Valkyrie',
    'Gunslinger',
    'Death Knight',
    'Jester',
    'Trickster',
    'Elementalist',
    'Beastmaster',
    'Samurai',
    'Ninja',
    'Swashbuckler',
    'Skald',
    'Archmage',
    'Necromancer',
    'Inquisitor',
    'Oracle',
    'Illusionist',
    'Dracomancer',
    'Pirate',
    'Gladiator',
    'Shadowdancer',
    'Chronomancer',
    'Alchemist',
    'Witch',
    'Duelist',
    'Shapeshifter',
    'Summoner',
    'Spirit Shaman',
    'Bounty Hunter',
    'Enchanter',
    'Berserker',
    'Martial Artist',
    'Spellsword',
    'Battlemage',
    'Arcane Trickster',
    'Elemental Shaman',
    'Brewmaster',
    'Dreamwalker',
    'Arcane Archer',
    'Scout',
    'Priestess',
    'Warrior Priest',
    'Shadow Knight',
    'Demonic Sorcerer',
    'Divine Herald',
    'Beast Tamer',
    'Spellblade',
    'Nature Warden',
    'Geomancer',
    'Dervish',
    'Airbender',
    'Earthshaker',
    'Waterweaver',
    'Firestarter',
    'Plague Doctor',
    'Hexblade',
    'Spellbreaker',
    'Bardbarian',
    'Runescribe',
    'Abyssal Walker',
    'Voidcaster',
    'Herald of Light',
    'Shadowblade',
    'Tidecaller',
    'Stormsinger',
    'Fortune Teller',
    'Bladeweaver',
    'Soulbinder',
    'Swordsworn',
    'Spellweaver',
    'Storm Herald',
    'Celestial',
    'Crusader',
    'Shadow Monk',
    'Frost Mage',
    'Warpriest',
    'Beast Knight',
    'Blood Mage',
    'Skald Berserker',
    'Mystical Rogue',
    'Eldritch Knight',
    'Arcane Healer',
    'Feylock',
    'Soulknife',
    'Pyromancer',
    'Druidic Knight',
    'Spellfire Archer',
    'Mindflayer',
    'Spiritualist',
    'Death Cleric',
    'Mystic Knight',
    'Demon Hunter',
    'Priest of Shadows',
    'Clockwork Engineer',
    'Feral Berserker',
    'Runic Mage',
    'Chaos Sorcerer',
    "Nature's Champion",
    'Hexblade Rogue',
    'Windwalker',
    'Blightcaster',
    'Blood Knight',
    'Lightning Monk',
    'Spellstorm',
    'Stone Warden',
    'Seer']


background = ['Acolyte', 'Charlatan', 'Criminal', 'Entertainer', 'Folk Hero', 'Guild Artisan', 'Hermit', 'Noble', 'Outlander', 'Sage', 'Sailor', 'Soldier', 'Urchin', 'Anthropologist', 'Archaeologist', 'Haunted One', 'City Watch', 'Clan Crafter', 'Cloistered Scholar', 'Courtier', 'Faction Agent', 'Far Traveler', 'Gladiator', 'Knight', 'Knight of the Order', 'Mercenary Veteran', 'Urban Bounty Hunter', 'Uthgardt Tribe Member', 'Waterdhavian Noble', 'Inheritor', 'Spy']

ethnicity = ['Human', 'Dwarf', 'Elf', 'Halfling', 'Dragonborn', 'Gnome', 'Half-Elf', 'Half-Orc', 'Tiefling']

age_settings = ['Infant', 'Child', 'Teenager', 'Young Adult', 'Adult', 'Middle-aged', 'Senior', 'Elderly', 'Ancient', 'Ageless', 'Timeless', 'Youthful']

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


