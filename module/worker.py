import os
from datetime import datetime
from time import sleep
import pytz

from module.settings import DUMP_DATA


class Dump():
    """Main dump data class."""

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
