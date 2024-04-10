import telebot

from service.environment import environmental_variables

bot = telebot.TeleBot(environmental_variables.BOT_TOKEN)


def send_alert(message: str):
    for chat_id in environmental_variables.CHAT_IDS.split(','):
        try:
            bot.send_message(chat_id, message)
        except Exception as e:
            print(e)
