import random
from settings.image_prompt_settings import artists_and_photographers, colors, illustrators, lighting, portrait, artists
from utils.indefinite_article import indefinite_article

def choose_two_and_join(elements):
    choices = random.sample(elements, 2)
    return ' and '.join(str(choice) for choice in choices)

# Create a class object for the character's image prompt

class ImagePrompt:
    def __init__(self, character):
        self.character = character
        self.genre = "Fantasy"
        self.emotion = self.character.behavior
        self.ethnicity = self.character.ethnicity_name
        self.background = self.character.background_name
        self.scene = self.scene()
        self.tones = self.tones()
        self.style = self.style()
        self.tags = self.tags()
        self.actor = self.actor()
        self.lighting = self.lighting()
        self.image_type = self.image_type()
        
    def scene(self):
        return f"{indefinite_article(self.background)} {self.ethnicity} {self.character.character_class} named {self.character.full_name}"

    def tones(self):
        return choose_two_and_join(colors)
    
    def style(self):
        return random.choice(artists_and_photographers + illustrators + artists)

    def tags(self):
        keywords = ', '.join(self.character.ethnicity_keywords)
        return f"{keywords}, Fantasy, Medieval Fantasy, Dungeons & Dragons. --s 1000 --upbeta --seed {self.character.picture_id}"

    def actor(self):
        return f"{self.character.create_physical_description_text()}"

    def lighting(self):
        return random.choice(lighting)
    
    def image_type(self):
        return random.choice(portrait)
    
    def craft_image_prompt(self):
        return f"{self.image_type} in the style of {self.style} | {self.genre} | {self.scene} | {self.actor} | {self.tones} tones | {self.lighting} | {self.tags}"
