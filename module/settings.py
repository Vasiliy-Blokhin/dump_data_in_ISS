import os

BASE_DIR = os.getcwd()
DUMP_DATA = BASE_DIR + '/dump_data'

# URL для получения данных Мосбиржи.
IMOEX_URL = (
    'http://iss.moex.com/iss/engines/stock/markets/shares/'
    'securities.json?iss.json=extended&iss.meta=off'
)
