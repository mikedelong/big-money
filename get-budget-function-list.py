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

from agencies import TOP_TIER

OUTPUT_FOLDER = './data/'

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

    data = dict()
    for agency in TOP_TIER:
        url = 'https://api.usaspending.gov/api/v2/agency/{}/budget_function/'.format(agency)
        data[agency] = get(url=url).json()
        LOGGER.info('%s %d', agency, len(data[agency]))

    output_file = OUTPUT_FOLDER + 'get-budget-function-list.json'
    LOGGER.info('dumping %d records to JSON: %s', len(data), output_file)
    with open(file=output_file, mode='w') as output_fp:
        dump(obj=data, fp=output_fp, sort_keys=True, indent=4)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
