import dash
from dash import html, dcc, callback
import plotly.express as px
from dash.dependencies import Input, Output, State
from data.data_pulling_functions import option_quote
from models.valuation_tools import option_spreads
import plotly.graph_objects as go

if __name__ == '__main__':
    import dash_bootstrap_components as dbc
    
    app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])

dash.register_page(__name__, path='/option_spreads',
                   title='option_spreads',
                   name='option_spreads')


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


# return the heatmaps for the option spreads
@callback(Output('heat_map_for_options1', 'figure'),
          [Input('option_submit_button', 'n_clicks'), State('ticker_input', 'value'),
           State('put_call_dropdown', 'value'), State('cal_vert_dropdown', 'value'),
           State('calendar_dropdown', 'value'),
           State('strike_dropdown', 'value')])
def update_heat_map(_, ticker_input, put_call, cal_vert, calendar, strike):
    # get the data
    if _ is None:
        raise dash.exceptions.PreventUpdate
    if cal_vert == 'C':
        # return a blank graph if no strike is selected
        if strike is None:
            print('no strike selected')
            return blank_fig()
        # gets the option quote data then plots it returning figure
        data = option_spreads.OptionSpreads(ticker_input, put_call).calendar_spread(strike)
        figure1 = option_spreads.OptionSpreads.plotter(data)
    
    elif cal_vert == 'V':
        # return a blank graph if no date is selected
        if calendar is None:
            return blank_fig()
        # gets the option quote data then plots it returning figure
        data = option_spreads.OptionSpreads(ticker_input, put_call).vertical_spread(calendar)
        figure1 = option_spreads.OptionSpreads.plotter(data)
    else:
        print('no cal_vert selected')
        figure1 = blank_fig()
    
    '''
    colouring = pd.DataFrame(self.option_spreads['risk_reward'])
    colouring = colouring.rename(columns={'risk_reward': ''})
    colouring = colouring.unstack(level=-1)
    '''
    return figure1


# update the calendar dropdown with the dates
@callback(Output('calendar_dropdown', 'options'),
          [Input('ticker_input', 'value')])
def update_calendar_dropdown(ticker_input):
    dates = option_quote.get_expiration_dates(ticker_input)
    return [{'label': i, 'value': i} for i in dates]


# update the strike dropdown with the strikes
@callback([Output('strike_dropdown', 'options'), Output('strike_dropdown', 'value')],
          [Input('ticker_input', 'value'), Input('calendar_dropdown', 'value')])
def update_strike_dropdown(ticker_input, date):
    strikes = option_quote.get_strikes(ticker_input, date)
    out = [{'label': i, 'value': i} for i in strikes]
    return out, strikes[1]


def layout_for_option_spread():
    width = '200px'
    layout_to_return = html.Div(id='parent', children=[
        html.Title('Option Spreads'),
        # inline dash components: text field,drop down with put/call dropdown,callendar/vertical dropdown, and a drop
        # down of strikes, and a submit button
        html.Div(id='input_fields', children=[
            dcc.Input(id='ticker_input', type='text', value='AAPL', style={'width': width, 'display': 'inline-block'}),
            dcc.Dropdown(id='put_call_dropdown', options=[
                {'label': 'Call', 'value': 'call'},
                {'label': 'Put', 'value': 'put'}
            ], value='call', style={'width': width, 'display': 'inline-block'}),
            dcc.Dropdown(id='cal_vert_dropdown', options=[
                {'label': 'Vertical Spread', 'value': 'V'},
                {'label': 'Calendar Spread', 'value': 'C'}], value='C',
                         style={'width': width, 'display': 'inline-block'}),
            dcc.Dropdown(id='calendar_dropdown', value=None, style={'width': width, 'display': 'inline-block'}),
            dcc.Dropdown(id='strike_dropdown', value=None, style={'width': width, 'display': 'inline-block'}),
            html.Div(id='submit_button', children=[
                html.Button('Submit', id='option_submit_button')
            ], style={'width': width, 'display': 'inline-block'})
        ]),
        dcc.Graph(id='heat_map_for_options1', figure=blank_fig()),
    
    ])
    return layout_to_return


layout = layout_for_option_spread()

if __name__ == '__main__':
    app.layout = layout
    app.run_server(debug=True)
