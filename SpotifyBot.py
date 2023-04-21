import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot import types
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from io import BytesIO
import requests


bot = telebot.TeleBot('TOKEN')

keyboard = InlineKeyboardMarkup()
button = InlineKeyboardButton(text="🔎 Начать поиск 🔎", callback_data="start_search")
button1 = InlineKeyboardButton(text="📧 Связь с разработчиком 📧", callback_data="write_developer")
button2 = InlineKeyboardButton(text="🎁 Исходники 🎁", callback_data="source_code")
keyboard.add(button)
keyboard.add(button1)
keyboard.add(button2)

keyboard1 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text="❌ Отменить ❌", callback_data="about")
keyboard1.add(button3)

keyboard2 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text="❌ Отменить ❌", callback_data="about")
button_url = InlineKeyboardButton(text='📧 Написать разработчику 📧', url='https://t.me/Codefer')
button4 = InlineKeyboardButton(text="📝Популярные вопросы📝", callback_data="quections")
keyboard2.add(button_url)
keyboard2.add(button4)
keyboard2.add(button3)

client_id = 'client_id'
client_secret = 'client_secret'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "<b>Здравствуй!\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\nЯ - бот, который найдет тебе трек.\nВсе, что мне нужно - это название трека.\nВыполняю поиск по сервису Spotify. Бесплатно, быстро и четко :)\n_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _</b>", parse_mode ='HTML', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "start_search")
def handle_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>📎Напишите навзание трека</b>", parse_mode ='HTML',reply_markup=keyboard1)

@bot.callback_query_handler(func=lambda call: call.data == "write_developer")
def handle_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>У вас есть вопросы к разработчику?\nВы можете почитать самые интересующие вопросы или связаться с разработчком.\nНажми на кнопки ниже:</b>", parse_mode ='HTML', reply_markup=keyboard2)

@bot.callback_query_handler(func=lambda call: call.data == "source_code")
def handle_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>Исходный код пока недоступен.\nСо временем появиться.</b>", parse_mode ='HTML',reply_markup=keyboard1)

@bot.callback_query_handler(func=lambda call: call.data == "about")
def handle_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="<b>Отменено</b>", parse_mode ='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "quections")
def handle_callback(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Популярные вопросы:\n1. Почему треки не длинее 30 сек?\nОтвет: Не знаю. Это дело работы Spotify, они предоставляют боту ваши искомые треки. Это зависит от них, а не от бота.\n2. Мой трек не находиться!\nОтвет: Скорее всего, твой трек отсутствует в базе Spotify.",reply_markup=keyboard1)

@bot.message_handler(func=lambda message: True)
def search_track(message):
    bot.reply_to(message, "🔎")
    results = sp.search(message.text, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_name = track['name']
        track_artist = track['artists'][0]['name']
        track_url = track['external_urls']['spotify']
        reply_text = f"Трек: {track_name}\nАртист: {track_artist}\nСсылка: {track_url}"
        bot.reply_to(message, reply_text)
        track_preview_url = track['preview_url']
        if track_preview_url:
            response = requests.get(track_preview_url)
            bot.reply_to(message, "<b>✅ Ваш запрос.\nТрек найден!</b>", parse_mode ='HTML')
            track_file = BytesIO(response.content)
            track_file.name = f"{track_name} - {track_artist}.mp3"
            bot.send_audio(message.chat.id, track_file)

        else:
            reply_text = f"Трек: {track_name}\nАртист: {track_artist}\nСсылка: {track_url}"
            bot.reply_to(message, reply_text)

    else:
        bot.reply_to(message, "<b>❌ К сожелению трек по вашему запросу я не смог найти.</b>", parse_mode ='HTML')


bot.polling()