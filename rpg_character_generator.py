from utils.image_optim import optimize_images
from models.character_manager_class import CharacterManager

def main():
    print("Welcome to the RPG Character Generator!")
    character_manager = CharacterManager()

    while True:
        # Menu
        print("1. Create random characters")
        print("2. Optimize images")
        print("3. Create a specific character")
        print("4. Update a specific character")
        print("0. Exit the program")

        choice = input("What do you want to do? ")

        if choice == "1":
            if character_manager.check_character_count():
                character_manager.create_random_character_option()
        elif choice == "2":
            optimize_images("./large_images", "./static/images")
            
            print("Images optimized!")
        elif choice == "3":
            if character_manager.check_character_count():
                character_manager.create_character(is_random=False)
        elif choice == "4":
            character_manager.update_character_prompt()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()



