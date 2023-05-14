# Create an image prompt for a random character
import random
portrait = [
  "Photorealistic portrait",
  "Photorealistic headshot",
  "Classic Portrait",
  "Candid Portrait",
  "Environmental Portrait",
  "Studio Portrait",
  "Headshot",
  "Close-up Portrait",
  "Fashion Portrait",
  "Glamour Portrait",
  "Lifestyle Portrait",
  "Fine Art Portrait",
  "Documentary Portrait",
  "Surreal Portrait",
  "Dramatic Portrait",
  "Minimalist Portrait",
  "Moody Portrait",
  "Character Portrait",
  "Head and Shoulders Portrait",
        "Three-Quarter Portrait",
        "Full-Length Portrait",
        "High-Angle Portrait",
        "Low-Angle Portrait",
        "Profile Portrait",
        "Silhouette Portrait",
        "High-Key Portrait",
        "Low-Key Portrait",
        "Rembrandt Portrait",
        "Split Lighting Portrait",
        "Loop Lighting Portrait",
        "Broad Lighting Portrait",
        "Short Lighting Portrait",
        "Glamour Lighting Portrait"
]


colors = [
  "Red",
  "Green",
  "Blue",
  "Yellow",
  "Orange",
  "Purple",
  "Pink",
  "Brown",
  "White",
  "Black",
  "Gray",
  "Crimson",
  "Scarlet",
  "Ruby",
  "Cherry",
  "Burgundy",
  "Maroon",
  "Coral",
  "Vermilion",
  "Raspberry",
  "Firebrick",
  "Emerald",
  "Lime",
  "Olive",
  "Jade",
  "Mint",
  "Chartreuse",
  "Forest Green",
  "Sage",
  "Fern Green",
  "Teal",
  "Sapphire",
  "Sky Blue",
  "Navy Blue",
  "Turquoise",
  "Cobalt Blue",
  "Baby Blue",
  "Steel Blue",
  "Azure",
  "Indigo",
  "Cerulean",
  "Lemon",
  "Gold",
  "Mustard",
  "Amber",
  "Honey",
  "Dandelion",
  "Cream",
  "Yellow Ochre",
  "Buttercup",
  "Saffron",
  "Tangerine",
  "Peach",
  "Apricot",
  "Coral",
  "Burnt Orange",
  "Pumpkin",
  "Terracotta",
  "Rust",
  "Carrot",
  "Ginger",
  "Lavender",
  "Violet",
  "Lilac",
  "Plum",
  "Mauve",
  "Orchid",
  "Amethyst",
  "Grape",
  "Eggplant",
  "Royal Purple",
  "Blush",
  "Bubblegum",
  "Fuchsia",
  "Rose",
  "Salmon",
  "Coral Pink",
  "Hot Pink",
  "Orchid Pink",
  "Magenta",
  "Carnation",
  "Tan",
  "Beige",
  "Chocolate",
  "Caramel",
  "Coffee",
  "Chestnut",
  "Mahogany",
  "Auburn",
  "Walnut",
  "Sienna",
  "Ivory",
  "Pearl",
  "Silver",
  "Gold",
  "Platinum",
  "Bronze",
  "Copper",
  "Mercury",
  "Onyx",
  "Opal"
]

lighting = [
  "Natural Light",
  "Soft Light",
  "Hard Light",
  "Diffused Light",
  "Backlighting",
  "Low Key Lighting",
  "High Key Lighting",
  "Side Lighting",
  "Top Lighting",
  "Rim Lighting",
  "Rembrandt Lighting",
  "Split Lighting",
  "Silhouette Lighting",
  "Candlelight",
  "Firelight",
  "Moonlight",
  "Sunlight",
  "Moonlight",
  "Golden Hour",
]

