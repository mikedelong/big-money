"""
Get some data from the USASpending API
"""

from json import load
from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now


INPUT_FILE = 'top_tier_codes.json'
INPUT_FOLDER = './data/'
OUTPUT_FOLDER = './data/'

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

    input_file = INPUT_FOLDER + INPUT_FILE
    with open(file=input_file, mode='r') as input_fp:
        data = load(fp=input_fp)


    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
