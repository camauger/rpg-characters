from mongoengine import Document, StringField, BooleanField, DictField
import os
import random


class Character(Document):
    meta = {'collection': 'characters'}

    # Basic character information
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    full_name = StringField(required=True)
    gender = StringField(required=True)

    # Character class and subclass information
    character_class_name = StringField()
    character_subclass_name = StringField()

    # Background information
    background_name = StringField()
    background_setting = StringField()

    # Ethnicity information
    ethnicity_name = StringField()

    # Other character attributes
    age = StringField()
    background_story = StringField()
    eye_color = StringField()
    hair_color = StringField()
    hair_style = StringField()
    has_image = BooleanField(default=False)
    picture_id = StringField()

    # Image prompt attributes (simplified for focus on main attributes)
    clothing = StringField()
    physical_trait = StringField()

    def save_character(self, character_data):
        """
        Saves character data to MongoDB.
        """
        for field, value in character_data.items():
            setattr(self, field, value)
        self.full_name = f"{self.first_name} {self.last_name}"
        self.picture_id = self.generate_picture_id()
        self.save()

    def generate_picture_id(self):
        """
        Generates a unique picture ID for the character.
        """
        return f"{self.full_name.replace(' ', '_').lower()}"
    # return f"{self.full_name.replace(' ', '_').lower()}_{random.randint(1000, 9999)}"

    def to_dict(self):
        """
        Converts the character document to a Python dictionary.
        """
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "gender": self.gender,
            "character_class_name": self.character_class_name,
            "character_subclass_name": self.character_subclass_name,
            "background_name": self.background_name,
            "background_setting": self.background_setting,
            "ethnicity_name": self.ethnicity_name,
            "age": self.age,
            "background_story": self.background_story,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "hair_style": self.hair_style,
            "has_image": self.has_image,
            "picture_id": self.picture_id,
            "clothing": self.clothing,
            "physical_trait": self.physical_trait
        }

    @classmethod
    def create_from_dict(cls, character_dict):
        """
        Creates a Character instance from a dictionary.
        """
        character = cls()
        character.save_character(character_dict)
        return character
