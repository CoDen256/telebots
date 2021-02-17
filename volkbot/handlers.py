import telebot
import configparser
import random
from models import *

config = configparser.ConfigParser()
config.read("application.cfg", encoding="UTF-8")

triggers = config['BOT']['triggers'].split(",")
token = config['BOT']['token']
wolf_error = config['BOT']['error']
bot = telebot.TeleBot(token, threaded=False)
debug_id = 283382228

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(
        message.chat.id,
        text="WELCOME to VOLKBOT, these are some commands"
    )

    bot.send_message(
        message.chat.id,
        text="1./add {quote} - add new quote\n" + \
             "2./remove {index} - remove specified quote\n" + \
             "3./list - list of quotes with indexes\n"
    )


@bot.message_handler(commands=['add'])
def add(message):
    try:
        separated = message.text.replace("@volk_ne_lev_bot", "").split("/add")
        if not separated[1] or separated[1].isspace():
            bot.send_message(message.chat.id,
                             "Неверное значение для /add")
            return
        quote = Quote(value=separated[1].strip())
        quote.save()

        bot.send_message(message.chat.id, f"Выражение *{quote.value}* было успешно добавлено в лексикон волка",
                         parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, wolf_error)
        log(str(e))


@bot.message_handler(commands=['remove'])
def remove(message):
    try:
        add_user(message)
        separated = message.text.split("/remove")
        if not separated[1] or separated[1].isspace() or not separated[1].strip().isnumeric():
            bot.send_message(message.chat.id,
                             "Неверное значение для /remove")
            return

        quotes = sorted(list(Quote.all()), key=lambda x: x.value)
        n = int(separated[1].strip()) - 1
        if not (-1 <= n < len(quotes)):
            bot.send_message(message.chat.id,
                             "Неверный индекс цитаты.")
            return

        if n == -1:
            for quote in Quote.all():
                quote.delete()
            bot.send_message(message.chat.id, f"Все выражения волка были удалены.")
            return

        quote = quotes[n]
        quote.delete()

        bot.send_message(message.chat.id, f"Выражение *{quote.value}* было успешно забыто волком.",
                         parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.chat.id, wolf_error)
        log(str(e))


@bot.message_handler(commands=['list'])
def quotes_list(message):
    quotes = ""
    lists = sorted(Quote.all(), key=lambda x: x.value)
    if not lists:
        bot.send_message(message.chat.id, "Список цитат волка пуст. Волк молчит, а значит перебивать его не стоит.")
        return

        for i, quote in enumerate(lists):
            quotes += f"{i+1}. {quote.value}\n"
        bot.send_message(message.chat.id,
                         text=quotes)
    except Exception as e:
        bot.send_message(message.chat.id, wolf_error)
        log(str(e))
""" DAILY """
@bot.message_handler(commands=['quote_day'])
def quote_day(message):
    global last_quote_date
    try:
        add_user(message)
        delta = datetime.now() - last_quote_date

        quotes = list(User.objects.all())
        if not quotes:
            bot.send_message(message.chat.id, "Волк не говорит...А значит молчит.")
            return
        new_quote = None
        try:
            old_quote = Quote.objects.get(of_day=True)
            if delta.days >= 1:
                old_quote.of_day = False
                old_quote.save()

                last_quote_date = datetime.now()
                bot.send_message(message.chat.id, "Волк думает...")
                new_quote = random.choice(list(Quote.objects.all()))
                new_quote.of_day = True
                new_quote.save()
            else:
                new_quote = old_quote

        except Quote.DoesNotExist:
            bot.send_message(message.chat.id, "Волк думает...")
            last_quote_date = datetime.now()
            new_quote = random.choice(list(Quote.objects.all()))
            new_quote.of_day = True
            new_quote.save()

        bot.send_message(message.chat.id, f"Цитата дня - *{new_quote.value}*!", parse_mode='markdown')

    except Exception as e:
        bot.send_message(message.chat.id, wolf_error)
        log(str(e))

@bot.message_handler(commands=['wolf_day'])
def wolf_day(message):
    global last_wolf_date
    try:
        add_user(message)
        delta = datetime.now() - last_wolf_date
        user = None
        old_user = User.objects.get(of_day=True)

        if delta.days >= 1:
            old_user.of_day = False
            old_user.save()

            user = random.choice(list(User.objects.all()))
            user.of_day = True
            user.save()

            last_wolf_date = datetime.now()
            bot.send_message(message.chat.id, "Проводим анализ личностей...")
            time.sleep(2)
            bot.send_message(message.chat.id, "Советуемся с экспертами из цирка...")
            time.sleep(2)
            bot.send_message(message.chat.id, "Выбираем волка дня...")
            time.sleep(2)
        else:
            user = old_user
        bot.send_message(message.chat.id, f"Волк дня - {user.link}!", parse_mode='markdown')

    except Exception as e:
        bot.send_message(message.chat.id, wolf_error)
        log(str(e))

""" ANALYSERS """
@bot.message_handler(content_types=["text"])
def text_analyser(message):
    for trigger in triggers:
        if trigger in message.text:
            quotes = map(lambda x: x.value, Quote.all())
            if quotes:bot.send_message(message.chat.id, random.choice([quotes]))


""" DEBUG """


def log(id, text):
    bot.send_message(debug_id, text=f"{id}\n{text}")

bot.polling()