artists_and_photographers = ['Michael Komarck', 'Donato Giancola', 'Todd Lockwood', 'Kekai Kotaki', 'Wayne Reynolds', 'Cynthia Sheppard', 'Jesper Ejsing', 'Luis Royo', 'Boris Vallejo', 'Frank Frazetta', 'H.R. Giger', 'Brian Froud', 'Nekro', 'Jenny Dolfen', 'Tommy Arnold', 'Magali Villeneuve', 'Rob Alexander', 'Mark Zug', 'Larry Elmore', 'Tony DiTerlizzi', 'Viktor Titov', 'Anne Stokes', 'Keith Parkinson', 'Jessica Rossier', 'Elena Dudina', 'Ben Wootten', 'Amanda Diaz', 'Lara Jade', 'Annie Leibovitz', 'Gregory Crewdson', 'Erik Almas', 'Justin Gerard', 'Mona Finden', 'Rovina Cai', 'Kari Christensen', 'Howard Lyon', 'Noah Bradley', 'Julie Dillon', 'Rebecca Guay', 'Seb McKinnon', 'Alexandra Douglass', 'Natalia P. Gutiérrez', 'Karla Ortiz', 'Yigit Koroglu', 'Johannes Voss', 'Sam Burley', 'Cris Griffin', 'Emily Hare', 'Titus Lunter', 'Cynthia Sheppard', 'Darek Zabrocki', 'Alexandra Semushina']

camera_settings_and_types = ['Aperture Priority Mode', 'Shutter Priority Mode', 'Manual Mode', 'Portrait Mode', '50mm Prime Lens', '85mm Prime Lens', 'Telephoto Lens', 'Wide-Angle Lens', 'Full Frame Camera', 'Crop Sensor Camera', 'Natural Light', 'Studio Lighting', 'Softbox', 'Beauty Dish', 'Fill Light', 'Reflector', 'Bokeh', 'Shallow Depth of Field', 'ISO 100', 'ISO 200', 'ISO 400', 'Low ISO', 'Medium ISO', 'High ISO']

illustrators = ["Tomer Hanuka", "James Jean", "Yuko Shimizu", "Sam Wolfe Connelly", "Yoshitaka Amano", "J.A.W. Cooper", "Audrey Kawasaki", "Esao Andrews", "Nico Delort", "Beeple", "Loish", "Feng Zhu", "Craig Mullins", "Sachin Teng", "Simon Stålenhag", "Jama Jurabaev", "Pascal Campion", "WLOP", "Nivanh Chanthara", "Marta Nael", "Ross Tran", "Ilya Kuvshinov", "Sparth"]

def craft_image_prompt(character, illustration=False):
        if illustration:
                return craft_image_prompt_illustration(character)
        else:
                return craft_image_prompt_photo(character)


def craft_image_prompt_photo(character):        
        prompt = f"In the style of {random.choice(artists_and_photographers)}, create a {character.nature} {random.choice(portrait)} of {character.full_name}, a {character.background} {character.character_class} | {character.physical_description_text} {random.choice(colors)} and {random.choice(colors)} tones | {random.choice(lighting)} | {character.psychological_description} | Detailed facial features, realistic | {random.choice(camera_settings_and_types)}. Forgotten Realms, Medieval Fantasy Setting, D&D. --s 1000 --upbeta --seed {character.id}".lower()
        return prompt.capitalize()

def craft_image_prompt_illustration_old(character):
        prompt = f"In the style of {random.choice(illustrators)}, create a {character.nature} {random.choice(portrait)} of {character.full_name}, a {character.background} {character.character_class} | {character.physical_description_text} {random.choice(colors)} and {random.choice(colors)} tones | {character.psychological_description} | Forgotten Realms, Medieval Fantasy Setting, D&D. --s 1000 --upbeta --seed {character.id}".lower()
        return prompt.capitalize()

def craft_image_prompt_illustration(character):
        image_type = random.choice(portrait)
        genre = "Fantasy"
        emotion = character.nature
        scene = f"A {character.background} {character.character_class} {random.choice(portrait)} {character.full_name}"
        tones = f"{random.choice(colors)} {random.choice(colors)} tones"
        actor = f"{character.physical_description_text} {character.psychological_description}"
        lighting_type = random.choice(lighting)
        tags = f"Forgotten Realms, Medieval Fantasy Setting, D&D. --s 1000 --upbeta --seed {character.id}"
        return f"IMAGE_TYPE: {image_type} | GENRE: {genre} | EMOTION: {emotion} | SCENE: {scene} | ACTOR: {actor} | TONES: {tones} | LIGHTING: {lighting_type} | TAGS: {tags}"