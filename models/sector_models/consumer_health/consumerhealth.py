import pandas as pd
from data.data_series_pull.for_lazy_load import lazy_load_for_consumer_health


def data_for_consumer_health(start_date='2018-01-01'):
    data = lazy_load_for_consumer_health(start_date=start_date)
    data['date'] = pd.to_datetime(data.date)
    data = data[data['date'] >= start_date]
    data = data.set_index('date')
    data = data.fillna(method='ffill')
    data = data.astype('float32')
    data = data[['PCEDurableGoods', 'PCENonDurableGoods', 'PCEServices', 'Personalinterestpayments',
                 'DisposablePersonalIncome', 'PersonalSaving', 'TotalCredit', 'DelinquencyRateOnBusinessLoans',
                 'DelinquencyRateOnSingleFamilyResidentialMortgages', 'DelinquencyRateOnCreditCardLoans',
                 'DelinquencyRateOnLeaseFinancingReceivables', 'DelinquencyRateOnConsumerLoans', 'Transportation',
                 'Recreation', 'Othergoodsandservices', 'Medicalcare', 'Housing', 'Foodandbeverages',
                 'Educationandcommunication', 'Apparel', 'MortgageRates', 'AutoRates', 'FedRate',
                 'RevolvingCreditChange',
                 'NonRevolvingCreditChange']]
    return data

