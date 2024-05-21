# NotesBot

AiogramNotesBot is a Telegram bot developed using the aiogram and aiogram-dialog libraries. It provides users with the ability to create and manage notes, as well as interact with the bot through a dialog interface.

## Features

- **Create and manage notes**: Users can create new notes, view a list of existing notes, and delete them.
  
- **Dialog interface**: aiogram-dialog is used to implement a dialog interface, making interaction with the bot more convenient and intuitive.
  
- **Localization in multiple languages**: The bot supports localization in English and Russian languages using the fluentogram library.

- **Use of Redis for data storage**: The bot uses the Redis database to store notes and other data.

## Installation and Usage

1. Install the necessary dependencies by running the command:
    ```bash
    pip install -r requirements.txt
    ```
2. Create a .env file and fill it as specified in the .env.example
3. Run the bot by executing the command:
    ```bash
   python main.py
    ```

## License

This project is licensed under the terms of the MIT license. For more details, see the [LICENSE](LICENSE) file.