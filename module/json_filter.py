""" Описание класса, для работы с БД."""
import logging
from datetime import datetime
from pytz import timezone

from module.settings import (
    NEEDFUL,
    handler,
    STOP_TRADING,
    RUN_TRADING,
    SHARE_GROUPS,
    TYPE_DATA_IMOEX,
    IMOEX_URL
)
from module.worker import Dump

# Запуск логгера.
logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class Filter(Dump):
    """ Родительский класс для базовых действий."""
    def __init__(self, url=None, file=None, type_data=None) -> None:
        self.type_data = type_data

    @classmethod
    def sorted_data(self, data):
        secid_list = []
        for share in data:
            secid = share.get('SECID')
            if secid in secid_list:
                data.remove(share)
                continue
            secid_list.append(secid)
        return data

    @classmethod
    def union_api_response(self, data_sec, data_md):
        """ Добавляет доплнительные параметры и сводит всё в одну БД."""
        result = []
        for el_sec in data_sec:
            for el_md in data_md:
                # Сведение БД в одну.
                if el_sec['SECID'] == el_md['SECID']:
                    el_sec.update(el_md)
            # Добавление новых параметров.
            if el_sec['TRADINGSESSION'] is None:
                el_sec['TRADINGSESSION'] = STOP_TRADING
            elif el_sec['TRADINGSESSION'] == '1':
                el_sec['TRADINGSESSION'] = RUN_TRADING

            if el_sec['CURRENCYID'] == 'SUR':
                el_sec['CURRENCYID'] = 'рубль'

            format = '%H:%M:%S (%d.%m)'
            el_sec['DATAUPDATE'] = (
                datetime.now(timezone('Europe/Moscow'))
            ).strftime(format)

            result.append(el_sec)
        # Проверка и вывод выходных данных.

        return self.sorted_data(result)

    @classmethod
    def return_data(self):
        """ Фильтрация данных, полученных с запроса."""
        result = []
        data_list = []
        logger.info('get response info from ISS')
        # Фильтрация полученных данных (из разных "графов").
        for type_data in TYPE_DATA_IMOEX:
            for element in self.get_api_response(
                url=IMOEX_URL
            )[1][type_data]:
                # Оставляет только акции.
                if (
                    type_data == 'securities'
                    and element.get('INSTRID') != 'EQIN'
                ):
                    continue
                if element.get('BOARDID') not in SHARE_GROUPS:
                    continue
                new_dict = {}
                # Добавление только необходимых параметров из списка.
                for key, value in element.items():
                    if key in NEEDFUL:
                        new_dict[key] = value
                data_list.append(new_dict)
            result.append(data_list)

        return self.union_api_response(*result)
