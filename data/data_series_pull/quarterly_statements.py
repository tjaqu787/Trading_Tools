from data.data_pulling_functions.fed import data_from_fed
import pandas as pd
import sqlite3


def download_quarterly_data(start_date='2000-01-01', replace=False):
    con = sqlite3.connect('../data.db')

    series_list = pd.read_csv('series_references/QuarterlyFinacialreportDataList.csv')
    data = data_from_fed(series_list.iloc[0, 1],
                                          series_list.iloc[0, 0] + series_list.columns.values[1],
                                          start_date=start_date)
    for i in range(series_list.shape[0]):
        for j in range(1, series_list.shape[1]):
            if i == 0 and j == 1:
                continue
            data = pd.merge(data,
                        data_from_fed(series_list.iloc[i, j],
                                      series_list.iloc[i, 0] + series_list.columns.values[j],
                                      start_date=start_date), on='date', how='outer')

    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')
    '''
    # make all measures per capita
    data = pd.merge(data, data_from_fed('POPTHM', 'pop', start_date=start_date), on='date', how='outer')
    data.iloc[:, 1:] = data.iloc[:, 1:].astype(float)
    data.iloc[:, 1:] = data.iloc[:, 1:].div(data['pop'], axis=0) * 1000
    '''
    # Import relavent sections of cpi, we may need to go 1 level deeper in the future

    if replace:
        data.to_sql('incomestatements', con, if_exists='replace', index=False, index_label='date')
    else:
        data.to_sql('incomestatements', con, if_exists='append', index=False, index_label='date')

    return data
