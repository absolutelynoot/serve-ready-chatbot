import telebot
import os
from dotenv import load_dotenv
import model

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
bot.set_webhook()

# Dictionary to store conversation history
conversation_history = {}


@bot.message_handler(commands=['start'])
def start(message):
    """
    Bot will introduce itself upon /start command, and prompt user for his request
    """
    try:
        # Start bot introduction
        start_message = "Hello! I'm Serve Ready Bot! Ask me anything about HealthServe onboarding, or if you need help!"
        bot.send_message(message.chat.id, start_message)

    except Exception as e:
        bot.send_message(
            message.chat.id, 'Sorry, something seems to gone wrong! Please try again later!')


@bot.message_handler(content_types=['text'])
def send_text(message):

    # Retrieve the user id and the message from telegram API
    user_id = message.from_user.id
    question = message.text

    # Retrieve the conversation history for the user
    chat_history = conversation_history.get(user_id, [])

    #  Get the response from the model
    response = model.getResponse(question, chat_history)

    # Add the model's response to the conversation history
    chat_history.append((question, response['answer']))

    print("====== chat history =======")
    print(chat_history)

    # Store the updated conversation history for the user
    conversation_history[user_id] = chat_history

    bot.send_message(message.chat.id, response['answer'])

def main():
    """Runs the Telegram Bot"""
    print('Successfully loaded! Starting bot...')
    bot.infinity_polling()


if __name__ == '__main__':
    main()
