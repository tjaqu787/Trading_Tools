

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from Data import yahoo_fin_Option_quotes


class OptionSpreads():
    def __init__(self,option_chain,graph_title):
        self.option_chain=option_chain
        self.vert_or_cal=self.detect_vert_or_cal()
        self.graph_title=str(graph_title)

    def detect_vert_or_cal(self):

        if 'Strike' in self.option_chain:
            self.vertical_spread()
            return 'Vertical'

        elif 'Expire Date' in self.option_chain:
            self.calendar_spread()
            return 'Calendar'

        elif isinstance(self.option_chain, pd.DataFrame):
            ValueError('Reformat df')
            return

        else:
            ValueError("Nat a valid DF")
            return

    def vertical_spread(self,return_df=False):
        option_chain = self.option_chain.rename(columns={'Strike': 'Buy_Strike'})
        option_chain = option_chain.set_index('Buy_Strike')

        option_spreads = pd.DataFrame()
        for buy in option_chain.index:
            for sell in option_chain.index:
                if buy!=sell:
                    bid=round(option_chain.loc[buy,'Bid']-option_chain.loc[sell,'Ask'],1)
                    ask=round(option_chain.loc[buy,'Ask']-option_chain.loc[sell,'Bid'],1)
                    payoff=int(sell)-int(buy)
                    risk_reward=payoff/((ask*2+bid)/3)
                    if bid <0:
                        below_zero='***'
                        bid_ask=f'{bid}-{ask} \n {payoff}\n{below_zero}'
                    else:
                        bid_ask=f'{bid}-{ask} \n {payoff}'
                else:
                    risk_reward=0
                    bid='-'
                    ask='-'
                    bid_ask='-'
                option_spreads=option_spreads.append([[buy,sell,bid,ask,bid_ask,risk_reward]],ignore_index=True)
        cols = ['Buy_Strike','Sell_Strike','bid','ask','Bid-Ask\nPayoff','risk_reward']
        new_dict = dict(zip(option_spreads.columns.values, cols))
        option_spreads=option_spreads.rename(columns=new_dict)

        option_spreads=option_spreads.set_index(keys=["Buy_Strike","Sell_Strike"])

        self.option_spreads=option_spreads

        if return_df:
            return option_spreads

    def calendar_spread(self,return_df=False):
        option_chain = self.option_chain.rename(columns={'Expire Date': 'Buy_Date'})
        option_chain = option_chain.set_index('Buy_Date')

        option_spreads = pd.DataFrame()
        for buy in option_chain.index:
            for sell in option_chain.index:
                if buy != sell:
                    bid = round(option_chain.loc[buy, 'Bid'] - option_chain.loc[sell, 'Ask'], 1)
                    ask = round(option_chain.loc[buy, 'Ask'] - option_chain.loc[sell, 'Bid'], 1)
                    delta = datetime.datetime.strptime(buy,'%Y-%m-%d').date() - datetime.datetime.strptime(sell,'%Y-%m-%d').date()
                    try:
                        payoff= int(int(delta.days)/((ask*2+bid)/3))
                    except OverflowError:
                        payoff= int(int(delta.days)/((ask*2+bid+1)/3))
                    bid_ask = f'{bid}-{ask}\n{delta.days}'
                else:
                    payoff=0
                    bid = '-'
                    ask = '-'
                    delta=0
                    bid_ask='-'
                option_spreads = option_spreads.append([[buy, sell,bid,ask,delta, bid_ask,payoff]], ignore_index=True)
        cols = ['Buy_Date', 'Sell_Date','bid','ask','days','Bid-Ask\nPayoff','risk_reward']
        new_dict = dict(zip(option_spreads.columns.values, cols))
        option_spreads = option_spreads.rename(columns=new_dict)

        option_spreads = option_spreads.set_index(keys=["Buy_Date", "Sell_Date"])
        self.option_spreads=option_spreads

        if return_df:
            return option_spreads

    def formatting_for_visualisation(self):
        graph_input=self.option_spreads['Bid-Ask\nPayoff']
        graph_input=graph_input.unstack(level=-1)
        graph_input=np.asarray(graph_input)

        colouring=pd.DataFrame(self.option_spreads['risk_reward'])
        colouring=colouring.rename(columns={'risk_reward':''})
        colouring=colouring.unstack(level=-1)

        return colouring, graph_input

    def plotter(self):
        colouring, graph_input = self.formatting_for_visualisation()
        plt.subplots(figsize=(150,150))
        sns.heatmap(colouring, annot=graph_input, fmt='s',linewidths=.5)
        plt.title(self.graph_title)
        plt.show()

        
if __name__ == '__main__'
    symbol='kndi'
    strike=16
    #strike='2021-03-19'
    x=yahoo_fin_Option_quotes.OptionsChain(symbol=symbol,calls_or_puts='put',date_or_strike=strike).option_chain
    #x.drop(x.tail(5).index,inplace=True)
    #x.drop(x.head(7).index,inplace=True)
    caw=OptionSpreads(x,strike)
    caw.plotter()
