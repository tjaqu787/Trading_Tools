import dash
import pandas as pd
from dash import html, dcc, callback, dash_table
import plotly.express as px
from dash.dependencies import Input, Output, State
from models.sector_models.consumer_health.consumerhealth import ConsumerHealthModel

if __name__ == '__main__':
    app = dash.Dash()

dash.register_page(__name__, path='/consumerhealth',
                   title='ConsumerHealth',
                   name='ConsumerHealth')


@callback([Output('cx_inflation_g1', 'figure'), Output('cx_inflation_g2', 'figure'),
           Output('cx_inflation_g3', 'figure'), Output('cx_inflation_g4', 'figure'),
           Output('cx_inflation_g5', 'figure'), Output('cx_inflation_g6', 'figure'),
           Output('cx_inflation_table1', 'columns'), Output('cx_inflation_table1','data'),
           Output('cx_inflation_table2', 'columns'), Output('cx_inflation_table2','data'),
           Output('cx_inflation_table3', 'columns'), Output('cx_inflation_table3','data'),
           Output('cx_inflation_table4', 'columns'), Output('cx_inflation_table4','data'),
           Output('cx_inflation_table5', 'columns'), Output('cx_inflation_table5','data'),
           Output('cx_inflation_table6', 'columns'), Output('cx_inflation_table6','data')],
          [Input('cx_inflation_submit', 'n_clicks'), Input('cx_inflation_submit2', 'n_clicks'),
           State('cx_inflation_table1', 'data'), State('cx_inflation_table2', 'data'),
           State('cx_inflation_table3', 'data'), State('cx_inflation_table4', 'data'),
           State('cx_inflation_table5', 'data'), State('cx_inflation_table6', 'data'), ])
def update_figure(_, __, table1, table2, table3, table4, table5, table6,n_ahead=18):
    change_array = pd.concat(objs=[pd.DataFrame(table1),
                                   pd.DataFrame(table2),
                                   pd.DataFrame(table3),
                                   pd.DataFrame(table4),
                                   pd.DataFrame(table5),
                                   pd.DataFrame(table6)], axis=1).transpose()
    model = ConsumerHealthModel()
    per_cap_spending = ["PCEDurableGoods", "PCENonDurableGoods", "PCEServices", 'Personalinterestpayments',
                        'DisposablePersonalIncome', 'PersonalSaving', 'TotalCredit']
    cpi_cols1 = ['Transportation', 'Recreation', 'Othergoodsandservices', 'Medicalcare']
    cpi_cols2 = ['Housing', 'Foodandbeverages', 'Educationandcommunication', 'Apparel']
    rate_cols = ['MortgageRates', 'AutoRates', 'FedRate']
    delinquency_rates = ['DelinquencyRateOnBusinessLoans', 'DelinquencyRateOnSingleFamilyResidentialMortgages',
                         'DelinquencyRateOnCreditCardLoans', 'DelinquencyRateOnLeaseFinancingReceivables',
                         'DelinquencyRateOnConsumerLoans']
    debt_factor_cols = ['RevolvingCreditChange', 'NonRevolvingCreditChange']
    #load forecast data and append to data array to plot
    if change_array.empty:
        forcast_data = model.forecast(n_ahead=n_ahead)
        
    else:
        change_array = change_array.transpose()
        forecasted_data = model.autoregressive_forecast(change_array)

    figure1 = px.line(forecasted_data, x=forecasted_data.index, y=per_cap_spending,
                      title='Personal Consumption Expenditures',
                      template='plotly_dark')
    figure2 = px.line(forecasted_data, x=forecasted_data.index, y=delinquency_rates,
                      title='Delinquency Rates',
                      template='plotly_dark')
    figure3 = px.line(forecasted_data, x=forecasted_data.index, y=cpi_cols1,
                      title='CPI Index Values',
                      template='plotly_dark')
    figure4 = px.line(forecasted_data, x=forecasted_data.index, y=cpi_cols2,
                      title='CPI Index Values',
                      template='plotly_dark')
    figure5 = px.line(forecasted_data, x=forecasted_data.index, y=rate_cols,
                      title='Interest Rates',
                      template='plotly_dark')
    figure6 = px.line(forecasted_data, x=forecasted_data.index, y=debt_factor_cols,
                      title='Debt Factor',
                      template='plotly_dark')
    forecasted_data = forecasted_data[-18:].transpose().reset_index()
    # grab the last <forcast horizon> samples
    data1 = forecasted_data[per_cap_spending].to_dict('records')
    data2 = forecasted_data[delinquency_rates].to_dict('records')
    data3 = forecasted_data[cpi_cols1].to_dict('records')
    data4 = forecasted_data[cpi_cols2].to_dict('records')
    data5 = forecasted_data[rate_cols][-18:].to_dict('records')
    data6 = forecasted_data[debt_factor_cols][-18:].to_dict('records')
    columns=[{'name': i, 'id': i} for i in forecasted_data.columns]

    return figure1, figure2, figure3, figure4, figure5, figure6, \
              columns, data1, columns, data2, columns, data3, columns, data4, columns, data5, columns, data6


def layout_for_inflation_impact(forecast_horizon=18):
    variables = [7, 5, 4, 4, 3, 2]
    layout_to_return = html.Div(id='parent', style={'backgroundColor': '#121212'}, children=[
        
        html.Button('Forecast', id='cx_inflation_submit2', n_clicks=0, style={'background-color': '#121212',
                                                                              'color': 'white',
                                                                              'height': '50px',
                                                                              'width': '100px',
                                                                              'margin-top': '50px',
                                                                              'margin-left': '50px',
                                                                              'border-radius': '12px'}),
        dcc.Graph(id='cx_inflation_g1'),
        dash_table.DataTable(
            id='cx_inflation_table1',
            editable=True),
        
        dcc.Graph(id='cx_inflation_g2'),
        dash_table.DataTable(
            id='cx_inflation_table2',
            editable=True),
        
        dcc.Graph(id='cx_inflation_g3'),
        dash_table.DataTable(
            id='cx_inflation_table3',
            editable=True),
        
        dcc.Graph(id='cx_inflation_g4'),
        dash_table.DataTable(
            id='cx_inflation_table4',
            editable=True),
        
        dcc.Graph(id='cx_inflation_g5'),
        dash_table.DataTable(
            id='cx_inflation_table5',
            editable=True),
        
        dcc.Graph(id='cx_inflation_g6'),
        dash_table.DataTable(
            id='cx_inflation_table6',
            editable=True),
        
        html.Button('Forecast', id='cx_inflation_submit', n_clicks=0, style={'background-color': '#121212',
                                                                             'color': 'white',
                                                                             'height': '50px',
                                                                             'width': '100px',
                                                                             'margin-top': '50px',
                                                                             'margin-left': '50px',
                                                                             'border-radius': '12px'}),
    ])
    return layout_to_return


layout = layout_for_inflation_impact()

if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)
