import dash
import pandas as pd
from dash import html, dcc, callback
import plotly.express as px
from dash.dependencies import Input, Output, State
import sqlite3
from os import path
from data.data_pulling_functions import option_quote
from models.valuation_tools import option_spreads

if __name__ == '__main__':
    app = dash.Dash()

dash.register_page(__name__, path='/option_spreads',
                   title='option_spreads',
                   name='option_spreads')


# return the heatmaps for the option spreads
@dash.callback(Input('option_submit_button', 'n_clicks'), State('ticker_input', 'value'),
               State('put_call_dropdown', 'value'), State('calendar_dropdown', 'value'),
               State('strike', 'value'), Output('heat_map', 'figure'))
def update_heat_map(_, ticker_input, put_call, calendar, strike):
    # get the data
    data = option_spreads.OptionSpreads(ticker_input, put_call, calendar, strike)
    figure1 = px.imshow(data, text_auto=True, aspect="auto")
    return figure1


# update the calendar dropdown with the dates
@dash.callback(Input('ticker_input', 'value'), Output('calendar_dropdown', 'options'))
def update_calendar_dropdown(ticker_input):
    dates = option_quote.get_expiration_dates(ticker_input)
    return [{'label': i, 'value': i} for i in dates]


# update the strike dropdown with the strikes
@dash.callback(Input('calendar_dropdown', 'value'), State('ticker_input', 'value')
    , Output('strike', 'options'))
def update_strike_dropdown(calendar_dropdown, ticker_input):
    strikes = option_quote.get_strikes(ticker_input, calendar_dropdown)
    return [{'label': i, 'value': i} for i in strikes]


def layout_for_option_spread():
    layout_to_return = html.Div(id='parent', style={'backgroundColor': '#121212'}, children=[
        html.Title('This is currently broken due to yahoo finance changing their website'),
        # inline dash components: text field,drop down with put/call dropdown,callendar/vertical dropdown, and a drop
            # down of strikes, and a submit button
        html.Div(id='input_fields', children=[
            html.Div(id='text_field', children=[
                html.P('Enter a ticker'),
                dcc.Input(id='ticker_input', type='text', value='AAPL'),
            ]),
            html.Div(id='put_call_dropdown', children=[
                html.P('Select Put or Call'),
                dcc.Dropdown(id='put_call_dropdown', options=[
                    {'label': 'Put', 'value': 'P'},
                    {'label': 'Call', 'value': 'C'}
                ], value='P'),
            ]),
            html.Div(id='strike_calendar_dropdown', children=[
                html.P('Select Calendar or Vertical'),
                dcc.Dropdown(id='cal_vert_dropdown', options=[
                    {'label': 'Vertical Spread', 'value': 'V'},
                    {'label': 'Calendar Spread', 'value': 'C'}],
                             value='Calendar'),
                html.Div(id='calendar_dropdown', children=[
                    html.P('Select Date'),
                    dcc.Dropdown(id='calendar_dropdown', value='Calendar')]),
                html.Div(id='strike_dropdown', children=[
                    html.P('Select Strike'),
                    dcc.Dropdown(id='strike_dropdown', value='Strike'),
                ]),
                html.Div(id='submit_button', children=[
                    html.Button('Submit', id='option_submit_button')
                ]),
            ]),
            dcc.Graph(id='heat_map_for_options'),
        
        ])])
    return layout_to_return


layout = layout_for_option_spread()

if __name__ == '__main__':
    app = dash.Dash()
    app.layout = layout
    app.run_server(debug=True)
