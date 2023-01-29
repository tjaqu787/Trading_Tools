import numpy as np
import pandas as pd
import sqlite3
from os import path
from functools import lru_cache


class GeneralIncomeStatementModel:
    @lru_cache(maxsize=50)
    def __init__(self, date='2018-01-01', sector='ComputerSystemsDesignAndRelatedServices'):
        filename = path.abspath(__file__)
        current_directory = filename.rstrip('income_statement.py')
        dbpath = path.join(current_directory, '../../../data/data.db')
        self.sector = sector
        self.file_path = path.join(current_directory, 'saved_models/latest')
        self.con = sqlite3.connect(dbpath, check_same_thread=False)
        ppi_cols = pd.read_csv(
            f'{path.abspath(__file__).rstrip("income_statement.py")}/template/ppi_factors_by_industry.csv')
        ppi_cols.index = ppi_cols['Products']
        ppi_cols = list(ppi_cols[ppi_cols[f'{self.sector}'] == 1].index.values)
        self.ppi_cols = ppi_cols
        self.rate_cols = ['AAA_yield', 'BAA_Yeild', 'FedRate', 'MortgageRates', 'AutoRates']
        self.qfr_cols = [f'{self.sector}revenueseries', f'{self.sector}depreciationseries',
                         f'{self.sector}costsseries', f'{self.sector}interestexpenseseries']
        self.pce_cols = ['PCEDurableGoods', 'PCENonDurableGoods', 'PCEServices']
        self.delinquency_cols = ['DelinquencyRateOnBusinessLoans',
                                 'DelinquencyRateOnSingleFamilyResidentialMortgages',
                                 'DelinquencyRateOnCreditCardLoans',
                                 'DelinquencyRateOnLeaseFinancingReceivables', 'DelinquencyRateOnConsumerLoans']
        self.consumer_delinquency_cols = ['DelinquencyRateOnSingleFamilyResidentialMortgages',
                                          'DelinquencyRateOnCreditCardLoans',
                                          'DelinquencyRateOnConsumerLoans']
        self.business_delinquency_cols = ['DelinquencyRateOnBusinessLoans',
                                          'DelinquencyRateOnLeaseFinancingReceivables']
        
        self.data_cols = self.qfr_cols + self.pce_cols + self.delinquency_cols + list(ppi_cols) + self.rate_cols
    
    @lru_cache(maxsize=50)
    def data_for_model(self):
        '''
        :return: target, rate, sector, debt_factor, income
        '''
        try:
            data = pd.read_sql(f'SELECT * from incomestatementview', self.con)
        except:
            self.make_view()
            data = pd.read_sql(f'SELECT * from incomestatementview', self.con)
        data['date'] = pd.to_datetime(data.date)
        data = data.set_index('date')
        data = data.fillna(method='ffill').fillna(method='bfill')
        data = data.astype('float32')
        
        data = data[self.data_cols]
        return data
    
    def make_view(self):
        sql = ['drop view if exists incomestatementview;',
               'CREATE VIEW incomestatementview AS SELECT * FROM debtandsavings'
               ' left join ppi using (date) left join delinquency using (date) left join rates using (date);']
        for queries in sql:
            self.con.execute(queries)


if __name__ == '__main__':
    # Entry point for training model
    m = GeneralIncomeStatementModel()
