import os
from datetime import datetime
from time import sleep
import pytz
import logging
import sys
import requests
import json

from module.settings import DUMP_DATA, IMOEX_URL

# Запуск логгера.
# Описание хандлера для логгера.
handler = logging.StreamHandler(sys.stdout)
formater = logging.Formatter(
    '%(name)s, %(funcName)s, %(asctime)s, %(levelname)s - %(message)s.'
)

handler.setFormatter(formater)
logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class Dump():
    """Main dump data class."""

    @classmethod
    def get_api_response(
        self,
        url=None,
        post=False,
        headers=None,
        body=None,
        delete=None
    ):
        """ Получение информации с запроса на сервер."""
        try:
            if url is None:
                url = self.url
            if post:
                return requests.post(url, headers=headers, json=body).json()
            elif delete:
                return requests.delete(url, headers=headers).json()
            return requests.get(url, headers=headers).json()
        except json.decoder.JSONDecodeError:
            return []

    @classmethod
    def save_file(self, data, file=None):
        """ Сохранение информации в файле."""
        if file is None:
            file = self.file
        with open(file, 'w') as outfile:
            json.dump(data, outfile)

    @classmethod
    def read_file(self, file=None):
        """ Чтение информации с файла."""
        if file is None:
            file = self.file
        with open(file) as json_file:
            return json.load(json_file)

    @staticmethod
    def get_current_data():
        return '{:%d.%m.%y}'.format(datetime.now())

    @staticmethod
    def get_current_time():
        timezone = 'Europe/Moscow'
        return '{:%H-%M}'.format(
            datetime.now(pytz.timezone(timezone))
        )

    @classmethod
    def create_daily_dir(cls):
        daily_dir = DUMP_DATA + '/' + cls.get_current_data()
        if not os.path.isdir(daily_dir):
            os.mkdir(daily_dir)
        return daily_dir

    @classmethod
    def create_time_json_file(cls):
        time_json_file_name = (
            cls.create_daily_dir() + '/' + cls.get_current_time() + '.json'
        )
        os.open(time_json_file_name, os.O_CREAT)
        return time_json_file_name

    @classmethod
    def write_data_in_file(cls, url=None):
        if url is None:
            url = IMOEX_URL
        cls.save_file(
            file=cls.create_time_json_file(),
            data=cls.get_api_response(url=url)
        )
