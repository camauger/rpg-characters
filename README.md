# RPG Character Generator

This Python script is a Role-Playing Game (RPG) Character Generator. It allows you to create, manage, and archive RPG characters with various attributes such as age, gender, ethnicity, class, subclass, and background. The characters are stored in a JSON file, and the script also supports image optimization and Discord bot integration.

## Features

1. **Create Random Characters**: Generate a random character with random attributes.
2. **Create Specific Characters**: Create a character with specific attributes based on user input.
3. **Manage Characters**: Load existing characters from a JSON file, add new characters, and save them back to the file.
4. **Character Images**: Manage character images, including checking which characters have images and which do not.
5. **Discord Bot Integration**: Start a Discord bot (the bot's functionality is not detailed in this script).
6. **Optimize Images**: Optimize images in a specified directory.
7. **Archive Files**: Move files to an archive (the specifics of this functionality are not detailed in this script).

## Usage

Run the script in a Python environment. You will be presented with a menu of options:

```
Welcome to the RPG Character Generator!
1. Create random characters
2. Optimize images
3. Create a specific character
4. Archive files
5. Manage characters
6. Start the Discord bot
0. Exit the program
```

Enter the number of the option you want to choose.

## Dependencies

This script imports several modules, some of which are not included in the standard Python library:

- `json`
- `random`
- `os`
- `settings.random_settings`
- `models.character_class`
- `utils.image_optim`
- `discord_bot`

Please ensure that you have all necessary modules installed in your Python environment before running the script.

## Limitations

The script has a maximum limit of 9999 characters. If you try to create more characters than this, you will be asked to delete some characters before creating new ones.

## Contributing

Contributions to this script are welcome. Please fork the repository and create a pull request with your changes.

## License

This script is available under the [MIT License](https://opensource.org/licenses/MIT).