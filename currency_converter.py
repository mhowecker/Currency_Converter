from abc import ABC

class CurrencyConversion(ABC):
    def __init__(self):
        pass

    def get_courses(self, src:str, to:str) -> dict or None:
        pass


