"""
Get some data from the USASpending API
"""

from glob import glob
from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import DataFrame
from pandas import read_csv


INPUT_FOLDER = './data/'
RECIPIENT_COLUMNS = ['recipient_name', 'recipient_uei', ]

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    if LOGGER.hasHandlers():
        LOGGER.handlers.clear()
    LOGGER.info('started')

    for folder in [INPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    result = dict()
    df = DataFrame()
    for index, input_file in enumerate(glob(INPUT_FOLDER + '*/*.csv')):
        if index == 0:
            LOGGER.info(input_file)
            df = read_csv(filepath_or_buffer=input_file, low_memory=False)

    columns_to_drop = [column for column in df.columns if df[column].isna().sum() == len(df)]
    df = df.drop(columns=columns_to_drop)

    recipient_df = df[RECIPIENT_COLUMNS].drop_duplicates().sort_values(by=['recipient_name']).copy(
        deep=True).reset_index().drop(columns=['index'])

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
