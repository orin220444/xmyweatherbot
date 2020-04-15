#импорт
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
	load_dotenv(dotenv_path)

import telebot
import pyowm
from telebot import types
#owm
owm_key=os.getenv("OWM")
owm = pyowm.OWM(owm_key,language='ru')
# telebot
TOKEN=os.getenv("BOT_TOKEN")
bot=telebot.TeleBot(TOKEN)


#старт
@bot.message_handler(commands=['start'])
def start(message):
    sticker = 'CAACAgIAAxkBAAPuXpNPjdOilp7Ja3mOu5T9S76S3CkAAiIBAAKmREgLEfW5zI8V9GYYBA'
    answer = """Добро пожаловать, {0.first_name}!
----------------------------
Я - <b>{1.first_name}</b>, бот погоды)🌤
----------------------------
чтобы ознакомится с ботом⚙️-/help."""
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, answer.format(message.from_user, bot.get_me()),
        parse_mode='html')


#podpiska
@bot.message_handler(commands=['podpiska'])
def help(message):
    markup=telebot.types.InlineKeyboardMarkup()
    #кнопки калбек
    button1=telebot.types.InlineKeyboardButton(text='ежедневная подписка✅', callback_data='den')
    button2=telebot.types.InlineKeyboardButton(text='еженедельная подписка✅', callback_data='nedelya')

    markup.add(button1)
    markup.add(button2)
    answer='''
этот бот находится в разработке⚙️🔧\n
_______________________________________\n

можете подписаться на ежедневную/еденедельную подписку✅:'''
    bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'den':
                bot.answer_callback_query(callback_query_id=call.id, text='подписка оформлена')
            elif call.data == 'nedelya':
                bot.answer_callback_query(callback_query_id=call.id, text='подписка оформлена')

    except:
	       bot.send_message(message.chat.id, 'Ошибка!')
#pogoda
@bot.message_handler(commands=['pogoda'])
def observation_request(message):
    try:
        bot.send_message(message.chat.id,'какой ваш город?')
        @bot.message_handler(func=lambda m: True)
        def send_pogoda(message):
            try:
                place=message.text
                print(place)
                observation = owm.weather_at_place(place)
                w = observation.get_weather()
                #переменная скорости ветра
                wind=w.get_wind ()['speed']
                #переменная влажности
                humi=w.get_humidity ()
                #переменная температуры
                tem=w.get_temperature('celsius')['temp']

                #сведения о погоде
                answer='сейчас в '+place+' '+w.get_detailed_status()+'\n'
                answer+='Температура около '+str(tem)+' c°'+'\n'
                answer+= 'Влажность воздуха около '+str(humi)+' %'+'\n'
                answer+='Скорость ветра около '+str(wind)+' м/c'

                bot.send_message(message.chat.id, answer)
            except pyowm.exceptions.api_response_error.NotFoundError:
                bot.send_message(message.chat.id, 'Город не найден :(')
    except:
        bot.send_message(message.chat.id, 'Ошибка!')

















bot.polling()
