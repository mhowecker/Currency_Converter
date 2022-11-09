import sys
from PyQt6.QtWidgets import QApplication
import requests
import json
import view


class Controller():
    def __init__(self):
        #self.model = model.Spiel()
        self.view = view.View(self)
    
    def get_currencies(self):
        #currencies = list_currency()
        f = open(".\currency_list.json", "r")
        currencies = f.read()
        currencies = json.loads(currencies)['currencies']
        cur = list()
        for c in currencies:
            cur.append(c)
        return cur
    
    def convert(self, betrag: float, src: str, to: str):
        conversion = live_currency(src, to)
        print(type(conversion))
        conversion = json.dumps(conversion)['quotes']
        print(type(conversion))
        print(conversion)


def first_api_call():
    r = requests.get('https://api.github.com/events')
    return r.status_code


def list_currency():
    url = "https://api.apilayer.com/currency_data/list"
    payload = {}
    headers = {"apikey": "Fx0f20iPjLla4EikRT1P4e7SH1EbkuWl"}
    
    response = requests.request("GET", url, headers = headers, data = payload)
    #return response.text
    if response.status_code == 200:
        return response.json
    else:
        return response.status_code


def convert_currency(amount, from_c, to_c):
    url = "https://api.apilayer.com/currency_data/convert?to={0}&from={1}&amount={2}".format(to_c, from_c, amount)
    payload = {}
    headers = {"apikey": "Fx0f20iPjLla4EikRT1P4e7SH1EbkuWl"}

    response = requests.request("GET", url, headers = headers, data = payload)
    #return response.text
    if response.status_code == 200:
        return response.json
    else:
        return response.status_code


def live_currency(from_c, to_c):
    url = "https://api.apilayer.com/currency_data/live?source={0}&currencies={1}".format(from_c, to_c)
    payload = {}
    headers = {"apikey": "Fx0f20iPjLla4EikRT1P4e7SH1EbkuWl"}

    response = requests.request("GET", url, headers = headers, data = payload)
    #return response.text
    if response.status_code == 200:
        return response.json
    else:
        return response.status_code

if __name__ == '__main__':
    #print(live_currency("EUR", "USD,CHF,DKK"))
    #print(convert_currency("10", "EUR", "CHF"))
    #list_currency())

    
    app = QApplication([])
    c = Controller()
    c.view.show()
    sys.exit(app.exec())
