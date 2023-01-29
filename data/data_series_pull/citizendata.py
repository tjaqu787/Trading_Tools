from data.data_pulling_functions.fed import data_from_fed
import pandas as pd
import sqlite3



def get_all_data(start_date='1995-01-01', replace=False):
    # all aggregate states that need to be divided by pop
    # https://fred.stlouisfed.org/release/tables?rid=54&eid=155443#snid=155470
    series_list = pd.read_csv('series_references/debt_and_saving_fred_codes.csv')
    data = pd.DataFrame(data_from_fed(series_list.iloc[0, 0], series_list.iloc[0, 1], start_date=start_date))
    for i in range(1, len(series_list)):
        data = pd.merge(data, data_from_fed(series_list.iloc[i, 0], series_list.iloc[i, 1], start_date=start_date),
                        on='date',
                        how='outer')
    # make all measures per capita
    data = pd.merge(data, data_from_fed('POPTHM', 'pop', start_date=start_date), on='date', how='outer')
    data.iloc[:, 1:] = data.iloc[:, 1:].astype(float)
    data.iloc[:, 1:] = data.iloc[:, 1:].div(data['pop'], axis=0) * 1000

    

    con = sqlite3.connect('../data.db')
    if replace:
        data.to_sql('consumerhealth', con, if_exists='replace', index=False, index_label='date')
    else:
        data.to_sql('consumerhealth', con, if_exists='append', index=False, index_label='date')

    return data