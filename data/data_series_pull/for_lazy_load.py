from os import path
import pandas as pd
from functools import cache
from data.data_pulling_functions.fed import data_from_fed

current_directory = path.abspath(__file__).rstrip('for_lazy_load.py')


@cache
def lazy_load_for_consumer_health(start_date='2018-01-01'):
    series_list = ['PCEDurableGoods', 'PCENonDurableGoods', 'PCEServices', 'Personalinterestpayments',
                   'DisposablePersonalIncome', 'PersonalSaving', 'TotalCredit', 'DelinquencyRateOnBusinessLoans',
                   'DelinquencyRateOnSingleFamilyResidentialMortgages', 'DelinquencyRateOnCreditCardLoans',
                   'DelinquencyRateOnLeaseFinancingReceivables', 'DelinquencyRateOnConsumerLoans', 'Transportation',
                   'Recreation', 'Othergoodsandservices', 'Medicalcare', 'Housing', 'Foodandbeverages',
                   'Educationandcommunication', 'Apparel', 'MortgageRates', 'AutoRates', 'FedRate',
                   'RevolvingCreditChange',
                   'NonRevolvingCreditChange']
    debt_codes = pd.read_csv(f'{current_directory}/series_references/debt_and_saving_fred_codes.csv')
    delinquency_codes = pd.read_csv(f'{current_directory}/series_references/delinquency.csv')
    cpi_codes = pd.read_csv(f'{current_directory}/series_references/cpi_weight_codes.csv').drop(columns=['weights'])
    # join together on axis 0
    series_names = pd.concat([cpi_codes, debt_codes, delinquency_codes], axis=0)
    series_names = series_names[series_names['name'].isin(series_list)]
    series_names = series_names[['name', 'codes']]

    data = data_from_fed(series_names.iloc[0, 1], series_names.iloc[0, 0], start_date=start_date)
    # download all the data from the fed
    for i in range(1, len(series_names)):
        data = pd.merge(data, data_from_fed(series_names.iloc[i, 1], series_names.iloc[i, 0], start_date=start_date),
                        on='date', how='outer')
    
    rate_data = download_rates_data(start_date=start_date).drop(columns=['AAA_Yield', 'BAA_Yield'])
    data = pd.merge(data, rate_data, on='date', how='outer')
    data['date'] = pd.to_datetime(data.date)
    return data


@cache
def download_rates_data(start_date='2018-01-01'):
    rate_data = data_from_fed('AAA', 'AAA_Yield', start_date=start_date, freq='m',
                              aggregation_method='avg')
    
    rate_data = pd.merge(rate_data, data_from_fed('BAA', 'BAA_Yield', start_date=start_date), on='date',
                         how='outer')
    
    rate_data = pd.merge(rate_data,
                         data_from_fed('DFF', 'FedRate', start_date=start_date, freq='m', aggregation_method='avg'),
                         on='date', how='outer')
    
    rate_data = pd.merge(rate_data, data_from_fed('MORTGAGE15US', 'MortgageRates', start_date=start_date, freq='m',
                                                  aggregation_method='avg'), on='date',
                         how='outer')
    rate_data = pd.merge(rate_data, data_from_fed('TERMCBAUTO48NS', 'AutoRates', start_date=start_date), on='date',
                         how='outer')
    return rate_data



def lazy_load_for_sector_plot(series, start_date='2018-01-01'):
    @cache
    def download_nonsector_data(start_date='2018-01-01'):
        pce_cols = ['AAA_yield', 'BAA_Yeild', 'FedRate', 'MortgageRates', 'AutoRates', 'PCEDurableGoods',
                    'PCENonDurableGoods', 'PCEServices', 'DelinquencyRateOnBusinessLoans',
                    'DelinquencyRateOnSingleFamilyResidentialMortgages', 'DelinquencyRateOnCreditCardLoans',
                    'DelinquencyRateOnLeaseFinancingReceivables', 'DelinquencyRateOnConsumerLoans',
                    'DelinquencyRateOnSingleFamilyResidentialMortgages', 'DelinquencyRateOnCreditCardLoans',
                    'DelinquencyRateOnConsumerLoans', 'DelinquencyRateOnBusinessLoans',
                    'DelinquencyRateOnLeaseFinancingReceivables']
        debt_codes = pd.read_csv(f'{current_directory}/series_references/debt_and_saving_fred_codes.csv')
        delinquency_codes = pd.read_csv(f'{current_directory}/series_references/delinquency.csv')
        ppi_codes = pd.read_csv(f'{current_directory}/series_references/ppi.csv')
        # join together on axis 0
        series_names = pd.concat([debt_codes, delinquency_codes, ppi_codes], axis=0)
        series_names = series_names[series_names['name'].isin(pce_cols)]
        series_names = series_names[['name', 'codes']]
        misc_data = data_from_fed(series_names.iloc[0, 1], series_names.iloc[0, 0], start_date=start_date)
        # download all the misc_data from the fed
        for i in range(1, len(series_names)):
            misc_data = pd.merge(misc_data,
                                 data_from_fed(series_names.iloc[i, 1], series_names.iloc[i, 0], start_date=start_date),
                                 on='date', how='outer')
        
        rate_data = download_rates_data(start_date=start_date)
        misc_data = pd.merge(misc_data, rate_data, on='date', how='outer')
        misc_data['date'] = pd.to_datetime(misc_data.date)
        return misc_data
    
    qfr_codes = pd.read_csv(f'{current_directory}/series_references/QuarterlyFinacialreportDataList.csv')
    qfr_codes = qfr_codes[qfr_codes.name.isin(series)]
    qfr_data = data_from_fed(qfr_codes.iloc[0, 1], qfr_codes.iloc[0, 0] + qfr_codes.columns.values[1],
                             start_date=start_date)
    data = pd.merge(qfr_data, download_nonsector_data(start_date=start_date), on='date', how='outer')
    data['date'] = pd.to_datetime(data.date)
    return data


@cache
def lazy_load_for_homepage_plot(start_date='2018-01-01'):
    series_list = ['AAA_yield', 'BAA_Yeild', 'FedRate', 'MortgageRates', 'PCEDurableGoods',
                   'PCENonDurableGoods', 'PCEServices', 'DelinquencyRateOnBusinessLoans',
                   'DelinquencyRateOnSingleFamilyResidentialMortgages', 'DelinquencyRateOnCreditCardLoans',
                   'DelinquencyRateOnLeaseFinancingReceivables', 'RevolvingCreditChange',
                   'NonRevolvingCreditChange']
    debt_codes = pd.read_csv(f'{current_directory}/series_references/debt_and_saving_fred_codes.csv')
    delinquency_codes = pd.read_csv(f'{current_directory}/series_references/delinquency.csv')
    
    # join together on axis 0
    series_names = pd.concat([debt_codes, delinquency_codes], axis=0)
    series_names = series_names[series_names['name'].isin(series_list)]
    series_names = series_names[['name', 'codes']]

    data = data_from_fed(series_names.iloc[0, 1], series_names.iloc[0, 0], start_date=start_date)
    # download all the data from the fed
    for i in range(1, len(series_names)):
        data = pd.merge(data, data_from_fed(series_names.iloc[i, 1], series_names.iloc[i, 0], start_date=start_date),
                        on='date', how='outer')
    
    rate_data = download_rates_data(start_date=start_date)
    data = pd.merge(data, rate_data, on='date', how='outer')
    data['date'] = pd.to_datetime(data.date)
    return data
