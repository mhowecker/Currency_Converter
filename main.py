import sys
from PyQt6.QtWidgets import QApplication
import requests
import json
from datetime import datetime
import view


def first_api_call():
    r = requests.get('https://api.github.com/events')
    return r.status_code


def list_currency():
    url = "https://api.apilayer.com/currency_data/list"
    payload = {}
    headers = {"apikey": "Fx0f20iPjLla4EikRT1P4e7SH1EbkuWl"}
    
    response = requests.request("GET", url, headers = headers, data = payload)
    return response.text
    if response.status_code == 200:
        return response.json
    else:
        return response.status_code


def convert_currency(amount, from_c, to_c):
    url = "https://api.apilayer.com/currency_data/convert?to={0}&from={1}&amount={2}".format(to_c, from_c, amount)
    payload = {}
    headers = {"apikey": "Fx0f20iPjLla4EikRT1P4e7SH1EbkuWl"}

    response = requests.request("GET", url, headers = headers, data = payload)
    return response.text
    if response.status_code == 200:
        return response.json
    else:
        return response.status_code


def live_currency(from_c, to_c):
    url = "https://api.apilayer.com/currency_data/live?source={0}&currencies={1}".format(from_c, to_c)
    payload = {}
    headers = {"apikey": "Fx0f20iPjLla4EikRT1P4e7SH1EbkuWl"}

    response = requests.request("GET", url, headers = headers, data = payload)
    return response.text
    if response.status_code == 200:
        return response.json
    else:
        return response.status_code


class Controller():
    def __init__(self):
        #self.model = model.Spiel()
        self.view = view.View(self)
    
    def get_currencies(self) -> list:
        #currencies = list_currency()
        f = open(".\currency_list.json", "r")
        currencies = f.read()
        currencies = json.loads(currencies)['currencies']
        cur = list()
        for c in currencies:
            cur.append(c)
        return cur
    
    def convert(self, betrag: float, src: str, to: str) -> dict:
        conversion = live_currency(src, to)
        conversion = dict(json.loads(conversion))
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
    #print(live_currency("EUR", "USD,CHF,DKK"))
    #print(convert_currency("10", "EUR", "CHF"))
    #list_currency())

    
    app = QApplication([])
    c = Controller()
    c.view.show()
    sys.exit(app.exec())
