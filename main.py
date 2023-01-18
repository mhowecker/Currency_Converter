import sys
from PyQt6.QtWidgets import QApplication
import requests
import json
from datetime import datetime
import view
from static_converter import StaticConverter
from live_converter import LiveConverter

# Method for first contact with requests-package
def first_api_call():
    r = requests.get('https://api.github.com/events')
    return r.status_code


# Returns a json object containing a list with all available currencies
def list_currency():
    url = "https://api.apilayer.com/currency_data/list"
    payload = {}
    headers = {"apikey": "Fx0f20iPjLla4EikRT1P4e7SH1EbkuWl"}
    
    try:
        response = requests.request("GET", url, headers = headers, data = payload)
    except:
        return None
    if response.status_code == 200:
        return response.text
    else:
        return None


# Returns a json object containing information about the conversion from one to an another currency
def convert_currency(amount, from_c, to_c):
    url = "https://api.apilayer.com/currency_data/convert?to={0}&from={1}&amount={2}".format(to_c, from_c, amount)
    payload = {}
    headers = {"apikey": "Fx0f20iPjLla4EikRT1P4e7SH1EbkuWl"}

    try:
        response = requests.request("GET", url, headers = headers, data = payload)
    except:
        return None
    if response.status_code == 200:
        return response.text
    else:
        return None


# Returns a json object containing the conversion rates from one to x other currencies
# This Method uses live conversion rates
def live_currency(from_c, to_c):
    url = "https://api.apilayer.com/currency_data/live?source={0}&currencies={1}".format(from_c, to_c)
    payload = {}
    headers = {"apikey": "Fx0f20iPjLla4EikRT1P4e7SH1EbkuWl"}

    try:
        response = requests.request("GET", url, headers = headers, data = payload)
    except:
        return None
    if response.status_code == 200:
        return response.text
    else:
        return None


# Returns a json object containung all conversion rates from USD to every other available currency
def plain_live_currency():
    url = "https://api.apilayer.com/currency_data/live"
    payload = {}
    headers = {"apikey": "Fx0f20iPjLla4EikRT1P4e7SH1EbkuWl"}

    try:
        response = requests.request("GET", url, headers = headers, data = payload)
    except:
        return None
    if response.status_code == 200:
        return response.text
    else:
        return None


# Returns a json object containing the conversion rates from one to x other currencies
# This Method uses static conversion rates - last update 17.01.2023
def static_currency(from_c, to_c):
    f = open(".\live_list.json", "r")
    quotes = f.read()
    quotes = json.loads(quotes)
    conversion = quotes
    conversion['source'] = from_c
    quotes = quotes['quotes']
    to_c = to_c.split(',')
    
    if from_c == 'USD': from_quote = 1
    else: from_quote = quotes['USD'+from_c]
    amount_in_usd = 1 / from_quote

    to_quotes = dict()
    for x in to_c:
        if x != 'USD': to_quotes[from_c+x] = amount_in_usd*quotes['USD'+x]
        else: to_quotes[from_c+x] = amount_in_usd

    conversion['quotes'] = to_quotes
    return conversion


class Controller():
    def __init__(self):
        self.view = view.View(self)
    
    # Can be done with live or static data
    # For developing the static list was used because of limited API calls
    def get_currencies(self) -> list:
        #currencies = list_currency()
        f = open(".\currency_list.json", "r")
        currencies = f.read()
        currencies = json.loads(currencies)['currencies']
        cur = list()
        for c in currencies:
            cur.append(c)
        return cur
    
    # Converts an amount from on to x other currencies
    def convert(self, betrag: float, src: str, to: str, live:bool) -> dict:
        if live:
            conversion = LiveConverter().get_courses(src, to)
            if conversion is None: return None
            conversion = dict(json.loads(conversion))
        else:
            conversion = StaticConverter().get_courses(src, to)
        quotes = dict(conversion['quotes'])
        converted = dict()
        converted['betrag'] = betrag
        converted['date'] = datetime.fromtimestamp(conversion['timestamp'])
        converted['src'] = conversion['source']
        converted['converted'] = dict()
        for q in quotes:
            kurs = quotes[q]
            converted['converted'][q[3:]] = {'kurs': kurs, 'betrag_neu': kurs * betrag}
        
        return converted


if __name__ == '__main__':
    app = QApplication([])
    c = Controller()
    c.view.show()
    sys.exit(app.exec())
