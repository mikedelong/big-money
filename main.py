"""
Get some data from the USASpending API
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import json_normalize
from requests import get

FULL_DOWNLOAD_URL = 'https://files.usaspending.gov/database_download/usaspending-db_20230108.zip'
OUTPUT_FOLDER = './data/'
URL = 'https://api.usaspending.gov/api/v2/award_spending/recipient/?fiscal_year=2016&awarding_agency_id=183'

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
    result_json = result.json()

    df = json_normalize(data=result_json['results'])

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
