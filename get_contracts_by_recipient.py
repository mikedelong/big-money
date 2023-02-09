"""
Get some data from the USASpending API
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now
from requests import post

DATA = {
    'keyword': 'CALIFORNIA'
}
OUTPUT_FOLDER = './data/'
URL = 'https://api.usaspending.gov/api/v2/recipient/'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    if LOGGER.hasHandlers():
        LOGGER.handlers.clear()
    LOGGER.info('started')

    response = post(url=URL, json=DATA, )
    LOGGER.info('status code: %d', response.status_code)
    LOGGER.info('reason: %s', response.reason)
    if response.status_code == 200:
        response_json = response.json()

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
