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

'''sector_dropdown = ['Food', 'BeverageAndTobaccoProducts', 'TextileMillsAndTextileProductMills', 'WoodProducts',
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
           Output('g6', 'figure')], [Input('submit', 'n_clicks'), Input('submit2', 'n_clicks'),
                                     State('change_array', 'data'), State('sector_sel', 'data')])
def update_figure(_, __, change_array, sector_selection='Food'):
    model = GeneralIncomeStatementModel(sector=sector_selection)
    forecasted_data = model.autoregressive_forecast(change_array)
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


@callback(Output('change_array', 'data'),
          [State('date_slider1', 'value'), State('change_array', 'data'),
           Input('change_slider1', 'value'), Input('change_slider2', 'value'),
           Input('change_slider3', 'value'), Input('change_slider4', 'value'),
           Input('change_slider5', 'value'), Input('change_slider6', 'value'),
           Input('change_slider7', 'value'), Input('change_slider8', 'value'),
           Input('change_slider9', 'value'), Input('change_slider10', 'value'),
           Input('change_slider11', 'value'), Input('change_slider12', 'value'),
           Input('change_slider13', 'value'), Input('change_slider14', 'value'),
           Input('change_slider15', 'value'), Input('change_slider16', 'value'),
           Input('change_slider17', 'value'), Input('change_slider18', 'value'),
           Input('change_slider19', 'value'), Input('change_slider20', 'value'),
           Input('change_slider21', 'value'), Input('change_slider22', 'value'),
           Input('change_slider23', 'value'), Input('change_slider24', 'value'),
           Input('change_slider25', 'value'), Input('change_slider26', 'value'),
           Input('change_slider27', 'value'), Input('change_slider28', 'value'),
           Input('change_slider29', 'value'), Input('change_slider30', 'value'),
           Input('change_slider31', 'value'), Input('change_slider32', 'value'),
           ])
def update_change_array(date_slider1, change_array, *args):
    change_array[date_slider1] = args
    return change_array


# this function has to be named layout for dash to input sector selection properly
def layout(sector_selection=None, forecast_horizon=18, variables=32):
    lay_out = html.Div(id='sector', children=[
        html.H1(id='H1', children=f'{sector_selection}',
                style={'textAlign': 'center', 'marginTop': 40, 'marginBottom': 40}),
        html.Button('Forecast', id='submit2', n_clicks=0, style={'background-color': '#121212',
                                                                 'color': 'white',
                                                                 'height': '50px',
                                                                 'width': '100px',
                                                                 'margin-top': '50px',
                                                                 'margin-left': '50px', 'border-radius': '12px'}),
        dcc.Slider(1, 18, 1, value=0, id='date_slider1'),
        dcc.Graph(id='g0'),
        
        dcc.Slider(.5, 1.5, value=1, id='change_slider1', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider2', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider3', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider4', updatemode='drag'),
        
        dcc.Graph(id='g1'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider5', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider6', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider7', updatemode='drag'),
        
        dcc.Graph(id='g2'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider8', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider9', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider10', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider11', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider12', updatemode='drag'),
        
        dcc.Graph(id='g3'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider13', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider14', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider15', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider16', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider17', updatemode='drag'),
        
        dcc.Graph(id='g4'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider18', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider19', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider20', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider21', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider22', updatemode='drag'),
        
        dcc.Graph(id='g5'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider23', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider24', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider25', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider26', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider27', updatemode='drag'),
        
        dcc.Graph(id='g6'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider28', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider29', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider30', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider31', updatemode='drag'),
        dcc.Slider(.5, 1.5, value=1, id='change_slider32', updatemode='drag'),
        
        html.Button('Forecast', id='submit', n_clicks=0, style={'background-color': '#121212',
                                                                'color': 'white',
                                                                'height': '50px',
                                                                'width': '100px',
                                                                'margin-top': '50px',
                                                                'margin-left': '50px', 'border-radius': '12px'}),
        dcc.Store(id='change_array', data=np.ones((forecast_horizon, variables), dtype=float)),
        dcc.Store(id='sector_sel', data=sector_selection)])
    return lay_out


layout_for_sectors = layout()

if __name__ == '__main__':
    app.layout = layout('BeverageAndTobaccoProducts')
    app.run_server(debug=True)
