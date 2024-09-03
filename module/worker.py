import os
from datetime import datetime
from time import sleep
import pytz
import logging
import requests
import json

from module.settings import DUMP_DATA, IMOEX_URL, SPLIT_SYM, handler


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
        delete=False
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
        return '{:%d-%m-%y}'.format(datetime.now())

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
    def write_data_in_file(cls, data=None, file=None):
        if data is None:
            data = cls.get_api_response(url=IMOEX_URL)
        if file is None:
            file = cls.create_time_json_file()

        cls.save_file(
            file=file,
            data=data
        )

    @classmethod
    def is_work_time(cls, url=None):
        if url is None:
            url = IMOEX_URL

        time_str = cls.get_current_time().split(SPLIT_SYM)
        time = int(time_str[0]) + int(time_str[1]) / 100

        data = cls.get_api_response(url=url)
        if (
            data[1]['marketdata'][0]['TRADINGSESSION'] is not None
            and (time > 11 or time < 18)
        ):
            return True
        return False
