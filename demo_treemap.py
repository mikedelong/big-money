'''
Demo the plotly tree map
'''

from logging import INFO
from logging import basicConfig
from logging import getLogger
from pathlib import Path

from arrow import now
from plotly.graph_objects import Treemap
from plotly.subplots import make_subplots

INPUT_FOLDER = './data/'
LABELS = ['Eve', 'Cain', 'Seth', 'Enos', 'Noam', 'Abel', 'Awan', 'Enoch', 'Azura']
PARENTS = ['', 'Eve', 'Eve', 'Seth', 'Seth', 'Eve', 'Eve', 'Awan', 'Eve']
OUTPUT_FOLDER = './plot/'
SOURCE = 'https://plotly.com/python/treemaps/'
VALUES = [10, 14, 12, 10, 2, 6, 6, 1, 4]
TOTAL_VALUES = [65, 14, 12, 10, 2, 6, 6, 1, 4]

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

    fig = make_subplots(
        cols=2, rows=1, column_widths=[0.4, 0.4],
        subplot_titles=('branchvalues: <b>remainder<br />&nbsp;<br />', 'branchvalues: <b>total<br />&nbsp;<br />'),
        specs=[[{'type': 'treemap', 'rowspan': 1}, {'type': 'treemap'}]]
    )

    fig.add_trace(Treemap(labels=LABELS, parents=PARENTS, values=VALUES,
                          textinfo='label+value+percent parent+percent entry+percent root', ), row=1, col=1)

    fig.add_trace(Treemap(branchvalues='total', labels=LABELS, parents=PARENTS, values=TOTAL_VALUES,
                          textinfo='label+value+percent parent+percent entry', ), row=1, col=2)

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.write_html(OUTPUT_FOLDER + 'demo_treemap.html')

    LOGGER.info('total time: {:5.2f}s'.format((now() - TIME_START).total_seconds()))
