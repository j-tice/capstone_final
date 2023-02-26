#!/usr/bin/env python

import numpy as np
import pandas as pd
from pandasql import sqldf
import matplotlib.pyplot as plt
import seaborn as sns

sensor = pd.read_csv('https://raw.githubusercontent.com/j-tice/capstone_final/master/data/prepared_data/clean_data/clean_sensor_data.csv')
weather = pd.read_csv('https://raw.githubusercontent.com/j-tice/capstone_final/ef9ac7bceb5cde6fd932cb5c0018ca90329a9d3c/data/prepared_data/clean_data/clean_meteorological_data.csv')
locations = pd.read_csv('https://raw.githubusercontent.com/j-tice/capstone_final/ef9ac7bceb5cde6fd932cb5c0018ca90329a9d3c/data/prepared_data/clean_data/locations.csv')
chem_counts = pd.read_csv('https://raw.githubusercontent.com/j-tice/capstone_final/a9b08f3c0f6fdd6e72bdd1465f3c6177b687d332/data/prepared_data/clean_data/chem_counts.csv')

psql = lambda q: sqldf(q, globals())


clean_locs = locations[locations.Name.str.contains('Sensor')]
clean_locs.columns = 'monitor,x,y'.split(',')
clean_locs.monitor = list(range(1,10))
clean_locs = clean_locs.reset_index().drop(['index'], axis='columns')

max_dfs = dict()
chem_names = sorted(list(set(chem_counts.chemical)))

for name in chem_names:
    q = '''
        WITH base AS (
        SELECT Chemical, Monitor, MAX(Reading) AS max_reading
        FROM sensor
        WHERE Chemical = "{chem}"
        GROUP BY Chemical, Monitor)  
        SELECT *
        FROM base LEFT JOIN clean_locs
        ON base.Monitor = clean_locs.monitor'''.format(chem=name)
    joined = psql(q)
    result = joined['Chemical,Monitor,x,y,max_reading'.split(',')]
    result.columns = [elem.lower() for elem in result.columns]
    max_dfs['d_{0}'.format(name)] = result


for df in max_dfs.values():
    focus = df.chemical[0]
    tmp = df

    factories = locations[~locations.Name.str.contains('Sensor')]
    factories.columns = 'monitor,x,y'.split(',')
    factories['chemical'] = ['Factory'] * len(factories)
    factories['max_reading'] = [1] * len(factories)
    factories = factories['chemical,monitor,x,y,max_reading'.split(',')]
    total = pd.concat([tmp,factories])

    bubbles = sns.relplot(
        x='x', y='y', 
        hue='chemical', palette='muted',
        size='max_reading', sizes=(40, 300), 
        alpha=.5, height=8, 
        data=total
    )

    ax = bubbles.axes[0,0]
    for idx,row in total.iterrows():
        x = row[2]
        y = row[3]
        text = row[1]
        label = 'Sensor ' + str(text) + ':\n{}'.format(round(row[4], 4)) if row[4] != 1 else text
        x_offset = x+1 if row[4] != 1 else x-10
        y_offset = y-1 if row[4] != 1 else y+2
        ax.text(x_offset, y_offset, label, horizontalalignment='left')
    plt.title(focus)
    
    plt.savefig('{}_max_per_sensor'.format(focus.upper()))


