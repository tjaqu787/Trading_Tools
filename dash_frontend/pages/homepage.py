import dash
import pandas as pd
from dash import html, dcc, callback
import plotly.express as px
from dash.dependencies import Input, Output, State
import sqlite3
from os import path


if __name__ == '__main__':
    app = dash.Dash()

dash.register_page(__name__, path='/',
                   title='homepage',
                   name='homepage')


def layout_for_inflation_impact():
    filename = path.abspath(__file__)
    dir = filename.rstrip('homepagedata.py')
    dbpath = path.join(dir, "../../data/data.db")
    engine = sqlite3.connect(dbpath)
    
    data = pd.read_sql('SELECT * FROM homepageview', con=engine)
    per_cap_spending = ["PCEDurableGoods", "PCENonDurableGoods", "PCEServices", 'Personalinterestpayments',
                        'DisposablePersonalIncome', 'PersonalSaving']
    cpi_cols1 = ['Transportation', 'Housing', 'Foodandbeverages', 'Medicalcare']
    rate_cols = ['MortgageRates', 'AutoRates', 'FedRate']
    delinquency_rates = ['DelinquencyRateOnBusinessLoans', 'DelinquencyRateOnSingleFamilyResidentialMortgages',
                         'DelinquencyRateOnCreditCardLoans', 'DelinquencyRateOnLeaseFinancingReceivables',
                         'DelinquencyRateOnConsumerLoans']
    # load forecast data and append to data array to plot
    
    figure1 = px.line(data, x=data.index, y=per_cap_spending,
                      title='Personal Consumption Expenditures',
                      template='plotly_dark')
    figure2 = px.line(data, x=data.index, y=delinquency_rates,
                      title='Delinquency Rates',
                      template='plotly_dark')
    figure3 = px.line(data, x=data.index, y=cpi_cols1,
                      title='CPI Index Values',
                      template='plotly_dark')
    figure5 = px.line(data, x=data.index, y=rate_cols,
                      title='Interest Rates',
                      template='plotly_dark')
    layout_to_return = html.Div(id='parent', style={'backgroundColor': '#121212'}, children=[
        html.Title('Economic Correction'),
        dcc.Graph(figure1),
        dcc.Graph(figure2),
        dcc.Graph(figure3),
        dcc.Graph(figure5)
    ])
    return layout_to_return
    
    

layout = layout_for_inflation_impact()

if __name__ == '__main__':
    app = dash.Dash()
    app.layout = layout
    app.run_server(debug=True)