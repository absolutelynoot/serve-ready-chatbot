import telebot
from telegram.constants import ParseMode
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

        # Retrieve user information
        user_info = bot.get_chat(message.from_user.id)

        # Extract the user's first name
        username = user_info.first_name
    
        start_message = (
f"""\
*Hi {username}*, I am Serve Ready Chat bot Bot 🤖 powered by OpenAI's Large Language Model GPT!

I'm here to assist you with various tasks, including:

1. Background and Services of HealthServe
I can provide information about HealthServe and the services it offers.

2. Cultural Understanding of Migrant Workers
I can help you better understand the cultures and backgrounds of migrant workers.

3. Situational Awareness
I can offer tips on situational awareness when working with migrant workers.

4. Personal Data Protection Act
I can provide information and clarifications related to PDPA (Personal Data Protection Act).

You can also clear the message history at any time to get a fresh answer. Simply type _'Clear Message History'_.

Feel free to ask any questions or request assistance with the topics mentioned above, and I'll do my best to help!

To share this bot with others, use this link: [ServeReadyBot](https://t.me/ServeReadyBot)
""")

        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        item = telebot.types.KeyboardButton('Clear Message History')
        markup.add(item)
        bot.send_message(message.chat.id, start_message, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)


    except Exception as e:
        bot.send_message(
            message.chat.id, 'Sorry, something seems to gone wrong! Please try again later!')


@bot.message_handler(func=lambda message: message.text == 'Clear Message History')
def clear_history(message):
    """
    Function to clear the message history for the user.
    """
    user_id = message.from_user.id
    conversation_history[user_id] = []
    bot.send_message(message.chat.id, 'Your Message history has been successfully cleared 😄.')

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
