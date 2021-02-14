import os
import requests
import telegram
import time
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
from dateutil import parser

load_dotenv()


def get_job(current_timestamp1, current_timestamp2, dict_job={}):

    Client_ID = os.getenv("Client_ID")
    Client_Secret = os.getenv("Client_Secret")
    headers = {"Authorization": f"OAuth {Client_Secret}"}

    url = "https://api.hh.ru/vacancies/"
    params = {
        "Authorization": "Bearer LFSRA3UJQAEGD4R0TJL6FQHJN5JA1ODEAM54GGF37DOC8DLCPE4V7VS55FHOOEQP",
        "text": "python",
        "area": get_area("Самара"),
        "describe_arguments": True,
        "period": 1,
    }
    answer = requests.get(url, params=params)
    for i in answer.json()["items"]:
        date_search = parser.parse(i["published_at"]).timestamp()
        if date_search > current_timestamp1 and date_search < current_timestamp2:
            name = i["name"]
            url = i["apply_alternate_url"]
            name = name.encode().decode()
            url = url.encode().decode()
            dict_job[i["published_at"]] = [name, url]
            send_message(dict_job[i["published_at"]])
    return


def send_message(message):
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    return bot.sendMessage(chat_id=CHAT_ID, text=message)


def get_acsess_token():
    Client_ID = os.getenv("Client_ID")
    Client_Secret = os.getenv("Client_Secret")
    url = "https://hh.ru/oauth/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": Client_ID,
        "client_secret": Client_Secret,
    }
    answer = requests.post(url, params=params)
    return answer.json()


def get_area(city):
    url = "https://api.hh.ru/suggests/areas/"
    params = {
        "Authorization": "Bearer LFSRA3UJQAEGD4R0TJL6FQHJN5JA1ODEAM54GGF37DOC8DLCPE4V7VS55FHOOEQP",
        "text": city,
    }
    answer = requests.get(url, params=params)
    return answer.json()["items"][0]["id"]


def main():
    current_timestamp1 = 1587752745
    current_timestamp2 = 1613318183
    while True:
        try:
            new_homework = get_job(current_timestamp1, current_timestamp2)
            time.sleep(300)  # опрашивать раз в пять минут
            current_timestamp1 = current_timestamp2
            current_timestamp2 = datetime.now().timestamp()
        except Exception as e:
            print(f"Бот упал с ошибкой: {e}")
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()
