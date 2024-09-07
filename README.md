
# Discord Nuke Bot

This repository contains two versions of a Discord Nuke Bot that automates mass deletion of roles, channels, banning members, and more. It also includes features like a **user whitelist** and **progress bar** to track the status of the operations.

- Python Version: Uses `discord.py`
- Node.js Version: Uses `discord.js`

> **Warning:** This bot is designed for destructive purposes (mass deletion of Discord server entities). Use it responsibly, only in servers where you have explicit permission.

## Features

- Delete all channels, roles, and emojis.
- Ban or kick all members (except bots and whitelisted users).
- Delete invites, webhooks, and emojis.
- Spam a message in a newly created channel.
- Lock down all channels.
- Progress bar to monitor operation status in the console.
- User whitelist to exempt certain users from banning or kicking.

## Requirements

Both versions of the bot have different requirements based on the programming language.

### Python Version (`discord.py`)

#### Prerequisites

- Python 3.8+
- Install the required dependencies:

```bash
pip install discord.py tqdm
```

#### Running the Python Bot

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/discord-nuke-bot.git
    cd discord-nuke-bot
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `token.txt` file in the root directory and add your bot token inside, or enter it when prompted.

4. Run the bot:

    ```bash
    python bot.py
    ```

5. The bot will prompt you for the **Server ID** and a **nuke option** to execute. Follow the instructions in the console to proceed.

### Node.js Version (`discord.js`)

#### Prerequisites

- Node.js 16.6.0 or higher
- Install the required dependencies:

```bash
npm install
```

#### Running the Node.js Bot

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/discord-nuke-bot.git
    cd discord-nuke-bot
    ```

2. Install the dependencies:

    ```bash
    npm install
    ```

3. Create a `token.txt` file in the root directory and add your bot token inside, or enter it when prompted.

4. Run the bot:

    ```bash
    node bot.js
    ```

5. The bot will prompt you for the **Server ID** and a **nuke option** to execute. Follow the instructions in the console to proceed.

## Nuke Options

When you run the bot, you will be prompted to select one of the following options:

1. Nuke all (without kicking members)
2. Delete channels
3. Delete roles
4. Ban members
5. Kick members
6. Delete emojis
7. Delete server (reset server name and icon)
8. Delete invites
9. Delete webhooks
10. Spam message
11. Lockdown channels

## Whitelist Feature

You can exempt specific users from being banned or kicked by adding their user IDs to the `WHITELIST` array in the code. This feature is present in both the Python and Node.js versions.

```python
# Python version whitelist
WHITELIST = [
    123456789012345678,  # Replace with actual user IDs
]
```

```javascript
// Node.js version whitelist
const WHITELIST = [
    '123456789012345678',  // Example User ID
];
```

## Logging

Both versions of the bot log the results of each operation to a log file, which will be created in the root directory, named with the current date and time.

## Contribution

Feel free to contribute to this project. If you encounter any issues, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer

This bot is for educational and testing purposes only. The authors are not responsible for any misuse of this bot.
