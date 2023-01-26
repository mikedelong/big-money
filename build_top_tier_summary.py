"""
Combine what we know about the top tier entities into a single somewhat dirty file
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import read_csv

AGENCY_AWARD_SUMMARY_FILE = 'get-agency-award-summary.csv'
BUDGET_FUNCTION_COUNT_FILE = 'budget-function-count.csv'
INPUT_FOLDER = './data/'
NEW_AWARD_COUNT_FILE = 'get-award-count.csv'
ON_COLUMN = 'toptier_code'
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

    drop_columns = ['fiscal_year']
    top_tier_file = INPUT_FOLDER + TOP_TIER_DATA_FILE
    top_tier_df = read_csv(filepath_or_buffer=top_tier_file)
    award_summary_file = INPUT_FOLDER + AGENCY_AWARD_SUMMARY_FILE
    award_summary_df = read_csv(filepath_or_buffer=award_summary_file)
    result_df = top_tier_df.merge(right=award_summary_df.drop(columns=drop_columns), on=ON_COLUMN, how='inner')
    new_count_file = INPUT_FOLDER + NEW_AWARD_COUNT_FILE
    new_count_df = read_csv(filepath_or_buffer=new_count_file)
    result_df = result_df.merge(right=new_count_df.drop(columns=drop_columns), on=ON_COLUMN, how='inner')
    function_count_file = INPUT_FOLDER + BUDGET_FUNCTION_COUNT_FILE
    function_count_df = read_csv(filepath_or_buffer=function_count_file)
    result_df = result_df.merge(right=function_count_df.drop(columns=drop_columns), on=ON_COLUMN, how='inner')

    output_file = OUTPUT_FOLDER + 'top_tier_summary.csv'
    LOGGER.info('writing %d rows to %s', len(result_df), output_file)
    result_df.to_csv(path_or_buf=output_file, index=False)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
