import random
from settings.image_prompt_settings import artists_and_photographers, colors, illustrators, lighting, portrait
from utils.indefinite_article import indefinite_article

class ImagePrompt:
    def __init__(self, character):
        self.character = character

    def craft_image_prompt(self):
        image_type = random.choice(portrait)
        genre = "Fantasy"
        emotion = self.character.behavior
        scene = f"{indefinite_article(self.character.background)} {self.character.character_class} named {self.character.full_name}"

        pick_tones = random.sample(colors, 2)
        tones = ' and '.join(str(choice) for choice in pick_tones)

        total_styles = artists_and_photographers + illustrators
        pick_styles = random.sample(total_styles, 2)
        styles = ' and '.join(str(choice) for choice in pick_styles)

        actor = f"{self.character.create_physical_description_text()}"
        lighting_type = random.choice(lighting)
        tags = f"Forgotten Realms, Medieval Fantasy Setting, D&D. --s 1000 --upbeta --seed {self.character.id}"
        return f"IMAGE_TYPE: {image_type} in the style of {styles} | GENRE: {genre} | EMOTION: {emotion} | SCENE: {scene} | ACTOR: {actor} | TONES: {tones} | LIGHTING: {lighting_type} | TAGS: {tags}"
