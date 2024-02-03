from models.character_class import Character
from settings.random_settings import pick_random_ethnicity
from utils.image_optim import optimize_images
from models.character_manager_class import CharacterManager


class RPGCharacterGenerator:
    def __init__(self):
        self.character_manager = CharacterManager()

    @staticmethod
    def print_menu():
        print("1. Create a random character")
        print("2. Optimize images")
        print("3. Create a specific character")
        print("4. Update a specific character")
        print("5. Create a fantasy character")
        print("0. Exit the program")

    def user_choice(self, choice):
        if choice == "1":
            new_character = Character()
            new_character.create_character(params={
            }, is_random=True)
            new_character.save()
        elif choice == "2":
            optimize_images("./large_images", "./static/images")
            print("Images optimized!")
        elif choice == "3":
            if self.character_manager.check_character_count():
                self.character_manager.create_character(is_random=False)
        elif choice == "4":
            self.character_manager.update_character_prompt()
        elif choice == "5":
            if self.character_manager.check_character_count():
                self.character_manager.create_character(
                    is_random=False, is_fantasy=True)
        elif choice == "0":
            print("Goodbye!")
            return False
        else:
            print("Invalid choice!")
        return True

    def main_loop(self):
        while True:
            self.print_menu()
            choice = input("What do you want to do? ")
            if not self.user_choice(choice):
                break


if __name__ == "__main__":
    rpg_gen = RPGCharacterGenerator()
    rpg_gen.main_loop()
