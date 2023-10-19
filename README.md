## Overview

This project is a Python-based implementation of a Language Model using OpenAI's GPT-3.5, designed to be used by a Telegram bot. The project consists of three main files and an environment variable configuration file (.env).

## Files

1. **.env.template**
   Create a file named `.env` by copying this template and filling in the necessary values for the environment variables.

   * `OPENAI_API_KEY`: Your OpenAI API key for accessing the language model.
   * `TELEGRAM_BOT_TOKEN`: Your Telegram bot's API token.
   * `LANGCHAIN_API_KEY`: Your LangChain API key if applicable.
2. **model.py**

   * Main file for training the Language Model using OpenAI.
   * Used to interact with the trained model.

   To use this file, make sure to configure your environment variables as specified in the `.env` file.
3. **train.py**

   * Training script that can be executed using the command `python train.py`.
   * Used for training your specific Language Model with OpenAI's GPT-3.5.
4. **telegram_bot.py**

   * Main file to activate the Telegram bot connected to the trained Language Model.
   * Run the Telegram bot using the command `python telegram_bot.py`.

## Getting Started

1. Clone this repository to your local machine:
   ```
   git clone https://github.com/KMRCrazyDuck/COR2221-AI---Humanity-Chatbot-Project.git
   ```
2. Create an `.env` file based on the provided `.env.template` and populate it with the necessary API keys and tokens.
3. Install the required Python dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Train the Language Model using `train.py`. 
5. Run the Telegram bot using `telegram_bot.py` to interact with the trained Language Model via Telegram.

## Usage

1. Ensure that the environment variables are correctly configured in the `.env` file.
2. Train the custom Language Model using `train.py` if needed.
3. Run the Telegram bot using `telegram_bot.py` to start interacting with the Language Model through Telegram.
