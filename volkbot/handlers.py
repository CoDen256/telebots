import telebot
import random
from django.conf import settings
from main.models import Quote

triggers = ["волк", "цирк", "сильнее", "лев", "льва"]

bot = telebot.TeleBot(settings.TOKEN, threaded=False)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        text="WELCOME to VOLKBOT, these are some commands"
    )

    bot.send_message(
        message.chat.id,
        text="1./add {quote} - add new quote\n"+\
             "2./remove {index}\n - remove specified quote" + \
             "3./list - quotes with indexes\n"
    )

@bot.message_handler(commands=['add'])
def add(message):
    separated = message.text.split("/add")
    if not separated[1] or separated[1].isspace():
        bot.send_message(message.chat.id,
                         "Incorrect value for /add")
        return
    quote = Quote(value=separated[1].strip())
    quote.save()

@bot.message_handler(commands=['remove'])
def remove(message):
    separated = message.text.split("/remove")
    if not separated[1] or separated[1].isspace() or not seprated[1].strip().isnum():
        bot.send_message(message.chat.id,
                         "Incorrect value for /remove")
        return

    n = int(separated[1].strip()) - 1
    if not (0 <= n < len(quotes)):
        bot.send_message(message.chat.id,
                        "The index is out of range")
        return

    quotes = Quote.objects.all().sort(key=lambda x: x.value)
    quote = quotes[n]
    quote.delete()


@bot.message_handler(commands=['list'])
def quotes_list(message):
    quotes = ""
    lists = Quote.objects.all().sort(key=lambda x: x.value)
    if not lists:
        bot.send_message(message.chat.id, "List is empty.")

    for i, quote in enumerate(lists):
        quotes += f"{i+1}.{quote.value}\n"
    bot.send_message(message.chat.id,
                     text=quotes)

@bot.message_handler(content_types=["text"])
def text_analyser(message):
    for trigger in triggers:
        if trigger in message.text:
            quotes = map(Quote.objects.all(), lambda x: x.value)
            if quotes:
                bot.send_message(message.chat.id, random.choice([quotes]))


""" DEBUG """
def log(id, text):
    bot.send_message(283382228, text=f"{id}\n{text}")