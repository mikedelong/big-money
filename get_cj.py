'''
Get some data from the USASpending API
'''

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import read_csv

OUTPUT_FOLDER = './data/'
URL = 'https://www.usaspending.gov/data/cj_list.csv'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    for folder in [OUTPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    df = read_csv(filepath_or_buffer=URL)
    LOGGER.info(df.shape)
    df.to_csv(path_or_buf=OUTPUT_FOLDER + 'cj.csv')

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
