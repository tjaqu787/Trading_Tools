import pandas as pd
import sqlite3
from os import path


class ConsumerHealthModel:
    def __init__(self, date='2018-01-01'):
        filename = path.abspath(__file__)
        dir = filename.rstrip('consumerhealth.py')
        dbpath = path.join(dir, "../../../data/data.db")
        self.file_path = path.join(dir, 'saved_models/latest')
        self.con = sqlite3.connect(dbpath)
        self.data = self.data_for_model(date)
    
    def data_for_model(self, start_date):
        """
        :param start_date:
        :return: target, rate, sector, debt_factor, income
        """
        try:
            data = pd.read_sql(f'SELECT * from consumerhealthview', self.con)
        except:
            self.make_view()
            data = pd.read_sql(f'SELECT * from consumerhealthview', self.con)
        
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
    
    def make_view(self):
        sql = ["drop view if exists consumerhealthview;",
               "drop table if exists temp_cxhealth;",
               "CREATE VIEW consumerhealthview AS SELECT * FROM debtandsavings left join cpi using (date) left join delinquency using (date);"]
        for queries in sql:
            self.con.execute(queries)


if __name__ == '__main__':
    # Entry point for training model
    model = ConsumerHealthModel()
    model = model.data_for_model()
