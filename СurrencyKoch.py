import telebot
from confyg import keys, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Я твой бот-конвертер валют и вот что умею: \n\
показывать списки доступных для конвертации валют /values \n\
конвертировать валюты, для этого необходимо \n\
ввести команду: <из какой валюты> <в какую валюту> <количество>'
    bot.reply_to(message, f'Привет, {message.chat.username}!\n' + text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(commands=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Хм, что-то пошло не так с {e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
