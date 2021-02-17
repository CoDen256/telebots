import telebot
from antonyms import get_antonym_for_word, demotivate_sentence, write_to_template, filename, get_synonym_for_word
from image_generator import generate_demotivator_image

TOKEN = "1301791952:AAHOFxIT4merFrPrWtY1HbvRW8vU7uclLYQ"
bot = telebot.TeleBot(TOKEN, threaded=False)
bot.send_message(283382228, "Starting demotivator-bot...")

error = "Ой мне поплохело...\n"


@bot.message_handler(commands=['start', 'help'])
def start(message):
    try:
        bot.send_message(
            message.chat.id,
            text="Добро пожаловать в *Демотиватор-бота*\nЭто базовые комманды для управления волком.",
            parse_mode='markdown'
        )

        bot.send_message(
            message.chat.id,
            text="/demotivate {quote} - Демотивирует цитату.\n" + \
                 "/add {key} {value} - Добавляет демотивирующую цитату.\n"
        )
    except Exception as e:
        bot.send_message(message.chat.id, error)
        log(str(e))


@bot.message_handler(commands=['demotivate'])
def demotivate(message):
    try:
        separated = message.text.split("/demotivate")
        words = separated[1].strip().split()

        original = " ".join(words)
        demotivated = "нет блять, " + demotivate_sentence(words)
        bot.send_message(message.chat.id, demotivated, parse_mode='markdown')

        generate_demotivator_image(original, demotivated)

        image = open('result.jpg', 'rb')
        bot.send_photo(message.chat.id, image)

    except Exception as e:
        bot.send_message(message.chat.id, error + str(e))
        log(str(e))


@bot.message_handler(commands=['add'])
def demotivate(message):
    try:
        separated = message.text.split("/add")
        key_value = separated[1].strip().split()
        key = key_value[0]
        value = key_value[1]

        write_to_template(filename, key, value)

        bot.send_message(message.chat.id, key + "=" + value + " is added", parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, error + str(e))
        log(str(e))


@bot.message_handler(commands=['synonym'])
def demotivate(message):
    try:
        separated = message.text.split("/synonym")
        word = separated[1]

        bot.send_message(message.chat.id, "\n".join(get_synonym_for_word(word)), parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, error + str(e))
        log(str(e))

@bot.message_handler(commands=['antonym'])
def demotivate(message):
    try:
        separated = message.text.split("/antonym")
        word = separated[1]

        bot.send_message(message.chat.id, "\n".join(get_antonym_for_word(word)), parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, error + str(e))
        log(str(e))

""" DEBUG """


def log(text):
    bot.send_message(283382228, text=f"{text}")


bot.polling()
