import os
import telegram
import requests
import logging
from bs4 import BeautifulSoup
from telegram.ext import CommandHandler

bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

def get_random_miejski():
    url = 'https://www.miejski.pl/losuj'

    page = requests.get(url)

    html_text = page.text
    soup = BeautifulSoup(html_text, 'html.parser')

    first_article = soup.find_all('article')[0]
    title = first_article.find('h1').text
    desc = first_article.find('p').text
    example = first_article.find('blockquote').text

    print(f"**title**")
    print(f"Opis: ```{desc}```")
    print(f"Przykład: ```{example}```")

    return "*{}*\n\nOpis:```\n{}\n```\nPrzykład:```\n{}\n```".format(title, desc, example)

def webhook(request):
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        entry = get_random_miejski()
        bot.sendMessage(chat_id=chat_id, text=entry, parse_mode="MarkdownV2")
    return entry
