import pandas as pd
import sqlite3
from os import path


def make_homepage_view():
    columns = ["PCEDurableGoods", "PCENonDurableGoods", "PCEServices", 'Personalinterestpayments',
               'DisposablePersonalIncome', 'PersonalSaving', 'Transportation', 'Housing', 'Foodandbeverages',
               'Medicalcare', 'MortgageRates', 'AutoRates', 'FedRate', 'DelinquencyRateOnBusinessLoans',
               'DelinquencyRateOnSingleFamilyResidentialMortgages', 'DelinquencyRateOnCreditCardLoans',
               'DelinquencyRateOnLeaseFinancingReceivables', 'DelinquencyRateOnConsumerLoans']
    filename = path.abspath(__file__)
    dir = filename.rstrip('homepagedata.py')
    dbpath = path.join(dir, "../../data/data.db")
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    cur.execute('DROP VIEW IF EXISTS homepageview')
    cur.execute(f'CREATE VIEW homepageview AS SELECT {columns} FROM consumerhealthview')
    con.commit()
    con.close()
    if __name__ == '__main__':
        con = sqlite3.connect(dbpath)
        data = pd.read_sql('SELECT * FROM homepageview', con=con)
        print(data)

if __name__ == '__main__':
    make_homepage_view()

