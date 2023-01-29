from data.data_pulling_functions.fed import data_from_fed
import pandas as pd
import sqlite3



def download_cpi_data(start_date='1995-01-01', replace=False):

# Import relavent sections of cpi, we may need to go 1 level deeper in the future
    series_list = pd.read_csv('series_references/cpi_weight_codes.csv')
    series_list = series_list[series_list.fred_codes.isin(
        ['CPITRNSL', 'CPIRECSL', 'CPIOGSSL', 'CPIMEDSL', 'CPIHOSSL', 'CPIFABSL', 'CPIEDUSL', 'CPIAPPSL'])]
    data = data_from_fed(series_list.iloc[0, 2], series_list.iloc[0, 0], start_date=start_date)
    for i in range(1,len(series_list)):
        data = pd.merge(data, data_from_fed(series_list.iloc[i, 2], series_list.iloc[i, 0], start_date=start_date),
                        on='date',
                        how='outer')


    data.iloc[:, 1:] = data.iloc[:, 1:].astype(float)

    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')

    con = sqlite3.connect('../data.db')
    if replace:
        data.to_sql('cpi', con, if_exists='replace', index=False, index_label='date')
    else:
        data.to_sql('cpi', con, if_exists='append', index=False, index_label='date')

    return data