"""
Get some data from the USASpending API
"""

from json import dump
from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from requests import get

from agencies import AGENCIES

OUTPUT_FOLDER = './data/'
URL = 'https://api.usaspending.gov/'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    if LOGGER.hasHandlers():
        LOGGER.handlers.clear()
    LOGGER.info('started')

    for folder in [OUTPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    year = 2023
    outfile = OUTPUT_FOLDER + 'explore_recipient.json'
    out_result = list()
    for agency in AGENCIES:
        endpoint = f'api/v2/award_spending/recipient/?fiscal_year={year}&awarding_agency_id={agency}'
        result = get(URL + endpoint).json()
        if result:
            keys = set(result.keys())
            if 'page_metadata' in keys and 'results' in keys:
                page_count = result['page_metadata']['count']
                if page_count > 0:
                    out_result.append(result)
                    with open(file=outfile, mode='w') as output_fp:
                        dump(obj=out_result, fp=output_fp, sort_keys=True)

            if 'page_metadata' in result.keys():
                LOGGER.info('%d page count: %d', agency, result['page_metadata']['count'])
            if 'results' in result.keys():
                results = result['results']
                LOGGER.info('%d result count: %d', agency, len(result['results']))
    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
