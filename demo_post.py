"""
Get some data from the USASpending API
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now
from requests import post

DATA = {'number': '12524', 'type': 'issue', 'action': 'show'}
URL = 'http://bugs.python.org'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    if LOGGER.hasHandlers():
        LOGGER.handlers.clear()
    LOGGER.info('started')

    response = post(url=URL, data=DATA)
    LOGGER.info(response.status_code)
    LOGGER.info(response.reason)
    LOGGER.info(response.text[:40])
    text = response.text

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
