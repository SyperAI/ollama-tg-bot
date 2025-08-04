# ATTENTION! The bot is in active development, in connection with which many of its components, including the architecture of the database may change!

# Ollama Telegram Bot 🦙🤖
ОThe real goal of this project is to implement a full-fledged interface of interaction with Ollama with the functionality of similar
on [Open WebUI](https://github.com/open-webui/open-webui) in the form of Telegram bot

## Key features ✨
1. [x] Chats - support for full-fledged dialogues with retention of their components and the ability to re-engage at any time.
   1. [x] Dynamic response - ability to stream responses in real time.
   2. [ ] System prompt - ability to set a separate system prompt for the current chat.
   3. [ ] Multi-model - ability to dynamically switch models within a single chat.
   4. [ ] Media input - ability to pass various types of media to the model.
   5. [ ] Image generation - ability to generate images directly from the dialogue using Stable Diffusion.
2. [ ] User settings - ability for each user to customize the bot to their preferences.
   1. [ ] Custom system prompt - ability to set a default system prompt.
   2. [ ] Language - ability to change the bot interface language.
3. [ ] Admin settings - ability to configure global bot settings and interact with ollama.
   1. [ ] Models - interaction with ollama to install and remove models; setting a default model for users.
   2. [ ] Options - configuration of options to be passed directly to the model via the bot interface.
   3. [ ] Users - user blocking/assigning user as administrator.

## Prerequisites ⚙️
1. **Install [Python](https://www.python.org/downloads/):** version 3.11 is recommended
2. **Install [MariaDB](https://mariadb.org/download/)**
3. **Create [Telegram Bot](https://core.telegram.org/bots#how-do-i-create-a-bot) and obtain bot token**

## How to Install 🚀
1. **Clone Repository:**<br>
    ```bash
    git clone https://github.com/SyperAI/ollama-tg-bot.git
    ```
2. **Go to Repository dir:**
    ```bash
   cd ollama-tg-bot
   ```
3. **Create python virtual environment:**
    ```bash
   python -m venv venv
   ```
4. **Activate python virtual environment:**
    ```bash
   source venv/bin/activate
   ```
5. **Install python requirements:**
    ```bash
   pip install -r requirements.txt
   ```
6. **Launch bot:**
    ```bash
   python main.py
   ```
   
> [!NOTE]
> On first launch config.ini file will be created and then bot will exit. Fill it and launch again.

> [!NOTE]
> After first success launch you will need to start bot from account with id which you entered `admin_id` filed, then after bot restart you will receive admin rights for that account.

> [!WARNING]
> Running on linux server without using `screen` utility may require manual termination of the process.