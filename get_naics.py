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

OUTPUT_FOLDER = './data/'
URL = 'https://api.usaspending.gov/api/v2/references/naics/'

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

    result = get(url=URL)
    if result.status_code == 200:
        result_json = result.json()
        output_file = OUTPUT_FOLDER + 'naics_two_digits.json'
        LOGGER.info('writing %d items to %s', len(result_json['results']), output_file)
        with open(file=output_file, mode='w') as output_fp:
            dump(obj=result_json['results'], fp=output_fp, indent=4, sort_keys=True)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
