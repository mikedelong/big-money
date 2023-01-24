"""
Get some data from the USASpending API
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import DataFrame
from requests import get
from pandas import read_csv

AGENCY_AWARD_SUMMARY_FILE = 'get-agency-award-summary.csv'
INPUT_FOLDER = './data/'
OUTPUT_FOLDER = './data/'
TOP_TIER_DATA_FILE = 'top_tier_data.csv'

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

    top_tier_file = INPUT_FOLDER + TOP_TIER_DATA_FILE
    top_tier_df = read_csv(filepath_or_buffer=top_tier_file)
    award_summary_file = INPUT_FOLDER + AGENCY_AWARD_SUMMARY_FILE
    award_summary_df = read_csv(filepath_or_buffer=award_summary_file)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
