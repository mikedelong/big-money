"""
Get some data from the USASpending API
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now
from pandas import concat
from pandas import json_normalize
from requests import post

INDEX = 3
DATA = [
    {
        'search_text': 'Defense'
    },
    {
        'search_text': 'Award'
    },
    {
        'type': 'award_agencies'
    },
    {
        'columns': [],
        'download_types': [
            'prime_awards'
        ],
        'file_format': 'csv',
        'filters': {
            'agencies': [
                {
                    'name': 'Animal and Plant Health Inspection Service',
                    'tier': 'subtier',
                    'toptier_name': 'Department of Agriculture',
                    'type': 'funding'
                }
            ],
            'prime_and_sub_award_types': {
                'prime_awards': [
                    '02',
                    '03',
                    '04',
                    '05',
                    '06',
                    '07',
                    '08',
                    '09',
                    '10',
                    '11',
                    'A',
                    'B',
                    'C',
                    'D',
                    'IDV_A',
                    'IDV_B',
                    'IDV_B_A',
                    'IDV_B_B',
                    'IDV_B_C',
                    'IDV_C',
                    'IDV_D',
                    'IDV_E'
                ],
                'sub_awards': []
            },
            'date_range': {
                'start_date': '2019-10-01',
                'end_date': '2020-09-30'
            },
        },
        'request_type': 'award'
    }
][INDEX]
FIELD = ['results', 'matched_terms', 'agencies', 'foo'][INDEX]
URL = [
    'https://api.usaspending.gov/api/v2/autocomplete/funding_agency/',
    'https://api.usaspending.gov/api/v2/autocomplete/glossary/',
    'https://api.usaspending.gov/api/v2/bulk_download/list_agencies/',
    'https://api.usaspending.gov/api/v2/bulk_download/awards/',
][INDEX]

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    if LOGGER.hasHandlers():
        LOGGER.handlers.clear()
    LOGGER.info('started')

    LOGGER.info('url: %s', URL)
    LOGGER.info('data: %s', DATA)
    # response = post(url=URL, data=DATA, )
    response = post(url=URL, json=DATA, )
    LOGGER.info('status code: %d', response.status_code)
    LOGGER.info('reason: %s', response.reason)
    if response.status_code == 200:
        response_json = response.json()
        if FIELD != 'agencies':
            df = json_normalize(data=response_json[FIELD])
        else:
            df = concat([json_normalize(data=response_json[FIELD][item]) for item in response_json[FIELD].keys()])

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
