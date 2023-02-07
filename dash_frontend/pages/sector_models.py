import dash
import numpy as np
import plotly.express as px
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from models.sector_models.incomestatements.income_statement import GeneralIncomeStatementModel

if __name__ == '__main__':
    app = dash.Dash()

dash.register_page(__name__,
                   path_template='/sectors/<sector_selection>',
                   title='Sectors',
                   name='Sectors')

'''
sector_dropdown = ['Food', 'BeverageAndTobaccoProducts', 'TextileMillsAndTextileProductMills', 'WoodProducts',
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
'''


@callback([Output('g0', 'figure'),
           Output('g1', 'figure'),
           Output('g2', 'figure'),
           Output('g3', 'figure'),
           Output('g4', 'figure'),
           Output('g5', 'figure'),
           Output('g6', 'figure')], [Input('sector_sel', 'data')])
def update_figure(sector_selection='Food'):
    model = GeneralIncomeStatementModel(sector=sector_selection)
    qfr_cols = [f'{sector_selection}revenueseries', f'{sector_selection}depreciationseries',
                f'{sector_selection}costsseries', f'{sector_selection}interestexpenseseries']
    per_cap_spending = ["PCEDurableGoods", "PCENonDurableGoods", "PCEServices"]
    rate_cols = ['AAA_yield', 'BAA_Yeild', 'FedRate', 'MortgageRates', 'AutoRates']
    delinquency_rates = ['DelinquencyRateOnBusinessLoans', 'DelinquencyRateOnSingleFamilyResidentialMortgages',
                         'DelinquencyRateOnCreditCardLoans', 'DelinquencyRateOnLeaseFinancingReceivables',
                         'DelinquencyRateOnConsumerLoans']
    ppi_cols1 = model.ppi_cols[0:5]
    ppi_cols2 = model.ppi_cols[-10:-5]
    ppi_cols3 = model.ppi_cols[-5:]
    forecasted_data = model.data_for_model()
    figure0 = px.line(forecasted_data, x=forecasted_data.index, y=qfr_cols,
                      title='Quarterly Results',
                      template='plotly_dark')
    figure1 = px.line(forecasted_data, x=forecasted_data.index, y=per_cap_spending,
                      title='Personal Consumption Expenditures',
                      template='plotly_dark')
    figure2 = px.line(forecasted_data, x=forecasted_data.index, y=delinquency_rates,
                      title='Delinquency Rates',
                      template='plotly_dark')
    figure3 = px.line(forecasted_data, x=forecasted_data.index, y=rate_cols,
                      title='Interest Rates',
                      template='plotly_dark')
    figure4 = px.line(forecasted_data, x=forecasted_data.index, y=ppi_cols1,
                      title='PPI Index Values',
                      template='plotly_dark')
    figure5 = px.line(forecasted_data, x=forecasted_data.index, y=ppi_cols2,
                      title='PPI Index Values',
                      template='plotly_dark')
    
    figure6 = px.line(forecasted_data, x=forecasted_data.index, y=ppi_cols3,
                      title='PPI Index Values',
                      template='plotly_dark')
    return figure0, figure1, figure2, figure3, figure4, figure5, figure6


# this function has to be named layout for dash to input sector selection properly
def layout(sector_selection=None):
    lay_out = html.Div(id='sector', children=[
        html.H1(id='H1', children=f'{sector_selection}',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        dcc.Slider(1, 18, 1, value=0, id='date_slider1'),
        dcc.Graph(id='g0'),
        
        dcc.Graph(id='g1'),
        dcc.Graph(id='g2'),
        dcc.Graph(id='g3'),
        dcc.Graph(id='g4'),
        dcc.Graph(id='g5'),
        dcc.Graph(id='g6'),
        dcc.Store(id='sector_sel', data=sector_selection)])
    return lay_out


layout_for_sectors = layout()

if __name__ == '__main__':
    app.layout = layout('BeverageAndTobaccoProducts')
    app.run_server(debug=True)
