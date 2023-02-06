import pandas as pd
import numpy as np
import datetime
from data.data_pulling_functions import option_quote
import warnings
import plotly.graph_objects as go
warnings.filterwarnings("ignore")

class OptionSpreads():
    def __init__(self, symbol,put_or_call):
        self.symbol = symbol
        self.put_or_call = put_or_call
        self.dates = option_quote.get_expiration_dates(self.symbol)
    
    def vertical_spread(self,expiry_date):
        option_chain = option_quote.for_vertical(self.symbol, expiry_date, self.put_or_call)
        option_chain = option_chain.rename(columns={'Strike': 'Buy_Strike'})
        option_chain = option_chain.set_index('Buy_Strike')
        
        option_spreads = pd.DataFrame()
        print('processing vertical spreads')
        for buy in option_chain.index:
            for sell in option_chain.index:
                if buy != sell:
                    bid = round(option_chain.loc[buy, 'Bid'] - option_chain.loc[sell, 'Ask'], 1)
                    ask = round(option_chain.loc[buy, 'Ask'] - option_chain.loc[sell, 'Bid'], 1)
                    payoff = int(sell) - int(buy)
                    risk_reward = payoff / ((ask * 2 + bid) / 3)
                    if bid < 0:
                        below_zero = '***'
                        bid_ask = f'{bid}-{ask} \n {payoff}\n{below_zero}'
                    else:
                        bid_ask = f'{bid}-{ask} \n {payoff}'
                else:
                    risk_reward = 0
                    bid = '-'
                    ask = '-'
                    bid_ask = '-'
                option_spreads = option_spreads.append([[buy, sell, bid, ask, bid_ask, risk_reward]], ignore_index=True)
        cols = ['Buy_Strike', 'Sell_Strike', 'bid', 'ask', 'Bid-Ask\nPayoff', 'risk_reward']
        new_dict = dict(zip(option_spreads.columns.values, cols))
        option_spreads = option_spreads.rename(columns=new_dict)
        
        option_spreads = option_spreads.set_index(keys=["Buy_Strike", "Sell_Strike"])
        
        return option_spreads
    
    def calendar_spread(self,strike):
        option_chain = option_quote.for_calendar(self.symbol,strike,self.put_or_call)
        option_chain.index = option_chain['Expire Date']
        print('processing calendar spreads')
        option_spreads = pd.DataFrame()
        for buy in option_chain.index:
            for sell in option_chain.index:
                if buy != sell:
                    bid = round(option_chain.loc[buy, 'Bid'] - option_chain.loc[sell, 'Ask'], 1)
                    ask = round(option_chain.loc[buy, 'Ask'] - option_chain.loc[sell, 'Bid'], 1)
                    delta = datetime.datetime.strptime(buy, '%Y-%m-%d').date() - \
                            datetime.datetime.strptime(sell, '%Y-%m-%d').date()
                    
                    # create a weighted average of ask and bid to calculate dollars per day
                    try:
                        payoff = int(int(delta.days) / ((ask * 2 + bid) / 3))
                    except OverflowError:
                        payoff = int(int(delta.days) / ((ask * 2 + bid + 1) / 3))
                    except RuntimeWarning:
                        payoff = int(int(delta.days) / ((ask * 2 + bid + 1) / 3))
                        
                    bid_ask = f'{bid}-{ask}\n{delta.days}'
                    
                else:
                    payoff = 0
                    bid = '-'
                    ask = '-'
                    delta = 0
                    bid_ask = '-'
                option_spreads = option_spreads.append([[buy, sell, bid, ask, delta, bid_ask, payoff]],
                                                       ignore_index=True)
        cols = ['Buy_Date', 'Sell_Date', 'bid', 'ask', 'days', 'Bid-Ask\nPayoff', 'risk_reward']
        new_dict = dict(zip(option_spreads.columns.values, cols))
        option_spreads = option_spreads.rename(columns=new_dict)
        
        option_spreads = option_spreads.set_index(keys=["Buy_Date", "Sell_Date"])
        
        return option_spreads
    
    @staticmethod
    def plotter(dataframe_from_class):
        text = np.asarray(dataframe_from_class['Bid-Ask\nPayoff'].unstack(level=-1))
    
        colour = pd.DataFrame(dataframe_from_class['risk_reward']).rename(columns={'risk_reward': ''}).unstack(level=-1)
    
        figure1 = go.Figure(go.Heatmap(x=colour.index, y=colour.columns.values, z=colour,
                                       text=text, texttemplate="%{text}", ))
        
        figure1.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        return figure1



if __name__ == '__main__':
    symbol = 'AAPL'
    strike = option_quote.get_expiration_dates(symbol)[4]
    print(strike)
    caw = OptionSpreads(symbol, 'put')
    import plotly.graph_objects as go
    data = caw.vertical_spread(strike)
    colour = data['risk_reward'].unstack(level=-1)
    text = data['Bid-Ask\nPayoff'].unstack(level=-1)
    figure1 = go.Figure(go.Heatmap(x=colour.index.values,y=colour.columns.values, z=colour,
                                   text=text, texttemplate="%{text}",))
    figure1.show()
