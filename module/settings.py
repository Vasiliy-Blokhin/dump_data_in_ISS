import os
import sys
import logging
from dotenv import load_dotenv


load_dotenv()

handler = logging.StreamHandler(sys.stdout)
formater = logging.Formatter(
    '%(name)s, %(funcName)s, %(asctime)s, %(levelname)s - %(message)s.'
)

handler.setFormatter(formater)

BASE_DIR: str = (
    os.getenv('BASE_DIR') if os.getenv('BASE_DIR') else os.getcwd()
)
DUMP_DATA = BASE_DIR + '/dump_data'

# URL для получения данных Мосбиржи.
IMOEX_URL = (
    'http://iss.moex.com/iss/engines/stock/markets/shares/'
    'securities.json?iss.json=extended&iss.meta=off'
)

SPLIT_SYM = '-'

MIN = 60
SLEEP_TIME = 40 * MIN

NEEDFUL = [
    'SECID', 'SHORTNAME', 'PREVPRICE', 'PREVWAPRICE', 'PREVDATE',
    'STATUS', 'WAPTOPREVWAPRICE', 'UPDATETIME', 'LCURRENTPRICE', 'LAST',
    'PRICEMINUSPREVWAPRICE', 'DATAUPDATE', 'CURRENCYID', 'TRADINGSESSION',
    'STATUS_FILTER', 'LASTCHANGEPRCNT', 'WAPRICE', 'LASTCNGTOLASTWAPRICE',
    'WAPTOPREVWAPRICEPRCNT', 'MARKETPRICE', 'ISSUECAPITALIZATION',
    'TRENDISSUECAPITALIZATION', 'BOARDID', 'VALUE'
]
SHARE_GROUPS = ['EQBR', 'EQBS', 'EQCC', 'TQBR']
STOP_TRADING = 'торги приостановлены'
RUN_TRADING = 'торги идут'
TYPE_DATA_IMOEX = ['securities', 'marketdata']
