import dash
import pandas as pd
from dash import html, dcc, callback, dash_table
import plotly.express as px
from dash.dependencies import Input, Output, State
from models.sector_models.consumer_health.consumerhealth import data_for_consumer_health

if __name__ == '__main__':
    app = dash.Dash()

dash.register_page(__name__, path='/consumerhealth',
                   title='ConsumerHealth',
                   name='ConsumerHealth')


@callback([Output('cx_inflation_g1', 'figure'), Output('cx_inflation_g2', 'figure'),
           Output('cx_inflation_g3', 'figure'), Output('cx_inflation_g4', 'figure'),
           Output('cx_inflation_g5', 'figure'), Output('cx_inflation_g6', 'figure')],
          [Input('cx_inflation_store', 'data')])
def update_figure(_):
    per_cap_spending = ["PCEDurableGoods", "PCENonDurableGoods", "PCEServices", 'Personalinterestpayments',
                        'DisposablePersonalIncome', 'PersonalSaving', 'TotalCredit']
    cpi_cols1 = ['Transportation', 'Recreation', 'Othergoodsandservices', 'Medicalcare']
    cpi_cols2 = ['Housing', 'Foodandbeverages', 'Educationandcommunication', 'Apparel']
    rate_cols = ['MortgageRates', 'AutoRates', 'FedRate']
    delinquency_rates = ['DelinquencyRateOnBusinessLoans', 'DelinquencyRateOnSingleFamilyResidentialMortgages',
                         'DelinquencyRateOnCreditCardLoans', 'DelinquencyRateOnLeaseFinancingReceivables',
                         'DelinquencyRateOnConsumerLoans']
    debt_factor_cols = ['RevolvingCreditChange', 'NonRevolvingCreditChange']
    # load forecast data and append to data array to plot
    forecasted_data = data_for_consumer_health()
    
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
    return figure1, figure2, figure3, figure4, figure5, figure6


def layout_for_inflation_impact():
    layout_to_return = html.Div(id='parent', style={'backgroundColor': '#121212'}, children=[
        dcc.Graph(id='cx_inflation_g1'),
        dcc.Graph(id='cx_inflation_g2'),
        dcc.Graph(id='cx_inflation_g3'),
        dcc.Graph(id='cx_inflation_g4'),
        dcc.Graph(id='cx_inflation_g5'),
        dcc.Graph(id='cx_inflation_g6'),
        dcc.Store(id='cx_inflation_store', data=1)
    ])
    return layout_to_return


layout = layout_for_inflation_impact()

if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)
