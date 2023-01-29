from os import path, mkdir

'''
This generates models for all of the fed quarterly financial result sectors, It creates models view and loads data 
'''
def main():
    sectors = ['Food', 'BeverageAndTobaccoProducts', 'TextileMillsAndTextileProductMills', 'WoodProducts',
               'Paper', 'PrintingAndRelatedSupportActivities', 'PetroleumAndCoalProducts', 'AllOtherChemicals',
               'PlasticsAndRubberProducts', 'NonmetallicMineralProducts', 'Foundrie',
               'FabricatedMetalProducts', 'Machinery', 'AllOtherElectronicProducts',
               'ElectricalEquipmentAppliancesAndComponents', 'FurnitureAndRelatedProducts',
               'MiscellaneousManufacturing', 'IronSteelAndFerroalloys', 'ComputerAndPeripheralEquipment',
               'BasicChemicalsResinsAndSynthetics', 'MotorVehiclesAndParts', 'NonferrousMetals',
               'CommunicationsEquipment', 'PharmaceuticalsAndMedicines', 'AerospaceProductsAndParts',
               'WholesaleTradeDurableGoods', 'WholesaleTradeNondurableGoods', 'FoodAndBeverageStores',
               'ClothingAndGeneralMerchandiseStores', 'PublishingIndustriesExceptInternet',
               'MotionPictureAndSoundRecordingIndustries: BroadcastingExceptInternet',
               'Telecommunications', 'AllOtherInformation', 'ComputerSystemsDesignAndRelatedServices',
               'ManagementAndTechnicalConsultingService', 'ScientificResearchAndDevelopmentServices',
               'AllOtherProfessionalAndTechnicalServicesExceptLegalServices', 'ApparelAndLeatherProducts',
               'AllMining', 'AllOtherRetailTrade']
    for sector in sectors:
        code_to_write = \
            f"import pandas as pd\n\
import sqlite3\n\
from os import path\n\n\n\
class {sector}IncomeStatementModel:\n\
    def __init__(self, date='2018-01-01'):\n\
        filename = path.abspath(__file__)\n\
        current_directory = filename.rstrip('consumerhealth.py')\n\
        dbpath = path.join(current_directory, '../../../data/cache/data.db')\n\
        self.file_path = path.join(current_directory, 'saved_models/latest')\n\
        self.con = sqlite3.connect(dbpath)\n\
        self.data = self.data_for_model(date)\n\
        self.model = self.load_model()\n\
\n\
    def data_for_model(self, start_date):\n\
        '''\n\
        :param start_date:\n\
        :return: target, rate, sector, debt_factor, income\n\
        '''\n\
        try:\n\
            data = pd.read_sql(f'SELECT * from incomestatementview', self.con)\n\
        except:\n\
            self.make_view()\n\
            data = pd.read_sql(f'SELECT * from incomestatementview', self.con)\n\
        data['date'] = pd.to_datetime(data.date)\n\
        data = data[data['date'] >= start_date]\n\
        data = data.set_index('date')\n\
        data = data.fillna(method='ffill')\n\
        data = data.astype('float32')\n\
        ppi_cols = pd.read_csv('ppi_cols.csv')\n\
        ppi_cols = ppi_cols[ppi_cols['{sector}' == 1]].index.values\n\
        self.ppi_cols = ppi_cols\n\
        qfr_cols = ['{sector}revenueseries', '{sector}depreciationseries',\n\
                    '{sector}costsseries','{sector}interestexpenseseries']\n\
\n\
        data = data[qfr_cols+['PCEDurableGoods', 'PCENonDurableGoods', 'PCEServices', 'DelinquencyRateOnBusinessLoans',\n\
                     'DelinquencyRateOnSingleFamilyResidentialMortgages', 'DelinquencyRateOnCreditCardLoans',\n\
                     'DelinquencyRateOnLeaseFinancingReceivables', 'DelinquencyRateOnConsumerLoans']+ppi_cols +\n\
                     #######\n\
                     ['MortgageRates', 'AutoRates', 'FedRate']]\n\
        return data\n\
\n\
    def make_and_train_model(self):\n\
\n\
        # load data\n\
        data = self.data_for_model('2002-02-01')\n\
        data = data.fillna(method='ffill').fillna(method='bfill')\n\
\n\
        from sklearn.linear_model import LinearRegression\n\
        X = pd.concat([data.shift(1)[12:], data.shift(2)[12:], data.shift(6)[12:], data.shift(12)[12:]], axis=1)\n\
        y = data[12:]\n\
        model = LinearRegression()\n\
        model.fit(X, y)\n\
        return model\n\
\n\
    def load_model(self):\n\
        # use to eager build model\n\
        try:\n\
            m = self.make_and_train_model()\n\
        except:\n\
            m = self.make_and_train_model()\n\
        return m\n\
\n\
    def autoregressive_forecast(self, prediction_array):\n\
        dff = self.data\n\
\n\
        for i in range(1, len(prediction_array)):\n\
            dff[-1:] = dff[-1:] * prediction_array[i]\n\
\n\
            X = pd.concat([dff.shift(1)[-1:], dff.shift(2)[-1:], dff.shift(6)[-1:], dff.shift(12)[-1:]], axis=1)\n\
\n\
            out = self.model.predict(X)\n\
            dff = pd.concat(\n\
                [dff, pd.DataFrame(out, columns=dff.columns, index=[dff.index[-1] + pd.DateOffset(months=1)])],\n\
                axis=0)\n\
        return dff\n\
\n\
    def make_view(self):\n\
        sql = ['drop view if exists consumerhealthview;',\n\
               'drop table if exists temp_cxhealth;',\n\
               'CREATE VIEW incomestatementview AS SELECT date,PCEDurableGoods,PCENonDurableGoods,PCEServices FROM debtandsavings'\n\
               ' left join ppi using (date) left join delinquency using (date) left join rates using (date);']\n\
        for queries in sql:\n\
            self.con.execute(queries)\n\
\n\
\n\
if __name__ == '__main__':\n\
    # Entry point for training model\n\
    model = {sector}IncomeStatementModel()\n\
    model = model.make_and_train_model()\n"

        path_string = f'../'
        with open(f'{path_string}{sector}_income_statement.py', 'w') as f:
            f.write(code_to_write)
            f.close()


if __name__ == '__main__':
    main()
