from currency_converter import CurrencyConversion
import json

class StaticConverter(CurrencyConversion):
    def __init__(self):
        super().__init__()

    def get_courses(self, src: str, to: str) -> dict or None:
        f = open(".\live_list.json", "r")
        quotes = f.read()
        quotes = json.loads(quotes)
        conversion = quotes
        conversion['source'] = src
        quotes = quotes['quotes']
        to = to.split(',')
        
        if src == 'USD': from_quote = 1
        else: from_quote = quotes['USD'+src]
        amount_in_usd = 1 / from_quote

        to_quotes = dict()
        for x in to:
            if x != 'USD': to_quotes[src+x] = amount_in_usd*quotes['USD'+x]
            else: to_quotes[src+x] = amount_in_usd

        conversion['quotes'] = to_quotes
        return conversion