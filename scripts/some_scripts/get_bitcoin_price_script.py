# Импорты | Imports
import requests

# Узнать стоимость биткоина | Find out the value of bitcoin | Ermitteln Sie den Wert von bitcoin
response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')

bitcoin_price = response.json()['bitcoin']['usd']

# Просто функция для импорта | Just a function to import
def get_bitcoin_price():
    get_bitcoin = f"Value of bitcoin: ${bitcoin_price}"
    return get_bitcoin

# print на всякий случай | print just in case
print(get_bitcoin_price())