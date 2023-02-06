import pandas as pd
import sqlite3
from os import path
from data.data_pulling_functions.fed import data_from_fed

class ConsumerHealthModel:
    def _init__(self):
        # download the data from the fed
        
        
        data_from_fed()
    
    def data_for_model(self, start_date):
        data_from_fed()
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



if __name__ == '__main__':
    # Entry point for training model
    model = ConsumerHealthModel()
    model = model.data_for_model()
