"""
Get some data from the USASpending API
"""

from glob import glob
from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now

INPUT_FOLDER = './data/'

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

    for input_file in glob(INPUT_FOLDER + '*.zip'):
        LOGGER.info(input_file)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
