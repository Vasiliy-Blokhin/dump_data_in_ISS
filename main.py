from time import sleep
import logging

from module.worker import Dump as D
from module.json_filter import Filter as F
from module.settings import SLEEP_TIME, handler


logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


if '__main__' == __name__:
    while True:
        try:
            if D.is_work_time():
                D.write_data_in_file(
                    data=F.return_data(),
                )
                logger.info('file is save')
        except Exception as error:
            logger.error(error)
        finally:
            sleep(SLEEP_TIME)
