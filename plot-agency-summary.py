"""
Load and graph agency top-level data
"""

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from matplotlib.pyplot import savefig
from pandas import read_csv
from plotly.graph_objects import Figure
from plotly.graph_objects import Treemap

INPUT_FILE = 'agencies-2023.csv'
INPUT_FOLDER = './data/'
OUTPUT_FOLDER = './plot/'
USECOLS = ['agency_name', 'outlay_amount', 'obligated_amount', 'budget_authority_amount',
           'current_total_budget_authority_amount', ]

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

    filepath_or_buffer = INPUT_FOLDER + INPUT_FILE
    LOGGER.info('loading: %s', filepath_or_buffer)
    df = read_csv(filepath_or_buffer=filepath_or_buffer, usecols=USECOLS)

    # drop agencies with no money
    df = df[df['outlay_amount'] > 0]

    outlay_amount = df['outlay_amount'].sum()
    obligated_amount = df['obligated_amount'].sum()
    current_total = df['current_total_budget_authority_amount'].sum()
    authority_amount = df['budget_authority_amount'].unique()[0]

    fractions = [item / authority_amount for item in [outlay_amount, obligated_amount, current_total]]

    for short_name, columns in {
        'authority_plot.png': ['budget_authority_amount'], 'obligation_plot.png': ['obligated_amount', ],
        'outlay_plot.png': ['outlay_amount', ],
        'triple_plot.png': ['outlay_amount', 'obligated_amount', 'budget_authority_amount'],
    }.items():
        plot = df[columns].plot.pie(subplots=True, figsize=(11, 6), labels=df['agency_name'])
        fname = OUTPUT_FOLDER + short_name
        savefig(fname=fname, format='png')

    for column in ['outlay_amount', 'obligated_amount', 'budget_authority_amount']:
        LOGGER.info('building treemap: %s', column)
        fig = Figure(Treemap(labels=df['agency_name'], parents=[''] * len(df), values=df[column]))
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
        fig.write_html(f'{OUTPUT_FOLDER}{column}.html')

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
