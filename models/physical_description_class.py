from settings.random_settings import create_eye_color, create_hair_color, create_hair_style, create_physical_trait

# Create a class object for the character's physical description
class PhysicalDescription:
    def __init__(self):
        self.physical_trait = create_physical_trait()
        self.hair_color = create_hair_color()
        self.hair_style = create_hair_style()
        self.eye_color = create_eye_color()

    def __str__(self) -> str:
        return f"The character has {self.hair_color} {self.hair_style} hair and {self.eye_color} eyes."
