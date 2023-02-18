#!/usr/bin/env python3

# DOCS: Handles conversion of excel documents to csv files

# will not be used enough to justify logging, see stdout
# room for addition of large-scale transformations on data before EDA

# ./pipeline/file_ingestion.py -d data/prepared_data

import argparse
import pandas as pd
 
def conversion(files, destination):
    for f in files:
        tmp = pd.read_excel(f)
        if 'meteorological' in f.lower():
            tmp.to_csv(f'{destination}/meteorological_data.csv', index=None, header=True)
        elif 'sensor' in f.lower():
            tmp.to_csv(f'{destination}/sensor_data.csv', index=None, header=True)
        else:
            print('Seems like your data is not for this project...')

def main():
    relative_paths = ['data/Meteorological Data.xlsx','data/Sensor Data.xlsx']

    print('Beginning file conversion\t..|')

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--destination', action='store')
    args = parser.parse_args()
    dest = args.destination

    print('Converting files to CSV format\t..|')
    conversion(relative_paths, dest)

    print('Conversion complete; check destination directory to confirm\t..|')

if __name__=='__main__':
    main()

