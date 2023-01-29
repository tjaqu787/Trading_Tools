from multiprocessing.spawn import import_main_path
from data.data_pulling_functions.fed import data_from_fed
import pandas as pd
import sqlite3


def download_PPI_data(start_date='1995-01-01', replace=False):
    con = sqlite3.connect('../data.db')

    series_list = pd.read_csv('series_references/ppi.csv')
    data = data_from_fed(series_list.iloc[0, 0], series_list.iloc[0, 1], start_date=start_date)
    for i in range(1,len(series_list)):
        data = pd.merge(data, data_from_fed(series_list.iloc[i, 0], series_list.iloc[i, 1], start_date=start_date),
                        on='date', how='outer')

    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')

    if replace:
        data.to_sql('ppi', con, if_exists='replace', index=False, index_label='date')
    else:
        data.to_sql('ppi', con, if_exists='append', index=False, index_label='date')

    return data
