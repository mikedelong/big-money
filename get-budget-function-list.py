"""
Get some data from the USASpending API
"""

from json import dump
from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import DataFrame
from requests import get

from agencies import TOP_TIER

OUTPUT_FOLDER = './data/'

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

    data = dict()
    for agency in TOP_TIER:
        url = 'https://api.usaspending.gov/api/v2/agency/{}/budget_function/'.format(agency)
        value = get(url=url).json()
        data[agency] = value
        LOGGER.info('%s %d', agency, len(data[agency]))

    output_file = OUTPUT_FOLDER + 'get-budget-function-list.json'
    LOGGER.info('dumping %d records to JSON: %s', len(data), output_file)
    with open(file=output_file, mode='w') as output_fp:
        dump(obj=data, fp=output_fp, sort_keys=True, indent=4)

    data = dict()
    for agency in TOP_TIER:
        url = 'https://api.usaspending.gov/api/v2/agency/{}/budget_function/count/'.format(agency)
        counts = get(url=url).json()
        data[agency] = {key: value for key, value in counts.items() if not isinstance(value, list)}
        LOGGER.info('%s %d', agency, len(data[agency]))
    df = DataFrame(data=data).T
    output_file = OUTPUT_FOLDER + 'budget-function-count.csv'
    LOGGER.info('writing %d records to %s', len(df), output_file)
    df.to_csv(path_or_buf=output_file, index=False)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
