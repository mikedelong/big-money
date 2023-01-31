"""
Get some data from the USASpending API
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now
from pandas import json_normalize
from requests import post

DATA = [
    {
        'search_text': 'Defense'
    },
][0]

URL = [
    'https://api.usaspending.gov/api/v2/autocomplete/funding_agency/',
][0]

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    if LOGGER.hasHandlers():
        LOGGER.handlers.clear()
    LOGGER.info('started')

    LOGGER.info('url: %s', URL)
    LOGGER.info('data: %s', DATA)
    response = post(url=URL, data=DATA,)
    LOGGER.info('status code: %d', response.status_code)
    LOGGER.info('reason: %s', response.reason)
    response_json = response.json()
    df = json_normalize(data=response_json['results'])

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
