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


def process(arg: dict) -> dict:
    result = {key: value for key, value in arg.items() if not isinstance(value, list)}
    for key, value in arg['agency_data_by_year'][0].items():
        if not isinstance(value, list):
            result[key] = value
    return result


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
        url = 'https://api.usaspending.gov/api/v2/agency/{}/budgetary_resources/'.format(agency)
        result = get(url=url)
        result_json = result.json()
        LOGGER.info('%s %d', agency, len(result_json))
        data[agency] = result_json

    output_file = OUTPUT_FOLDER + 'budgetary-resources.json'
    LOGGER.info('dumping %d records to %s', len(data), output_file)
    with open(file=output_file, mode='w') as output_fp:
        dump(obj=data, fp=output_fp)

    df = DataFrame(data={key: process(value) for key, value in data.items()}).T
    output_file = OUTPUT_FOLDER + 'budgetary-resources.csv'
    LOGGER.info('writing %d records to %s', len(df), output_file)
    df.to_csv(path_or_buf=output_file, index=False)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
