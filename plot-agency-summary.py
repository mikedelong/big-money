"""
Load and graph agency top-level data
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import DataFrame
from pandas import read_csv

INPUT_FILE = 'agencies-2023.csv'
INPUT_FOLDER = './data/'
OUTPUT_FOLDER = './plot/'
USECOLS = ['agency_name', 'outlay_amount', 'obligated_amount', 'budget_authority_amount',
           'current_total_budget_authority_amount', ]

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    if LOGGER.hasHandlers():
        LOGGER.handlers.clear()
    LOGGER.info('started')

    for folder in [INPUT_FOLDER, OUTPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    filepath_or_buffer = INPUT_FOLDER + INPUT_FILE
    LOGGER.info('loading: %s', filepath_or_buffer)
    df = read_csv(filepath_or_buffer=filepath_or_buffer, usecols=USECOLS)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
