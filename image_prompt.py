# Create an image prompt for a random character
import random
portrait = [
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
  "Character Portrait"
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

def craft_image_prompt(character):
        return f"Create a {random.choice(portrait)} of {character.full_name}. {character.physical_description_text} {random.choice(colors)} and {random.choice(colors)} tones. {random.choice(lighting)}. Medieval Fantasy Setting, D&D. --seed {character.id}"
