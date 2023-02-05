"""
Get some data from the USASpending API
"""

from json import load
from logging import INFO
from logging import basicConfig
from logging import getLogger
from time import sleep

from arrow import now
from requests import get
from requests import post

ALL_AWARD_TYPES = ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11', 'A', 'B', 'C', 'D', 'IDV_A', 'IDV_B',
                   'IDV_B_A', 'IDV_B_B', 'IDV_B_C', 'IDV_C', 'IDV_D', 'IDV_E', ]
OUTPUT_FOLDER = './data/'

if __name__ == '__main__':
    TIME_START = now()
    LOGGER = getLogger(__name__, )
    basicConfig(format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', level=INFO, )
    if LOGGER.hasHandlers():
        LOGGER.handlers.clear()
    LOGGER.info('started')

    with open(file='./post_bulk_download.json', mode='r') as input_fp:
        json_data = load(fp=input_fp)

    # now update request fields
    json_data['data']['filters']['agencies'][0]['name'] = 'all'

    LOGGER.info('url: %s', json_data['url'])
    LOGGER.info('data: %s', json_data['data'])
    response = post(url=json_data['url'], json=json_data['data'], )
    LOGGER.info('status code: %d', response.status_code)
    LOGGER.info('reason: %s', response.reason)
    if response.status_code == 200:
        response_json = response.json()
        done = False
        # wait for the request to complete
        while not done:
            status = get(url=response_json['status_url'])
            status_code = status.status_code
            status_json = status.json()
            done = int(status_code) == 200 and status_json['status'] == 'finished'
            LOGGER.info('%d %s', status_code, status_json['status'])
            if not done:
                sleep(30)
        # get the download
        output_file = OUTPUT_FOLDER + response_json['file_name']
        with open(file=output_file, mode='wb') as output_fp:
            get_content = get(url=response_json['file_url'], stream=True).content
            output_fp.write(get_content)

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
