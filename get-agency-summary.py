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

from agencies import AGENCIES

OUTPUT_FOLDER = './data/'
URL = 'https://api.usaspending.gov/'

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

    endpoint = '/api/v2/references/agency/{}/'
    data = dict()
    for agency in AGENCIES:
        LOGGER.info(agency)
        result = get(url=URL + endpoint.format(agency)).json()
        if result:
            data[agency] = result['results']
    # data = {agency: get(url=URL + endpoint.format(agency)).json()['results'] for agency in AGENCIES}
    df = DataFrame(data=data).T.drop_duplicates()

    output_file = OUTPUT_FOLDER + 'agencies-{}.csv'.format(df['active_fy'].unique()[0])
    LOGGER.info('writing %d rows to %s', len(df), output_file)
    df.to_csv(path_or_buf=output_file)
    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
