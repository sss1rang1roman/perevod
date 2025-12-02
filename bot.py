import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import token
from logic import *

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    help_text = """
 БОТ-ПЕРЕВОДЧИК + ОТВЕТЫ

 Что я умею:
1. Переводить текст (рус↔англ)
2. Отвечать на некоторые вопросы

💬 Примеры вопросов:
- как тебя зовут
- сколько тебе лет  
- привет / hello
- что ты умееш
- what can you do

Просто напиши мне что-нибудь!
    """
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user = message.from_user.username or str(message.from_user.id)
    TextAnalysis(message.text, user)
    
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton('🔄 ПЕРЕВОД', callback_data='translate'),
        InlineKeyboardButton('💬 ОТВЕТ', callback_data='answer')
    )
    
    bot.send_message(message.chat.id, f"📝: {message.text}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def button_click(call):
    user = call.from_user.username or str(call.from_user.id)
    
    if user not in TextAnalysis.memory or not TextAnalysis.memory[user]:
        bot.send_message(call.message.chat.id, "Напиши сначала сообщение!")
        return
    
    last_msg = TextAnalysis.memory[user][-1]
    
    if call.data == 'translate':
        bot.send_message(call.message.chat.id, f"🔄 Перевод:\n{last_msg.translation}")
    elif call.data == 'answer':
        bot.send_message(call.message.chat.id, f"💬 Ответ:\n{last_msg.response}")

print("🤖 Бот с ответами запущен!")
bot.infinity_polling()