"""
Get some data from the USASpending API
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger

from arrow import now
from pandas import json_normalize
from requests import post

DATA = [{'number': '12524', 'type': 'issue', 'action': 'show'},
        {
            'filters': {
                'prime_award_types': [
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
                    'IDV_E',
                    '02',
                    '03',
                    '04',
                    '05',
                    '10',
                    '06',
                    '07',
                    '08',
                    '09',
                    '11'
                ],
                'date_type': 'action_date',
                'date_range': {
                    'start_date': '2019-10-01',
                    'end_date': '2020-09-30'
                },
                'agencies': [
                    {
                        'type': 'funding',
                        'tier': 'subtier',
                        'name': 'Animal and Plant Health Inspection Service',
                        'toptier_name': 'Department of Agriculture'
                    }
                ]
            },
            'file_format': 'csv'
        },
        {
            'filters': {
                'prime_award_types': ['A'],
                'date_type': 'action_date',
                'date_range': {
                    'start_date': '2022-01-01',
                    'end_date': '2022-02-01'
                },
                'agencies': [
                    {
                        'type': 'funding',
                        'tier': 'subtier',
                        'name': 'Animal and Plant Health Inspection Service',
                        'toptier_name': 'Department of Agriculture'
                    }
                ]
            },
            'file_format': 'csv'
        },
        {
            'search_text': 'Springfield',
            'limit': 40,
            'filter': {
                'country_code': 'USA',
                'scope': 'recipient_location',
                'state_code': 'VA'
            }
        },
        {
            'search_text': 'Springfield',
            'limit': 40,
            'country_code': 'USA'
        },
        {
            'filters': {
                'award_type_codes': ['10'],
                'agencies': [
                    {
                        'type': 'awarding',
                        'tier': 'toptier',
                        'name': 'Social Security Administration'
                    },
                    {
                        'type': 'awarding',
                        'tier': 'subtier',
                        'name': 'Social Security Administration'
                    },
                    {
                        'type': 'funding',
                        'tier': 'toptier',
                        'name': 'Social Security Administration'
                    },
                    {
                        'type': 'funding',
                        'tier': 'subtier',
                        'name': 'Social Security Administration'
                    }
                ],
                'legal_entities': [779928],
                'recipient_scope': 'domestic',
                'recipient_locations': [650597],
                'recipient_type_names': ['Individual'],
                'place_of_performance_scope': 'domestic',
                'place_of_performance_locations': [60323],
                'award_amounts': [
                    {
                        'lower_bound': 1500000.00,
                        'upper_bound': 1600000.00
                    }
                ],
                'award_ids': [1018950]
            },
            'fields': ['Award ID', 'Recipient Name', 'Start Date', 'End Date', 'Award Amount', 'Awarding Agency',
                       'Awarding Sub Agency', 'Award Type', 'Funding Agency', 'Funding Sub Agency'],
            'sort': 'Recipient Name',
            'order': 'desc'
        },
        {
            'search_text': 'Defense'
        },
        ][-1]

URL = [
    'http://bugs.python.org',
    'https://api.usaspending.gov/api/v2/bulk_download/awards/',
    'https://api.usaspending.gov/api/v2/awards/accounts/',
    'https://api.usaspending.gov/api/v2/autocomplete/city/',
    'https://api.usaspending.gov/api/v2/search/spending_by_award/',
    'https://api.usaspending.gov/api/v2/autocomplete/cfda/',
    'https://api.usaspending.gov/api/v2/autocomplete/funding_agency/',
][-1]

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    if LOGGER.hasHandlers():
        LOGGER.handlers.clear()
    LOGGER.info('started')

    LOGGER.info('url: %s', URL)
    LOGGER.info('data: %s', DATA)
    response = post(url=URL, data=DATA,
                    # headers={"Content-Type": "application/json"}
                    )
    LOGGER.info(response.status_code)
    LOGGER.info(response.reason)
    LOGGER.info(response.text[:40])
    text = response.text
    response_json = response.json()
    df = json_normalize(data=response_json['results'])

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
