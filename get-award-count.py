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
        url = 'https://api.usaspending.gov/api/v2/agency/{}/awards/new/count'.format(agency)
        result = get(url=url).json()
        LOGGER.info('%s %d', agency, len(result))
        data[agency] = result

    df = DataFrame(data=data).T.drop_duplicates()
    output_file = OUTPUT_FOLDER + 'get-award-count.csv'
    LOGGER.info('writing %d rows to %s', len(df), output_file)
    df.to_csv(path_or_buf=output_file, index=False)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
