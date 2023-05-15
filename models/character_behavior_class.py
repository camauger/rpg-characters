import json, random

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
    
    def __str__(self) -> str:
        return f"The character's ideal is {self.ideal()}, their flaw is {self.flaw()}, their bond is {self.bond()}, their behavior is {self.behavior()}, and their nature is {self.nature()}."
    

