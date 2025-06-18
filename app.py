import asyncio

import requests
from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


async def translate(text):
    translator = Translator()
    result = await translator.translate(text, src="en", dest="ru")
    return result.text


### asyncio.run(translate(english_words))

def get_zenquotes(headers):
    url = "https://zenquotes.io/api/random"
    response = requests.get(url, headers=headers)
    if response.status_code == requests.codes.ok:
        data = response.json()[0]
        data.update({'t': asyncio.run(translate(data['q']))})
        return data


def get_api_ninjas(headers: dict) -> dict:
    api_url = 'https://api.api-ninjas.com/v1/quotes'
    merged_headers = {
        **headers,  # User-Agent, Accept…
        'X-Api-Key': 'lHH+5taLAKpAmM2a0RATcQ==QZd3XVHARzcKNHx6',  # API-ключ
    }
    response = requests.get(api_url, headers=merged_headers)
    if response.status_code == requests.codes.ok:
        data = response.json()[0]
        data.update({'translate': asyncio.run(translate(data['quote']))})
        return data


def get_quoteslate(HEADERS):
    url = "https://quoteslate.vercel.app/api/quotes/random?count=5"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == requests.codes.ok:
        raw_data = response.json()
        # пересобираем список, добавляя перевод
        data = [
            {**q, 'translate': asyncio.run(translate(q['quote']))}
            for q in raw_data
        ]
        return (data)  # вот здесь data уже с переводами


@app.route('/', methods=['GET', 'POST'])
def index():
    zenquotes = api_ninjas = quoteslate = None
    if request.method == 'POST':
        zenquotes = get_zenquotes(HEADERS)
        api_ninjas = get_api_ninjas(HEADERS)
        quoteslate = get_quoteslate(HEADERS)
    return render_template('index.html', zenquotes=zenquotes, api_ninjas=api_ninjas, quoteslate=quoteslate)


if __name__ == '__main__':
    app.run(debug=True)
