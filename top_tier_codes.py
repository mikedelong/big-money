"""
Get some data from the USASpending API
"""

from json import dump
from logging import INFO
from logging import Logger
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from requests import get

from agencies import TOP_TIER


def get_code_data(arg: str, logger: Logger) -> dict:
    result = get(url=URL_FORMAT.format(arg))
    logger.info('agency: %s result size: %d', arg, len(result.text))
    return result.json()


OUTPUT_FOLDER = './data/'
URL_FORMAT = 'https://api.usaspending.gov/api/v2/agency/{}/'

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

    data = {code: get_code_data(code, LOGGER) for code in TOP_TIER}

    output_file = OUTPUT_FOLDER + 'top_tier_codes.json'
    LOGGER.info('writing %d records to %s', len(data), output_file)
    with open(file=output_file, mode='w') as output_fp:
        dump(obj=data, fp=output_fp, indent=4, sort_keys=True)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
