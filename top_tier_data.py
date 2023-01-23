"""
Get some data from the USASpending API
"""

from json import load
from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import DataFrame


def remove_list_values(arg: dict) -> dict:
    return {key: value for key, value in arg.items() if not isinstance(value, list)}


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

    df = DataFrame(data=[remove_list_values(arg=value) for value in data.values()])

    output_file = OUTPUT_FOLDER + 'top_tier_data.csv'
    LOGGER.info('writing %d records to %s', len(df), output_file)
    df.to_csv(index=False, path_or_buf=output_file, )

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
