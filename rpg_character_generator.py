from utils.image_optim import optimize_images
from discord_bot import move_files, start_discord_bot
from models.character_manager_class import CharacterManager


def main():
    print("Welcome to the RPG Character Generator!")

    # Menu
    print("1. Create random characters")
    print("2. Optimize images")
    print("3. Create a specific character")
    print("4. Archive files")
    print("5. Start the Discord bot")
    print("6. Update a specific character")
    print("0. Exit the program")

    choice = input("What do you want to do? ")
    character_manager = CharacterManager()
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
        move_files()
        print("Files moved!")
    elif choice == "5":
        print("Starting the Discord bot...")
        start_discord_bot()
    elif choice == "6":
        character_manager.update_character_prompt()
    elif choice == "0":
        print("Goodbye!")
        return
    else:
        print("Invalid choice!")

    main()


if __name__ == "__main__":
    main()
