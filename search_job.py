# coding: utf-8


import json
import os
import requests
import telegram
import time
from dotenv import load_dotenv
from datetime import datetime
from dateutil import parser

load_dotenv()

hh_token = os.getenv('HH_TOKEN')


def get_job(current_timestamp1, current_timestamp2):
    """Функция получает на вход 2 даты и проверяет есть ли в указанном
    временном диапазоне вакансии на hh.
    Если такие есть, то отправляет их в телеграмм."""

    url = "https://api.hh.ru/vacancies/"
    params = {
        "Authorization": f"Bearer {hh_token}",
        "text": "python",
        "area": get_area("Самара"),
        "describe_arguments": True,
        "period": 1,
    }
    answer = requests.get(url, params=params)
    for i in answer.json()["items"]:
        date_search = parser.parse(i["published_at"]).timestamp()
        if (date_search > current_timestamp1 and
                date_search < current_timestamp2):
            name = i["name"]
            url = i["apply_alternate_url"]
            message = name + '\n' + url
            send_message(message)

    return


def send_message(message):
    """ Функция для отправки сообщения в телеграмм"""
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    return bot.sendMessage(chat_id=CHAT_ID, text=message)


def get_area(city):
    url = "https://api.hh.ru/suggests/areas/"
    params = {
        "Authorization": f"Bearer {hh_token}",
        "text": city,
    }
    answer = requests.get(url, params=params)
    return answer.json()["items"][0]["id"]


def main():
    current_timestamp1 = 1587752745
    current_timestamp2 = 1613318183
    while True:
        try:
            get_job(current_timestamp1, current_timestamp2)
            time.sleep(300)  # опрашивать раз в пять минут
            current_timestamp1 = current_timestamp2
            current_timestamp2 = datetime.now().timestamp()
        except Exception as e:
            print(f"Бот упал с ошибкой: {e}")
            time.sleep(300)
            continue


if __name__ == "__main__":
    main()
