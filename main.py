'''
Get some data from the USASpending API
'''

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from pandas import DataFrame
from requests import get
from requests import post

OUTPUT_FOLDER = './data/'
URL = 'https://api.usaspending.gov/'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    LOGGER.info('started')

    for folder in [OUTPUT_FOLDER]:
        LOGGER.info('creating folder %s if it does not exist', folder)
        Path(folder).mkdir(parents=True, exist_ok=True)

    # found values for agency are 400? and 456

    data = {agency:
                get(url=URL + '/api/v2/references/agency/{}/'.format(agency)).json()['results']
            for agency in range(410, 500)
            }
    df = DataFrame(data=data).T.drop_duplicates()
    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
