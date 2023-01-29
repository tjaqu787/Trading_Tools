import pandas as pd
import sqlite3
from data.data_pulling_functions.fed import data_from_fed


def download_rate_data(start_date='1995-01-01', replace=False):
    con = sqlite3.connect('../data.db')

    #####################
    # lots of things to add: credit upgrades/downgrades, look at change in rates
    #
    #
    #####################
    # https://fred.stlouisfed.org/release/tables?rid=434&eid=200180#snid=200181

    # grab rate and delinquency data

    rate_data = data_from_fed('AAA', 'AAA_Yield', start_date=start_date, freq='m',
                                                  aggregation_method='avg')

    rate_data = pd.merge(rate_data, data_from_fed('BAA', 'BAA_Yield', start_date=start_date), on='date',
                         how='outer')

    rate_data = pd.merge(rate_data,
                         data_from_fed('DFF', 'FedRate', start_date=start_date, freq='m', aggregation_method='avg'),
                         on='date', how='outer')

    data = pd.merge(rate_data, data_from_fed('MORTGAGE15US', 'MortgageRates', start_date=start_date, freq='m',
                                             aggregation_method='avg'), on='date',
                    how='outer')
    data = pd.merge(data, data_from_fed('TERMCBAUTO48NS', 'AutoRates', start_date=start_date), on='date',
                    how='outer')

    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')

    if replace:
        data.to_sql('rates', con, if_exists='replace', index=False, index_label='date')
    else:
        data.to_sql('rates', con, if_exists='append', index=False, index_label='date')

    return data
