import json
import os
import telebot
import re
with open("config.json", 'r') as file:
    tk = json.load(file)
bot = telebot.TeleBot(tk['TOKEN'])

# @bot.message_handler(content_types=['text'])
# def get_text_message(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.from_user.id,"Привет, чем помочь?")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши привет")
#     else:
#         bot.send_message(message.from_user.id, 'Я тебя не понимаю, напиши "Привет" ')


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Здравствуйте, этот бот реализует переадресацию')


@bot.message_handler(commands=['reg'])
def start_command(message):
    bot.send_message(message.from_user.id, "Введите номер для переадресации")
    bot.register_next_step_handler(message, get_phone)

@bot.message_handler(commands=['stop'])
def start_command(message):
    bot.send_message(message.from_user.id, "Досрочно снимаю переадресацию")
    os.system(f'python cancel_ph.py')
    bot.send_message(message.from_user.id,"Переадресация снята")

@bot.message_handler(func = lambda m: True)
def echo_all(message):
    bot.reply_to(message, "Я не понимаю, я пока знаю такие комманды как /start & /reg")


def get_phone(message):
    print(message.text)
    phone_ch = message.text
    ch_tel = ''.join(c for c in phone_ch if c.isdigit())
    try:
        if ch_tel[0] == '7':
            ch_tel = ch_tel[1:]
    except IndexError:
        pass
    if len(ch_tel) == 10:
        bot.send_message(message.from_user.id, f"Номер для переадресации {ch_tel} принят")
        os.system(f'python main.py {ch_tel}')
        bot.send_message(message.from_user.id, f"переадресация {phone_ch} выполнена")
        bot.send_message(message.from_user.id, 'Введите дату окончания переадресации, в формате yyyy-mm-dd hh:mm')
        bot.register_next_step_handler(message, get_date)
    else:
        bot.send_message(message.from_user.id, 'Не верно задан номер телефона')

def get_date(message):
    print(message.text)
    print(len(message.text))
    if re.match(r'(^([2]?[0]?[2]?[1-9]?)-(\d\d)-(\d\d) (\d\d):(\d\d)$)', message.text) and len(message.text) == 16:
        get_data(message)
        bot.send_message(message.from_user.id, 'Дата окончания установлена')
    else:
        bot.send_message(message.from_user.id, 'не правильный формат даты, повторите ввод даты в формате yyyy-mm-dd hh:mm')
        bot.register_next_step_handler(message, get_date)


def get_data(message):
    print(message.text)
    with open ('client.txt', 'w') as file:
        file.write(f'{message.text};{message.from_user.id}')


bot.polling(none_stop=True, interval=0)