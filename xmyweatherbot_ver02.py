#импорт
import telebot
import pyowm
from telebot import types
#owm
owm = pyowm.OWM('b1c89f460a40430fd4a0214d984230ce',language='ru') 
# telebot
TOKEN='1129677508:AAEdpIa5SpUWam78lYud6rFyc2W-j4iVj5c'
bot=telebot.TeleBot(TOKEN)


#старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAPuXpNPjdOilp7Ja3mOu5T9S76S3CkAAiIBAAKmREgLEfW5zI8V9GYYBA')
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n----------------------------\nЯ - <b>{1.first_name}</b>, бот погоды)🌤\n----------------------------\nчтобы ознакомится с ботом⚙️-/help.".format(message.from_user, bot.get_me()),
        parse_mode='html')


#podpiska
@bot.message_handler(commands=['podpiska'])
def help(message):
    markup=telebot.types.InlineKeyboardMarkup()
    #кнопки калбек
    button1=telebot.types.InlineKeyboardButton(text='эждневная подписку✅', callback_data='den')
    button2=telebot.types.InlineKeyboardButton(text='еженедельная подписку✅', callback_data='nedelya')

    markup.add(button1)
    markup.add(button2)    
    
    bot.send_message(chat_id=message.chat.id, text='''
    этот бот находится в разработке⚙️🔧\n
    _______________________________________\n
    можете подписатся на еже-дневную/недельную подписку✅:''', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'den':
                bot.answer_callback_query(callback_query_id=call.id, text='подписка оформлена')
            elif call.data == 'nedelya':
                bot.answer_callback_query(callback_query_id=call.id, text='Hello оформлена')


#pogoda
@bot.message_handler(commands='pogoda')
def send_pogoda(message):
    try:
        bot.send_message(message.chat.id,'какой город?')
        place=message.text
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
        answer+='Скорость ветра окала '+str(wind)+' м/c'

    except pyowm.exceptions.api_response_error.NotFoundError:
      bot.send_message(message.chat.id, 'Город не найден :(')
  
       

















bot.polling()