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

AGENCIES = [100, 183, 209, 252, 267, 308, 315, 456, 503, 535, 538, 539, 552, 554, 558, 560, 561, 610, 611, 614, 650,
            651, 654, 655, 680, 682, 685, 687, 692, 693, 694, 695, 697, 699, 700, 731, 766, 800, 801, 803, 805, 806,
            860, 862, 878, 879, 882, 925, 930, 1067, 1068, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134,
            1135, 1136, 1137, 1138, 1139, 1141, 1142, 1143, 1144, 1146, 1147, 1149, 1152, 1154, 1155, 1156, 1157, 1158,
            1159, 1161, 1162, 1163, 1164, 1165, 1166, 1169, 1173, 1205]
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