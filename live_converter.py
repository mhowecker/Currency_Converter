from currency_converter import CurrencyConversion
import requests
import json

class LiveConverter(CurrencyConversion):
    def __init__(self):
        super().__init__()

    def get_courses(self, src: str, to: str) -> dict or None:
        url = "https://api.apilayer.com/currency_data/live?source={0}&currencies={1}".format(src, to)
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