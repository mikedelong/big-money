"""
Get some data from the USASpending API
"""

from json import load
from logging import INFO
from logging import basicConfig
from logging import getLogger
from time import sleep

from arrow import now
from requests import get
from requests import post

DATA = {
    'filters': {
        'recipient_id': '1c3edaaa-611b-840c-bf2b-fd34df49f21f-P',
        'time_period': [
            {
                'start_date': '2019-09-28',
                'end_date': '2020-09-28'
            }
        ]
    },
    'category': 'naics',
    'limit': 5,
    'page': 1
}
OUTPUT_FOLDER = './data/'
URL = 'https://api.usaspending.gov/api/v2/search/spending_by_category/naics/'

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
