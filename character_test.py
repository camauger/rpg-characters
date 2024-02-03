from models.character_class import Character


if __name__ == "__main__":
    # Create a new character

    new_character = Character()
    new_character.create_character(params={
    }, is_random=True)
    print(new_character.__str__() + "\n")
