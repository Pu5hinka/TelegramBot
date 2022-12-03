import requests
import json
from confyg import keys


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось распознать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось распознать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать {amount}')
        if amount <= 0:
            raise APIException(f'Невозможно конвертировать количество валюты меньше или равное 0')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        if base_ticker == 'BTC':
            result = f'{(total_base * amount):.8f}'
            result = result.rstrip('0').rstrip('.') if '.' in result else result
        else:
            result = f'{(total_base * amount):.2f}'

        return result

