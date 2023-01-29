@staticmethod
def get_all_data(start_date='1995-01-01', replace=False):
    # all aggregate states that need to be divided by pop
    # https://fred.stlouisfed.org/release/tables?rid=54&eid=155443#snid=155470
    series_list = pd.read_csv('debt_and_saving_fred_codes.csv')
    data = pd.DataFrame(data_from_fed(series_list.iloc[0, 0], series_list.iloc[0, 1], start_date=start_date))
    for i in range(1, len(series_list)):
        data = pd.merge(data, data_from_fed(series_list.iloc[i, 0], series_list.iloc[i, 1], start_date=start_date),
                        on='date',
                        how='outer')
    # make all measures per capita
    data = pd.merge(data, data_from_fed('POPTHM', 'pop', start_date=start_date), on='date', how='outer')
    data.iloc[:, 1:] = data.iloc[:, 1:].astype(float)
    data.iloc[:, 1:] = data.iloc[:, 1:].div(data['pop'], axis=0) * 1000

    # Import relavent sections of cpi, we may need to go 1 level deeper in the future
    series_list = pd.read_csv('cpi_weight_codes.csv')
    series_list = series_list[series_list.fred_codes.isin(
        ['CPITRNSL', 'CPIRECSL', 'CPIOGSSL', 'CPIMEDSL', 'CPIHOSSL', 'CPIFABSL', 'CPIEDUSL', 'CPIAPPSL'])]
    for i in range(len(series_list)):
        data = pd.merge(data, data_from_fed(series_list.iloc[i, 2], series_list.iloc[i, 0], start_date=start_date),
                        on='date',
                        how='outer')

    data = pd.merge(data, data_from_fed('DRCCLACBS', 'cc_delinquency', start_date=start_date), on='date',
                    how='outer')
    data = pd.merge(data, data_from_fed('MORTGAGE15US', 'MortgageRates', start_date=start_date, freq='m',
                                        aggregation_method='avg'), on='date',
                    how='outer')
    data = pd.merge(data, data_from_fed('TERMCBAUTO48NS', 'AutoRates', start_date=start_date), on='date',
                    how='outer')
    data = pd.merge(data,
                    data_from_fed('DFF', 'FedRate', start_date=start_date, freq='m', aggregation_method='avg'),
                    on='date',
                    how='outer')
    data.iloc[:, 1:] = data.iloc[:, 1:].astype(float)

    data = data.fillna(method='ffill')
    data = data.fillna(method='bfill')

    con = sqlite3.connect('../../../data/cache/model_data.db')
    if replace:
        data.to_sql('consumerhealth', con, if_exists='replace', index=False, index_label='date')
    else:
        data.to_sql('consumerhealth', con, if_exists='append', index=False, index_label='date')

    return data