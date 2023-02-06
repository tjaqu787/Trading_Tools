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
    from data.data_series_pull.for_lazy_load import lazy_load_for_homepage_plot
    
    data = lazy_load_for_homepage_plot()
    per_cap_spending = ["PCEDurableGoods", "PCENonDurableGoods", "PCEServices"]
    credit_change = ['RevolvingCreditChange', 'NonRevolvingCreditChange']
    rate_cols = ['MortgageRates', 'AutoRates', 'FedRate']
    delinquency_rates = ['DelinquencyRateOnBusinessLoans', 'DelinquencyRateOnSingleFamilyResidentialMortgages',
                         'DelinquencyRateOnCreditCardLoans', 'DelinquencyRateOnLeaseFinancingReceivables']
    
    # load forecast data and append to data array to plot
    figure1 = px.line(data, x=data.index, y=per_cap_spending,
                      title='Personal Consumption Expenditures',
                      template='plotly_dark')
    figure2 = px.line(data, x=data.index, y=delinquency_rates,
                      title='Delinquency Rates',
                      template='plotly_dark')
    figure3 = px.line(data, x=data.index, y=credit_change,
                      title='CPI Index Values',
                      template='plotly_dark')
    figure5 = px.line(data, x=data.index, y=rate_cols,
                      title='Interest Rates',
                      template='plotly_dark')
    layout_to_return = html.Div(id='parent', style={'backgroundColor': '#121212'}, children=[
        html.Title('Economic Correction'),
        dcc.Graph(id='home1', figure=figure1),
        dcc.Graph(id='home2', figure=figure2),
        dcc.Graph(id='home3', figure=figure3),
        dcc.Graph(id='home4', figure=figure5)
    ])
    return layout_to_return


layout = layout_for_inflation_impact()

if __name__ == '__main__':
    app = dash.Dash()
    app.layout = layout
    app.run_server(debug=True)
